# 07 — negRisk sans frais : fabrication à 1 $, revente > 1 $ ?

_Passe unique, lecture seule, 2026-07-29. Frais revalidés EN DIRECT (Gamma feesEnabled + CLOB /fee-rate), pas le flag stocké du run 1. Provenance [mesuré run 7] / [doc officielle] / [non vérifié]._

## Revalidation des 26 candidats (run 1)

- Candidats fees_status=off au run 1 : **26** [run 1].
- Revalidés en direct : **26** événements lus.
- **Encore sans frais effectifs (tous marchés, /fee-rate) : 26** [vérifié direct].
- **Encore actifs ET sans frais : 26** — dont **16 standard**, **10 augmentés**.
- Augmentés = conversion possiblement soumise à shortfall (issue placeholder « Other ») → fabrication NON sereine, à écarter. Le feeRate de conversion du NegRiskAdapter est on-chain, **[non vérifié]** ici.

## Événements actifs sans frais — par événement

| événement | type | issues (bid/no-bid) | Σ bids | net imm. | capacité $ (paniers) | net profond $ | résidu notion. | échéance (j) |
|---|---|---|--:|--:|--:|--:|--:|--:|
| São Tomé Presidential Election Fir | augmenté | 1/31 | 0.9990 | -0.0010 | 0 (0) | +0.00 | 0.01 | -10.0 |
| Which party will gain most seats i | augmenté | 6/28 | 0.9970 | -0.0030 | 0 (0) | +0.00 | 0.00 | 52.0 |
| Russia Parliamentary Election Winn | augmenté | 7/27 | 0.9900 | -0.0100 | 0 (0) | +0.00 | 0.00 | 52.0 |
| Next Prime Minister of Ethiopia? | augmenté | 8/25 | 0.9800 | -0.0200 | 0 (0) | +0.00 | 0.00 | -59.0 |
| Where will Zelenskyy and Putin mee | augmenté | 14/16 | 0.9760 | -0.0240 | 0 (0) | +0.00 | 0.00 | 154.0 |
| Avg. # of ships transiting Strait  | standard | 5/0 | 0.9730 | -0.0270 | 0 (0) | +0.00 | 0.00 | 2.0 |
| Who will be the next Prime Ministe | augmenté | 18/10 | 0.9710 | -0.0290 | 0 (0) | +0.00 | 0.00 | 154.0 |
| Iran leader end of 2026? | augmenté | 30/91 | 0.9700 | -0.0300 | 0 (0) | +0.00 | 0.00 | 154.0 |
| Where will Trump and Putin meet ne | standard | 15/0 | 0.9660 | -0.0340 | 0 (0) | +0.00 | 0.00 | 154.0 |
| How many ships transit Bab el-Mand | standard | 1/5 | 0.9600 | -0.0400 | 0 (0) | +0.00 | 0.02 | -3.0 |
| Maduro Prison Time? | standard | 5/0 | 0.9560 | -0.0440 | 0 (0) | +0.00 | 0.00 | 519.0 |
| How many different countries will  | standard | 8/0 | 0.9530 | -0.0470 | 0 (0) | +0.00 | 0.00 | 154.0 |
| France United Left Primary Winner | augmenté | 6/19 | 0.9470 | -0.0530 | 0 (0) | +0.00 | 0.00 | 73.0 |
| Where will the next next round of  | standard | 16/3 | 0.9360 | -0.0640 | 0 (0) | +0.00 | 0.00 | 63.0 |
| Next leader out of power before 20 | standard | 22/0 | 0.9310 | -0.0690 | 0 (0) | +0.00 | 0.00 | 154.0 |
| How many 7.0 or above earthquakes  | standard | 5/0 | 0.9290 | -0.0710 | 0 (0) | +0.00 | 0.00 | 154.0 |
| Russia Parliamentary Election: 3rd | augmenté | 4/30 | 0.9240 | -0.0760 | 0 (0) | +0.00 | 0.00 | 52.0 |
| Which month will Strait of Hormuz  | standard | 7/0 | 0.9110 | -0.0890 | 0 (0) | +0.00 | 0.00 | 155.0 |
| Next Premier of Quebec | augmenté | 7/22 | 0.9010 | -0.0990 | 0 (0) | +0.00 | 0.00 | 67.0 |
| How many ships transit Bab el-Mand | standard | 4/0 | 0.9010 | -0.0990 | 0 (0) | +0.00 | 0.00 | 4.0 |
| How many different countries will  | standard | 11/1 | 0.8710 | -0.1290 | 0 (0) | +0.00 | 0.00 | 154.0 |
| How many ships transit the Strait  | standard | 5/0 | 0.8630 | -0.1370 | 0 (0) | +0.00 | 0.00 | 4.0 |
| How many seats will United Russia  | standard | 7/0 | 0.8420 | -0.1580 | 0 (0) | +0.00 | 0.00 | 52.0 |
| How many ships transit the Strait  | standard | 4/1 | 0.8380 | -0.1620 | 0 (0) | +0.00 | 0.00 | -3.0 |
| Avg. # of ships transiting Bab el- | standard | 7/0 | 0.8220 | -0.1780 | 0 (0) | +0.00 | 0.00 | 2.0 |
| Number of North Korea Missile Test | standard | 3/0 | 0.4230 | -0.5770 | 0 (0) | +0.00 | 0.00 | 2.0 |

## Cas à Σ bids > 1,00 (revente taker immédiatement > 1 $), issue par issue

_Aucun événement actif sans frais n'a Σ bids > 1,00 au moment du scan._

## Anomalies et réserves

- **Résidu invendable** : les issues sans bid ne se vendent pas en taker ; leur valeur notionnelle est ici la MEILLEURE OFFRE (borne haute). Réserve **sélection adverse** : le résidu vaut en pratique MOINS (on te sert ce qui monte, tu gardes ce qui baisse ; cf. HISTORIQUE-PROJET.md).
- **Capital immobilisé** : la conversion negRisk est à SENS UNIQUE ; le résidu reste bloqué jusqu'à la résolution (colonne échéance).
- **Augmentés** : shortfall de conversion possible ; feeRate du NegRiskAdapter **[non vérifié]** (on-chain).
- **Capacité profonde** : marche de carnet sur les MEILLEURS niveaux successifs des issues vendables ; s'arrête dès qu'une issue vendable s'épuise ou que la Σ marginale passe sous 1,00. Instantané, non rejoué.
- **Frais** : effectifs = 0 confirmés par /fee-rate + feesEnabled [doc officielle] ; sans frais, la revente encaisse Σ bids brut.
