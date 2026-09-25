# VWAP Multi-Jours (glissant) — indicateur TradingView

Script Pine Script v6 qui affiche sur le graphique jusqu'à **4 VWAP glissants**,
chacun calculé sur une fenêtre paramétrable **en jours** (7J, 30J, 90J, 365J...).

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
| Général | Masquer tant que l'historique ne couvre pas la fenêtre | Cache la ligne tant que le graphique n'a pas au moins N jours de données. |
| Général | Afficher les étiquettes | Affiche « VWAP 7J  12345.6 » à droite de chaque ligne. |
| Général | Décalage / Épaisseur | Mise en forme. |
| VWAP 1 à 4 | Activer | Affiche ou masque cette ligne. |
| VWAP 1 à 4 | **Jours** | **Longueur de la fenêtre en jours calendaires** (1 à 3650). |
| VWAP 1 à 4 | Couleur | Couleur de la ligne. |

Valeurs par défaut : 7J (activé), 30J (activé), 90J (désactivé), 365J (activé).
Pour un autre horizon (14J, 180J, 2 ans = 730J...), il suffit de modifier le
champ « Jours » du slot voulu.

## Méthode de calcul

Pour une fenêtre de N jours :

```
VWAP(N) = Σ(prix × volume) / Σ(volume)
```

sur toutes les bougies dont l'heure d'ouverture est dans les N derniers jours
(fenêtre basée sur le temps, pas sur un nombre de bougies).

Conséquences pratiques :

- Le résultat est cohérent quelle que soit l'unité de temps du graphique
  (1 min, 1 h, 1 D...). Plus l'unité de temps est fine, plus le VWAP est précis.
- Les marchés 24/7 (crypto) et les marchés avec week-ends (actions) sont gérés
  sans réglage particulier.
- Le script conserve des sommes cumulées et un pointeur qui n'avance que vers
  l'avant, donc un VWAP 365J sur un graphique en 1 minute reste rapide.

## Limites

- TradingView ne charge qu'un nombre limité de bougies par graphique
  (environ 20 000, davantage avec un abonnement Premium). Sur un graphique en
  1 minute, 20 000 bougies ≈ 14 jours pour un marché 24/7 : un VWAP 365J n'y
  aura pas assez d'historique et restera masqué (option « Masquer... »
  activée) ou équivaudra à un VWAP depuis le début des données (option
  désactivée). Utiliser une unité de temps plus large (1 h, 4 h, 1 D) pour les
  longues fenêtres.
- Les symboles sans volume (certains indices, forex selon le courtier) ne
  permettent pas de calculer un VWAP : un avertissement rouge s'affiche.
