#!/usr/bin/env python3
"""
Télécharge les historiques de prix quotidiens (5 ans ou depuis la création)
pour chaque actif de collatéral et les écrit dans data/prix/<actif>.csv.

Usage :  python3 scripts/telecharger_prix.py            (tous les actifs)
         python3 scripts/telecharger_prix.py BTC SPY     (une sélection)

Sources publiques gratuites, sans clé API, lecture seule :
  - Kraken  (api.kraken.com, OHLC)      : BTC, ETH, PAXG, ETHFI, HYPE   (USD)
      · intervalle quotidien = 720 derniers jours ;
      · intervalle hebdomadaire pour compléter jusqu'à 5 ans (le CSV note "weekly"
        sur ces lignes : les stats les utilisent avec la bonne annualisation).
  - Nasdaq Data (api.nasdaq.com)        : SPY, QQQ, BIL, GLD  (proxies des xStocks / PAXG)
  - Stooq (stooq.com)                    : repli pour SPY/QQQ/BIL/GLD si Nasdaq échoue
  - Yahoo Finance (query1.finance.yahoo.com) : second repli
  - CoinGecko (api.coingecko.com, 365 j max sans clé) : SPYx, QQQx, TBLLx, GLDx,
        eBTC, weETH (tokens réellement utilisés en collatéral, historique court)

Format CSV : date,close,source,frequence   (close en USD)
Un fichier data/prix/_meta.json enregistre la date de téléchargement et la source.
Aucune transaction, aucune clé, aucun wallet.
"""
import csv, json, os, sys, time, datetime as dt, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "prix")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
      "Accept": "application/json,text/csv,*/*", "Accept-Language": "en-US,en;q=0.9"}
TODAY = dt.date.today()
START = TODAY - dt.timedelta(days=5 * 365 + 3)

def get(url, timeout=40, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (i + 1))
    raise last

