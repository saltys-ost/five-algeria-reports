# 04 — Scan des liquidity rewards

_Généré le 2026-07-28 — lecture seule. Provenance : [mesuré run 4] sauf indication._

## Question

Sur quels marchés binaires le couple « spread capturable + loyer quotidien » est-il le plus favorable, rapporté au capital déjà en compétition et pénalisé par la volatilité ?

## Méthode et formule de score

- Enveloppe **E** = Σ des `rewards_daily_rate` du marché (CLOB `/sampling-markets`), en USD/jour.
- Capital en zone **K** = Σ, sur les jetons YES et NO, des (prix × taille) des ordres à ≤ `max_spread` du milieu, des deux côtés (CLOB `/books`). `max_spread` est en cents (÷100).
- Spread capturable **S** = `ask_YES + ask_NO − 1`.
- Volatilité **V** = amplitude haut-bas du prix YES sur 24 h (CLOB `/prices-history`).
- `rendement_reward = E / (K + 1000)` (le +1000 simule notre arrivée avec 1000 $).
- **`score = (rendement_reward + S) / (1 + 5 × V)`** — la volatilité pénalise multiplicativement.

## Couverture

- Marchés à enveloppe non nulle (binaires actifs, carnet activé) : **8674** [mesuré run 4].
- Échantillon analysé : top 500 par volume 24 h (sur 8674).

## Distribution du rendement enveloppe/capital (E/(K+capital propre))

| tranche | marchés |
|---|---:|
| ≤ 0 | 19 |
| ≤ 0.0001 | 91 |
| ≤ 0.0005 | 64 |
| ≤ 0.001 | 37 |
| ≤ 0.005 | 110 |
| ≤ 0.01 | 39 |
| ≤ 0.05 | 114 |
| > 0.05 | 26 |

## Top 30 par score

