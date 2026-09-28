#!/usr/bin/env python3
"""
Regroupe data/parametres.json et data/prix/*.csv dans data/bundle.js
(window.ETHERFI_DATA) pour que index.html fonctionne même ouvert en double-clic
(file://), sans serveur et sans appel réseau. Lancé automatiquement à la fin de
telecharger_prix.py ; peut être relancé seul après une modification de parametres.json.
"""
import csv, json, os, glob, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
params = json.load(open(os.path.join(ROOT, "data", "parametres.json"), encoding="utf-8"))
prix = {}
for path in sorted(glob.glob(os.path.join(ROOT, "data", "prix", "*.csv"))):
    name = os.path.splitext(os.path.basename(path))[0]
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    prix[name] = {"dates": [r["date"] for r in rows], "close": [float(r["close"]) for r in rows],
                  "source": rows[0]["source"] if rows else None,
                  "frequence": [r["frequence"] for r in rows]}
meta_path = os.path.join(ROOT, "data", "prix", "_meta.json")
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
out = {"genere_le": dt.datetime.now().isoformat(timespec="seconds"), "parametres": params, "prix": prix, "prix_meta": meta}
with open(os.path.join(ROOT, "data", "bundle.js"), "w", encoding="utf-8") as f:
    f.write("// Généré par scripts/generer_bundle.py — ne pas éditer à la main\nwindow.ETHERFI_DATA = ")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")
print("data/bundle.js écrit :", len(prix), "séries de prix,", len(params["parametres"]), "paramètres")
