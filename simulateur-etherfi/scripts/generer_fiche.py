#!/usr/bin/env python3
"""Écrit data/FICHE_DONNEES.md (tableau complet des paramètres, statuts et dates) à partir de data/parametres.json."""
import json, os, datetime as dt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
j = json.load(open(os.path.join(ROOT, "data", "parametres.json"), encoding="utf-8"))
P = j["parametres"]
BLOCS = {"A": "Bloc A — Mon usage", "B": "Bloc B — Taux d'emprunt et rendements (à reconfirmer à chaque session)", "C": "Bloc C — Frais",
         "D": "Bloc D — Collatéral : LTV / seuil de liquidation / bonus", "Dbis": "Bloc D bis — Spreads de valorisation", "Dter": "Bloc D ter — Voies d'acquisition (interne vs externe)",
         "E": "Bloc E — Cashback", "F": "Bloc F — Scénarios et Monte Carlo"}
def val(v):
    if v is None: return "—"
    if isinstance(v, dict): return "<br>".join(f"{k} : {'?' if x is None else x}" for k, x in v.items() if not isinstance(x, dict))
    if isinstance(v, bool): return "oui" if v else "non"
    return str(v)
def esc(s): return str(s or "").replace("|", "\\|").replace("\n", " ")
out = ["# Fiche de données — simulateur ether.fi Cash", "", f"Générée le {dt.date.today().isoformat()} à partir de `data/parametres.json` (version {j['meta'].get('version')}, créé le {j['meta'].get('date_creation')}).", "",
       "Statuts : **CONFIRMÉ** = validé par vous (ou par le support, source « support ether.fi (chat) » : engage moins qu'une documentation) · **VÉRIFIÉ** = lu par Claude Code dans une source publique (URL et date dans `VERIFICATIONS.md`) · **DÉFAUT** = valeur datée du cahier des charges, non revalidée · **INCONNU** = bloque l'actif ou le calcul concerné (jamais remplacé par une valeur inventée).", ""]
from collections import Counter
c = Counter(p["statut"] for p in P.values())
out += ["| Statut | Nombre |", "|---|---|"] + [f"| {k} | {c.get(k,0)} |" for k in ["CONFIRMÉ", "VÉRIFIÉ", "DÉFAUT", "INCONNU"]] + [""]
for b, titre in BLOCS.items():
    out += [f"## {titre}", "", "| Paramètre | Valeur | Unité | Statut | Source | Date | Où trouver | Note |", "|---|---|---|---|---|---|---|---|"]
    for k, p in P.items():
        if p.get("bloc") != b: continue
        out.append(f"| **{esc(p['libelle'])}**<br>`{k}` | {esc(val(p['valeur']))} | {esc(p.get('unite'))} | {p['statut']} | {esc(p.get('source'))} | {esc(p.get('date'))} | {esc(p.get('ou_trouver'))} | {esc(p.get('note'))} |")
    out.append("")
open(os.path.join(ROOT, "data", "FICHE_DONNEES.md"), "w", encoding="utf-8").write("\n".join(out))
print("data/FICHE_DONNEES.md écrite :", len(P), "paramètres,", dict(c))
