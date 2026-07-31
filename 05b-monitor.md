# 05b — Suivi 24 h de la shortlist rewards + scoring officiel

_Début 2026-07-29T07:06:16.835053+00:00 — 24 relevés, fenêtre couverte ~24.1 h (cible 24 h). Lecture seule ; les trous de suspension du conteneur sont acceptés et visibles dans la colonne `elapsed_h` de data/05_monitor_timeseries.csv. Provenance [mesuré run 5]._

## Suivi par marché

| marché | E/j | K instant | K moy | K min | K max | pic (t+h) | S moy | S min–max | vide 1 côté | rend. K-instant | rend. K-moy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| US x Iran Effective Ceasefire by A | 250 | 904 | 13213 | 1987 | 32288 | 21.5 | 0.018 | 0.010–0.030 | non | 0.1313 | 0.0176 |
| Will no qualifying diplomatic US-I | 142 | 1634 | 15924 | 9099 | 28357 | 13.6 | 0.004 | 0.001–0.018 | non | 0.0539 | 0.0084 |
| Iran military action against a Gul | 60 | 612 | 1098 | 0 | 4218 | 7.2 | 0.059 | 0.010–0.180 | non | 0.0372 | 0.0286 |
| Will GPT-6 be released by Septembe | 50 | 582 | 2968 | 665 | 4146 | 7.2 | 0.017 | 0.010–0.030 | non | 0.0316 | 0.0126 |
| US x Iran Effective Ceasefire by A | 200 | 5543 | 12608 | 3252 | 26866 | 21.5 | 0.013 | 0.010–0.030 | non | 0.0306 | 0.0147 |
| Israel x Iran ceasefire continues  | 200 | 5624 | 8482 | 3842 | 13849 | 4.1 | 0.013 | 0.010–0.020 | non | 0.0302 | 0.0211 |
| Israel x Iran ceasefire continues  | 100 | 2385 | 8938 | 1529 | 21463 | 6.2 | 0.014 | 0.010–0.030 | non | 0.0295 | 0.0101 |
| Iran full airspace closure by Augu | 100 | 2545 | 6891 | 2674 | 12517 | 23.6 | 0.017 | 0.010–0.030 | non | 0.0282 | 0.0127 |
| Will the highest temperature in Se | 28 | 216 | 0 | 0 | 0 | 0.0 | — | — | OUI | 0.0230 | 0.0280 |
| US x Iran diplomatic meeting by Au | 100 | 3494 | 10044 | 6224 | 21348 | 24.1 | 0.015 | 0.010–0.030 | non | 0.0222 | 0.0091 |
| Will the highest temperature in Ho | 93 | 3187 | 705 | 0 | 4301 | 7.2 | 0.012 | 0.002–0.030 | OUI | 0.0222 | 0.0545 |
| Will the highest temperature in Sh | 171 | 6718 | 153 | 0 | 1851 | 0.0 | 0.020 | 0.010–0.030 | OUI | 0.0222 | 0.1483 |
| US x Iran diplomatic meeting by Au | 300 | 13678 | 18270 | 2916 | 35569 | 3.1 | 0.017 | 0.010–0.030 | non | 0.0204 | 0.0156 |
| Will Shohei Ohtani win the 2026 Na | 113 | 4616 | 26849 | 10133 | 50765 | 3.1 | 0.010 | 0.010–0.010 | non | 0.0201 | 0.0041 |
| Will the highest temperature in Je | 105 | 4484 | 38 | 0 | 587 | 0.0 | 0.040 | 0.020–0.070 | OUI | 0.0191 | 0.1012 |

## Scoring officiel des liquidity rewards et non-proportionnalité au capital

Formule transcrite de la doc officielle Polymarket (market-makers/liquidity-rewards),
lue le 2026-07-28. Chaque élément porte `[doc officielle]`.

**Score d'un ordre** `[doc officielle]`
Pour un ordre à une distance `s` (spread, en cents) du milieu ajusté, avec le
`max_spread` du marché `v` (cents) :

    S(s) = ((v − s) / v)²          (nul si s > v), puis pondéré par la taille de l'ordre.

Le score d'un côté agrège ces contributions sur le marché `m` et son complément `m'` :
`[doc officielle]`

    Q_one = Σ scored(bids sur m)  +  Σ scored(asks sur m')
    Q_two = Σ scored(asks sur m)  +  Σ scored(bids sur m')

**Règle de bilatéralité (Q_min)** `[doc officielle]`
- Milieu dans [0.10, 0.90] : `Q_min = max( min(Q_one, Q_two),  max(Q_one, Q_two) / c )`, avec `c = 3`.
- Milieu hors [0.10, 0.90] : `Q_min = min(Q_one, Q_two)` — la liquidité doit être
  **bilatérale** pour scorer (un seul côté donne 0).

**Part de récompense** `[doc officielle]`
Le carnet est échantillonné très fréquemment (≈ à la minute). À chaque échantillon,
le `Q_min` du maker est normalisé par la somme des `Q_min` de tous les makers en
compétition, puis cumulé sur l'epoch :

    Q_final = Σ_échantillons ( Q_min_maker / Σ_makers Q_min )
    récompense = Q_final × (pool quotidien du marché)      (payout minimum 1 $)

### Pourquoi la part n'est PAS proportionnelle au capital posé

1. **Quadratique en distance** `[doc officielle]` — `((v−s)/v)²` : un dollar posté
   près du milieu vaut beaucoup plus qu'un dollar au bord de `max_spread`. Le score
   n'est linéaire en taille qu'à distance fixe ; déplacer le capital vers le milieu
   le fait croître **quadratiquement**. Donc « rendement par dollar » dépend d'*où*
   on poste, pas seulement de *combien*.
2. **Q_min bilatéral** `[doc officielle]` — le score est plafonné par le côté le plus
   faible (`min(Q_one,Q_two)`, ou `max(.)/3`). Empiler du capital sur un seul côté
   ne rapporte rien au-delà de l'équilibre ; hors [0.10,0.90], un seul côté = 0.
3. **Seuil `min_size` / `Qmin` de qualification** `[doc officielle]` — un ordre sous
   la taille minimale du marché ne score pas : il n'y a pas de proportionnalité depuis
   zéro, mais un plancher.
4. **Normalisation par la concurrence** `[doc officielle]` — la part est
   `Q_min / Σ Q_min` : elle **décroît quand les autres makers ajoutent du capital**.
   C'est exactement pourquoi le run 5 mesure le rendement avec `K` (capital déjà en
   zone) et compare le rendement « borne-haute » (K instantané) à celui basé sur le
   `K` moyen sur 24 h : notre part réelle est diluée par ce K, pas fixée par notre
   seul apport.