# ---------- Kraken ----------
def kraken(pair, name):
    rows = {}
    # hebdo (long historique) puis quotidien (720 j) qui écrase les semaines récentes
    for interval, freq in ((10080, "weekly"), (1440, "daily")):
        d = json.loads(get(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"))
        if d.get("error"):
            raise RuntimeError(d["error"])
        key = [k for k in d["result"] if k != "last"][0]
        for c in d["result"][key]:
            date = dt.datetime.utcfromtimestamp(int(c[0])).date()
            if date < START and freq == "weekly":
                continue
            if freq == "daily":
                # supprime la ligne hebdo de la même semaine
                for k in list(rows):
                    if rows[k][2] == "weekly" and abs((k - date).days) < 7:
                        del rows[k]
            rows[date] = (float(c[4]), "kraken", freq)
        time.sleep(1.2)
    return rows

# ---------- Nasdaq ----------
def nasdaq(symbol, assetclass="etf"):
    url = ("https://api.nasdaq.com/api/quote/%s/historical?assetclass=%s&fromdate=%s&limit=9999&todate=%s"
           % (symbol, assetclass, START.isoformat(), TODAY.isoformat()))
    d = json.loads(get(url))
    rows = {}
    for r in d["data"]["tradesTable"]["rows"]:
        m, dd, y = r["date"].split("/")
        date = dt.date(int(y), int(m), int(dd))
        rows[date] = (float(r["close"].replace("$", "").replace(",", "")), "nasdaq", "daily")
    if not rows:
        raise RuntimeError("nasdaq: aucune ligne")
    return rows

# ---------- Stooq ----------
def stooq(symbol):
    txt = get(f"https://stooq.com/q/d/l/?s={symbol}&i=d")
    rows = {}
    for r in csv.DictReader(txt.splitlines()):
        date = dt.date.fromisoformat(r["Date"])
        if date >= START and r.get("Close"):
            rows[date] = (float(r["Close"]), "stooq", "daily")
    if not rows:
        raise RuntimeError("stooq: aucune ligne")
    return rows

# ---------- Yahoo ----------
def yahoo(symbol):
    d = json.loads(get(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d"))
    res = d["chart"]["result"][0]
    ts = res["timestamp"]; cl = res["indicators"]["quote"][0]["close"]
    rows = {}
    for t, c in zip(ts, cl):
        if c is not None:
            rows[dt.datetime.utcfromtimestamp(t).date()] = (float(c), "yahoo", "daily")
    return rows

# ---------- CoinGecko (365 j sans clé) ----------
def coingecko(cid):
    d = json.loads(get(f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=365&interval=daily"))
    rows = {}
    for t, p in d["prices"]:
        rows[dt.datetime.utcfromtimestamp(t / 1000).date()] = (float(p), "coingecko", "daily")
    time.sleep(3)  # limite de débit du plan public
    return rows

ASSETS = {
    # nom fichier : liste de (fonction, args) essayées dans l'ordre
    "BTC":   [(kraken, ("XBTUSD", "BTC"))],
    "ETH":   [(kraken, ("ETHUSD", "ETH"))],
    "PAXG":  [(kraken, ("PAXGUSD", "PAXG"))],
    "ETHFI": [(kraken, ("ETHFIUSD", "ETHFI"))],
    "HYPE":  [(kraken, ("HYPEUSD", "HYPE"))],
    "SPY":   [(nasdaq, ("SPY",)), (stooq, ("spy.us",)), (yahoo, ("SPY",))],
    "QQQ":   [(nasdaq, ("QQQ",)), (stooq, ("qqq.us",)), (yahoo, ("QQQ",))],
    "BIL":   [(nasdaq, ("BIL",)), (stooq, ("bil.us",)), (yahoo, ("BIL",))],
    "GLD":   [(nasdaq, ("GLD",)), (stooq, ("gld.us",)), (yahoo, ("GLD",))],
    # tokens réellement déposables (historique court : 365 j max sur l'API publique)
    "SPYx":  [(coingecko, ("sp500-xstock",))],
    "QQQx":  [(coingecko, ("nasdaq-xstock",))],
    "TBLLx": [(coingecko, ("tbll-xstock",))],
    "GLDx":  [(coingecko, ("gold-xstock",))],
    "eBTC":  [(coingecko, ("ether-fi-staked-btc",))],
    "weETH": [(coingecko, ("wrapped-eeth",))],
}

def main():
    os.makedirs(OUT, exist_ok=True)
    wanted = sys.argv[1:] or list(ASSETS)
    meta_path = os.path.join(OUT, "_meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for name in wanted:
        if name not in ASSETS:
            print(f"[{name}] inconnu, ignoré"); continue
        rows, used, err = None, None, None
        for fn, args in ASSETS[name]:
            try:
                rows = fn(*args); used = fn.__name__; break
            except Exception as e:  # noqa
                err = f"{fn.__name__}: {e}"
                print(f"[{name}] échec {err}")
        if not rows:
            print(f"[{name}] AUCUNE SOURCE DISPONIBLE — fichier non écrit"); meta[name] = {"erreur": err, "date": TODAY.isoformat()}; continue
        path = os.path.join(OUT, f"{name}.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["date", "close", "source", "frequence"])
            for date in sorted(rows):
                c, s, fr = rows[date]; w.writerow([date.isoformat(), f"{c:.6f}", s, fr])
        dates = sorted(rows)
        meta[name] = {"source": used, "date_telechargement": TODAY.isoformat(), "debut": dates[0].isoformat(),
                      "fin": dates[-1].isoformat(), "n": len(rows),
                      "jours_quotidiens": sum(1 for v in rows.values() if v[2] == "daily")}
        print(f"[{name}] {len(rows)} lignes via {used} ({dates[0]} → {dates[-1]})")
    json.dump(meta, open(meta_path, "w"), indent=2, ensure_ascii=False)
    print("Méta écrite dans", meta_path)
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "generer_bundle.py")], check=False)

if __name__ == "__main__":
    main()
