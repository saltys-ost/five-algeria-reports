# VWAP Multi-Jours (glissant) — indicateur TradingView

Script Pine Script v6 qui affiche sur le graphique jusqu'à **4 VWAP glissants**,
chacun calculé sur une fenêtre paramétrable **en jours** (7J, 30J, 90J, 365J...),
**quelle que soit l'unité de temps du graphique** (M1, M5, H1, D...).

Fichier : [`vwap_multi_jours.pine`](./vwap_multi_jours.pine)

## Installation

1. Ouvrir un graphique sur TradingView.
2. En bas de l'écran, ouvrir l'onglet **Éditeur Pine**.
3. Supprimer le contenu par défaut, coller l'intégralité de `vwap_multi_jours.pine`.
4. Cliquer sur **Ajouter au graphique** (et **Enregistrer** pour le retrouver dans « Mes scripts »).

## Paramètres

Ouvrir les réglages de l'indicateur (roue crantée) :

| Groupe | Paramètre | Rôle |
|---|---|---|
| Général | Source du prix | Prix pondéré par le volume (`hlc3` par défaut, standard du VWAP). |
| Général | Masquer tant que l'historique ne couvre pas la fenêtre | Cache la ligne tant que l'UT de calcul n'a pas au moins N jours de données. |
| Général | Afficher les étiquettes | Affiche « VWAP 7J  12345.6 » à droite de chaque ligne. |
| Général | Décalage / Épaisseur | Mise en forme. |
| VWAP 1 à 4 | Activer | Affiche ou masque cette ligne. |
| VWAP 1 à 4 | **Jours** | **Longueur de la fenêtre en jours calendaires** (1 à 3650). |
| VWAP 1 à 4 | Couleur | Couleur de la ligne. |
| VWAP 1 à 4 | **UT de calcul** | Unité de temps sur laquelle le VWAP est calculé (voir ci-dessous). |

Valeurs par défaut :

| Slot | Jours | UT de calcul | Activé |
|---|---|---|---|
| VWAP 1 | 7J | 15 min | oui |
| VWAP 2 | 30J | 1 h | oui |
| VWAP 3 | 90J | 4 h | non |
| VWAP 4 | 365J | 1D | oui |

Pour un autre horizon (14J, 180J, 2 ans = 730J...), il suffit de modifier le
champ « Jours » du slot voulu et, si besoin, son UT de calcul.

## Pourquoi une « UT de calcul » ? (exemple : VWAP 365J sur un graphique M5)

TradingView ne charge qu'un nombre limité de bougies par graphique (environ
20 000, davantage avec un abonnement Premium). Sur un graphique M5 :

- marché 24/7 (crypto) : 20 000 bougies M5 ≈ 69 jours ;
- actions (≈ 78 bougies M5 par séance) : ≈ 256 séances, soit environ un an.

Un VWAP 365J calculé directement sur les bougies M5 n'aurait donc pas assez
d'historique. Le script calcule chaque VWAP sur l'UT que vous choisissez
(par exemple 1D, dont l'historique couvre plusieurs années) puis reporte la
valeur sur le graphique courant. Sur un graphique M5, le VWAP 365J est ainsi
visible et se met à jour au fil de la journée.

Règle simple pour choisir l'UT de calcul :

| Fenêtre | UT de calcul conseillée |
|---|---|
| 1 à 3 jours | celle du graphique (laisser vide) ou 5 min |
| 7 jours | 15 min ou 1 h |
| 30 jours | 1 h |
| 90 jours | 4 h |
| 365 jours et plus | 1D |

Plus l'UT de calcul est fine, plus le VWAP est précis et réactif ; plus elle
est large, plus l'historique disponible est long. Si l'UT de calcul est plus
petite que celle du graphique (par exemple 15 min sur un graphique 1D), le
script utilise automatiquement l'UT du graphique.

## Méthode de calcul

Pour une fenêtre de N jours :

```
VWAP(N) = Σ(prix × volume) / Σ(volume)
```

sur toutes les bougies de l'UT de calcul dont l'heure d'ouverture est dans les
N derniers jours (fenêtre basée sur le temps, pas sur un nombre de bougies).

Conséquences pratiques :

- Les marchés 24/7 (crypto) et les marchés avec week-ends (actions) sont gérés
  sans réglage particulier.
- Le script conserve des sommes cumulées et un pointeur qui n'avance que vers
  l'avant, donc le calcul reste rapide même sur de longues fenêtres.

## Limites

- Sur les bougies historiques, la valeur reportée depuis une UT supérieure est
  celle de la clôture de la bougie de l'UT de calcul (comportement standard de
  `request.security`). En temps réel, la valeur évolue au fil de la bougie en
  cours. Une ligne calculée en 1D apparaît donc en « escalier » sur un
  graphique intraday.
- Les symboles sans volume (certains indices, forex selon le courtier) ne
  permettent pas de calculer un VWAP : un avertissement rouge s'affiche.
