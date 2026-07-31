# 10 — Persistance de la performance des meilleurs wallets (copy-trading)

_Étude rétrospective, lecture seule, généré 2026-07-31T19:20:40Z. Provenance : [mesuré run 10]._

**Question.** La performance des meilleurs wallets Polymarket persiste-t-elle d'une période à l'autre, assez pour qu'une stratégie de copie soit envisageable ?

**Méthode.** Pas de leaderboard public (vérifié : `data-api/leaderboard` = 404). On récolte des wallets actifs sur les plus gros marchés résolus de la fenêtre SOURCE, on mesure le profit de chacun **sur les deux fenêtres** via `/activity` (même méthode), puis on gèle un **top** (les mieux classés en fenêtre SOURCE, ≥ 30 trades) et un **témoin** (le reste des candidats actifs, tiré au hasard). Résolution des marchés via CLOB `/markets/<conditionId>` (issue gagnante). Profit d'un marché = flux de trésorerie net des trades + parts de l'issue gagnante × 1. Graine fixe (42), cadence ≤ 3 req/s.

## Réponse chiffrée

| | Top (médiane W2) | Témoin (médiane W2) | ρ rang W1→W2 (top) | Top W2 > 0 |
|---|--:|--:|--:|--:|
| Avec MM | 0 $ | 0 $ | 0.16 | 9/30 |
| Sans MM | 0 $ | -25 $ | 0.15 | 8/21 |

**Persistance (hors market makers) : FAIBLE — le classement ne tient pas.** Corrélation de rang Spearman W1→W2 = **0.15** (0 = aucun lien, 1 = classement identique). Le top garde une médiane W2 de 0 $ contre -25 $ pour le témoin.

## Paire P1 — détail

Marchés source échantillonnés : 6.

- **avec MM** — top : médiane W2 0 $ (moyenne 12 $, 9/30 positifs) ; témoin : médiane W2 0 $ (moyenne 96 $) ; ρ rang W1→W2 = 0.16.
- **sans MM** — top : médiane W2 0 $ (moyenne 23 $, 8/21 positifs) ; témoin : médiane W2 -25 $ (moyenne -14 $) ; ρ rang W1→W2 = 0.15.

## Paire P2 — détail

Marchés source échantillonnés : 6.

- **avec MM** — top : médiane W2 0 $ (moyenne 86 $, 4/13 positifs) ; témoin : médiane W2 0 $ (moyenne 1192 $) ; ρ rang W1→W2 = -0.08.
- **sans MM** — top : médiane W2 0 $ (moyenne 104 $, 4/12 positifs) ; témoin : médiane W2 0 $ (moyenne 1549 $) ; ρ rang W1→W2 = 0.04.

## Les 10 profils les plus persistants (top, hors MM, positifs W1 et W2)

| wallet | style | W1 profit | W2 profit | trades | marchés |
|---|---|--:|--:|--:|--:|
| 0x645a…fd84 | directionnel | 867 $ | 452 $ | 1963 | 74 |
| 0x8457…87fd | directionnel | 112 $ | 1122 $ | 985 | 203 |
| 0x191e…ef6b | directionnel | 1098 $ | 100 $ | 1795 | 359 |
| 0x14ae…bba3 | directionnel | 7 $ | 8 $ | 234 | 12 |
| 0x4da9…3f5d | directionnel | 53 $ | 6 $ | 1181 | 65 |
| 0xdbc4…4347 | directionnel | 3 $ | 165 $ | 1848 | 179 |
| 0xed38…e0b2 | directionnel | 11 $ | 2 $ | 198 | 14 |
| 0xaf15…3b51 | directionnel | 2 $ | 2 $ | 1906 | 133 |

## Limites de la mesure

- **Décalage de copie NON simulé.** On mesure la performance des wallets, pas ce qu'un copieur aurait gagné : on copie les entrées, jamais les sorties (cf. rapport 20 repos). Le rendement réel d'une copie serait **inférieur**.
- **Reconstruction approximative.** Le profit ignore les splits/merges/redeems et les positions ouvertes avant la fenêtre ou fermées après ; une position nette négative (vendu plus qu'acheté dans la fenêtre) fausse le calcul de ce wallet.
- **Sélection par échantillon.** Le top est repéré sur un échantillon de marchés source (pas tout Polymarket) ; la re-mesure via /activity est, elle, complète sur la fenêtre mais plafonnée en pages.
- **Maker/taker indisponible** en public : l'étiquette « market maker probable » est une heuristique (beaucoup de marchés, petits tickets, achat/vente équilibrés).
- **Frais et gas** non déduits ; échantillon et fenêtres courts.

*Données brutes : `data/10_cohorts.csv`, `data/10_performance.csv` (gitignorées).*
