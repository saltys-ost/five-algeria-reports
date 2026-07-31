# 06 — Fenêtres d'arbitrage (WebSocket temps réel)

_Couverture cumulée ~4.17 h sur 30 tranches (cible 4 h). Trous de suspension entre tranches acceptés et visibles dans les horodatages. Provenance [mesuré run 6] sauf indication. Frais : feeRateBps RÉEL par marché (/fee-rate), formule officielle fee = C×(bps/10000)×p×(1−p) [doc officielle]._

## Fenêtres A (sumAsk < 1,00) par strate

| strate | marchés | fenêtres | fenêtres NETTES | fen./h | avec trade tiers |
|---|--:|--:|--:|--:|--:|
| geo_no_fee | 15 | 34 | 34 | 8.16 | 0 |
| crypto_short | 15 | 7 | 3 | 1.68 | 0 |
| big_volume | 15 | 50 | 8 | 11.99 | 0 |

**Total : 91 fenêtres A détectées, dont 45 NETTES (profit après frais > 0).**

## Distribution des durées des fenêtres (ms)

- -inf … 50 ms : 91
- 50 … 100 ms : 0
- 100 … 250 ms : 0
- 250 … 500 ms : 0
- 500 … 1000 ms : 0
- 1000 … 5000 ms : 0
- 5000 … 30000 ms : 0
- > 30000 ms : 0

## Distribution du net après frais (par paire, $)

- -inf … -0.05 $ : 0
- -0.05 … -0.01 $ : 32
- -0.01 … 0 $ : 14
- 0 … 0.005 $ : 23
- 0.005 … 0.01 $ : 11
- 0.01 … 0.02 $ : 8
- 0.02 … 0.05 $ : 1
- > 0.05 $ : 2

- net/paire médian : -0.0002 $ ; max : +0.2075 $.

## Profondeur capturable

- Profondeur médiane au min (min des deux asks) : **17.05 $** par fenêtre ; max 3544 $.
- Net total capturable médian sur les fenêtres NETTES : **+0.15 $**.

## Un tiers a-t-il pris la fenêtre ?

- 0/91 fenêtres (0 %) ont vu ≥ 1 `last_trade_price` pendant leur durée.

## Espace maker sous 1 : distribution de 1 − sumBid par strate

| strate | échantillons | médiane(1−sumBid) | p90 | max |
|---|--:|--:|--:|--:|
| geo_no_fee | 20234 | 0.0100 | 0.0190 | 0.0900 |
| crypto_short | 9492 | 0.0100 | 0.0500 | 0.3300 |
| big_volume | 5780 | 0.0010 | 0.0100 | 0.6910 |

_1 − sumBid > 0 = marge pour poster deux achats maker sous 1 (avant probabilité d'exécution, inconnue non mesurée ici)._

## Couverture, anomalies, réserves

- Couverture cumulée : 4.17 h en 30 tranches (WebSocket continu par tranche ; coupures entre tranches = suspensions du conteneur, acceptées).
- Le carnet local est reconstruit par snapshots `book` + deltas `price_change` ; un message manqué est corrigé au `book` suivant.
- La profondeur capturable est celle des MEILLEURS niveaux au moment du min ; elle ignore la profondeur aux niveaux suivants (borne basse).
- Frais [doc officielle] : part en frais des achats taker ; le net suppose l'achat des deux jambes en taker puis merge (rend 1,00 $, cf. ERRATA).
- Non mesuré : la probabilité d'exécution d'un ordre maker (stratégie B) — inconnue décisive, cf. reports/00-etat-des-lieux.md.