| # | marché | cat | E/j | K zone | S | vol24h | rend. | score |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Iran military action against a Gulf State on | Iran | 60 | 0 | 0.154 | 0.098 | 0.0600 | 0.1436 |
| 2 | Will the lowest temperature in Shanghai be 2 | Weather | 288 | 0 | 0.32 | 0.66 | 0.2880 | 0.1414 |
| 3 | Iran military action against a Gulf State on | Iran | 60 | 0 | 0.152 | 0.1005 | 0.0600 | 0.1411 |
| 4 | US x Iran Effective Ceasefire by August 31? | Iran | 250 | 904 | 0.05 | 0.07 | 0.1313 | 0.1343 |
| 5 | Will Starbucks (SBUX) beat quarterly earning | Finance | 5 | 0 | 0.21 | 0.145 | 0.0050 | 0.1246 |
| 6 | Will the next Google Gemini Pro model added  | AI | 50 | 0 | 0.195 | 0.2145 | 0.0500 | 0.1182 |
| 7 | Map Handicap: IMP (-1.5) vs BESTIA (+1.5) | Sports | 150 | 0 | 0.06 | 0.2 | 0.1500 | 0.1050 |
| 8 | Will Trump and Netanyahu not shake hands by  | Politics | 118 | 0 | 0.26 | 0.548 | 0.1180 | 0.1011 |
| 9 | Will MrBeast's next video get between 40 and | MrBeast | 150 | 124 | 0.084 | 0.2375 | 0.1335 | 0.0994 |
| 10 | Will "Spider-Man: Brand New Day" score at le | Movies | 50 | 0 | 0.32 | 0.62 | 0.0500 | 0.0902 |
| 11 | LoL: 9z Globant vs Maze Gaming (BO5) - LRS P | Sports | 253 | 851 | 0.02 | 0.195 | 0.1367 | 0.0793 |
| 12 | Will Arc launch a token by June 30 2027? | Crypto | 5 | 0 | 0.18 | 0.275 | 0.0050 | 0.0779 |
| 13 | Will Trump say "Top Five" or "Top Ten" durin | Politics | 100 | 0 | 0.149 | 0.5145 | 0.1000 | 0.0697 |
| 14 | Israel x Iran ceasefire continues through Au | Iran | 50 | 225 | 0.07 | 0.12 | 0.0408 | 0.0693 |
| 15 | Will monthly inflation increase by 0.1% or m | Inflation | 30 | 0 | 0.1 | 0.185 | 0.0300 | 0.0675 |
| 16 | Counter-Strike: Bounty Hunters Esports vs la | Sports | 337 | 0 | — | 0.7995 | 0.3370 | 0.0674 |
| 17 | LoL: Hyperion vs Francesinhas (BO1) - LPLOL  | Sports | 253 | 0 | — | 0.56 | 0.2530 | 0.0666 |
| 18 | Will MrBeast's next video get less than 40 m | MrBeast | 150 | 401 | 0.035 | 0.235 | 0.1071 | 0.0653 |
| 19 | Will Moonshot be the second-best Code Arena  | AI | 15 | 0 | 0.119 | 0.2325 | 0.0150 | 0.0620 |
| 20 | LoL: paiN Gaming Academy vs Team Solid (BO1) | Sports | 253 | 0 | — | 0.7095 | 0.2530 | 0.0556 |
| 21 | Will the highest temperature in Austin be be | Weather | 110 | 70 | 0.07 | 0.455 | 0.1028 | 0.0527 |
| 22 | Will the lowest temperature in Hong Kong be  | Weather | 12 | 0 | 0.15 | 0.445 | 0.0120 | 0.0502 |
| 23 | Will no qualifying diplomatic US-Iran meetin | Politics | 142 | 1634 | 0.021 | 0.1015 | 0.0539 | 0.0497 |
| 24 | Will the highest temperature in Miami be bet | Weather | 200 | 86 | 0.08 | 0.96 | 0.1841 | 0.0455 |
| 25 | Atlanta Braves vs. Chicago White Sox | Sports | 0.001 | 64902 | 0.05 | 0.02 | 0.0000 | 0.0455 |
| 26 | Will Trump endorse Likud in the 2026 Israeli | Trump | 25 | 1093 | 0.05 | 0.09 | 0.0119 | 0.0427 |
| 27 | US x Iran diplomatic meeting by August 15, 2 | Politics | 100 | 3494 | 0.03 | 0.05 | 0.0222 | 0.0418 |
| 28 | Iran military action against a Gulf State on | Iran | 60 | 612 | 0.02 | 0.075 | 0.0372 | 0.0416 |
| 29 | Will the highest temperature in Seattle be b | Weather | 109 | 41 | 0.05 | 0.545 | 0.1047 | 0.0415 |
| 30 | Will GPT-6 be released by September 30, 2026 | sam altman | 50 | 582 | 0.04 | 0.15 | 0.0316 | 0.0409 |

## Lecture des résultats (mise en garde)

- **16/30** des mieux classés ont une **zone qui score vide** (`capital_in_zone = 0`) : ils montent parce que `E/(K+1000)` n'est dilué par personne — mais une zone vide signale souvent un marché trop peu liquide (carnet large), pas une occasion. Capital en zone médian sur l'échantillon : ~8071 $.
- **17/30** doivent l'essentiel de leur score au **spread capturable S**, pas au loyer : or un S large = un spread large = illiquidité. C'est exactement le biais du run 3 (classer par Σ asks − 1 revient à classer par illiquidité).
- Pistes de lecture plus sûres : filtrer sur une profondeur minimale au meilleur niveau et sur un `capital_in_zone > 0`, puis lire le **loyer par dollar réellement engageable**, pas le S.

## Anomalies rencontrées

- Aucune.

## Réserves

- `max_spread` supposé en cents (valeurs 3–6 typiques) → converti en prix ÷100 ; à confirmer si un marché exotique dérogeait.
- Le capital en zone est un instantané du carnet à l'heure du scan ; il varie dans la journée.
- La volatilité est l'amplitude 24 h ; l'écart-type des variations est aussi dans le CSV (`vol_std_24h`).
- Aucun ordre posé ; ce scan ne mesure pas la probabilité d'exécution (inconnue décisive, cf. reports/00-etat-des-lieux.md).
