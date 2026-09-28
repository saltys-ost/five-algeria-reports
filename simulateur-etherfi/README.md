# Simulateur de rentabilité ether.fi Cash

Application locale (un seul fichier `index.html`) qui simule sur 36 ou 48 mois si payer ses dépenses avec la carte ether.fi Cash — en Direct Pay (routes B1, B2, C) ou en Borrow sur collatéral (route D) — rapporte plus qu'une carte bancaire classique (route A), avec cashback en ETHFI, intérêts, rendement du collatéral, risque de liquidation, scénarios fixes et Monte Carlo.

## Lancer l'app (une commande)

```bash
cd simulateur-etherfi && python3 -m http.server 8080
```

puis ouvrez http://localhost:8080 dans votre navigateur. (Un double-clic sur `index.html` fonctionne aussi : les données sont embarquées dans `data/bundle.js`.)

Pour rafraîchir les historiques de prix (à faire une fois, puis quand vous voulez) :

```bash
python3 scripts/telecharger_prix.py
```

Le script lit des sources publiques gratuites sans clé (Kraken, Nasdaq, CoinGecko ; Stooq et Yahoo en repli), écrit `data/prix/<actif>.csv` et régénère `data/bundle.js`. La page HTML n'appelle **jamais** une API.

## Mode d'emploi en 5 lignes

1. Réglez dans la colonne de gauche vos dépenses, votre capital, l'horizon, le mode de remboursement, la répartition du collatéral et le scénario ; les résultats se recalculent tout seuls.
2. Onglet **Résultats** : tableau des 4 routes (frais, intérêts, cashback nominal et net, yield, liquidation, gain net vs carte bancaire), verdict en une phrase, graphiques LTV et dette/collatéral.
3. Onglet **Seuils & grille** : capital nécessaire pour une dépense donnée (Sens 1), dépense soutenable pour un capital (Sens 2), grille de rentabilité colorée (Sens 3), point mort cashback vs intérêts (Sens 4), collatéral minimal en scénario Bear.
4. Onglet **Monte Carlo** : 10 000 trajectoires avec μ/σ historiques (onglet **Statistiques**), probabilité de liquidation, distribution P5–P95, éventail, histogramme, comparaison par actif.
5. Onglet **Données** : chaque paramètre avec sa pastille (CONFIRMÉ / VÉRIFIÉ / DÉFAUT / INCONNU), sa source et sa date ; bouton **Mettre à jour les données** (interrogatoire bloc par bloc), téléchargement du `parametres.json` rempli, bouton **Réinitialiser aux valeurs vérifiées sept. 2026**, export CSV des résultats.

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | l'application (HTML + CSS + JS, Chart.js via CDN avec repli local `lib/`) |
| `data/parametres.json` | tous les paramètres : valeur, unité, source, date, statut, bloc, où trouver, note |
| `data/FICHE_DONNEES.md` | le même tableau, lisible, généré par `scripts/generer_fiche.py` |
| `data/VERIFICATIONS.md` | vérifications publiques V1 → V11 (URL, date, résultat, confiance) |
| `data/QUESTIONS_SUPPORT.md` | questions prêtes à coller dans le chat du support ether.fi |
| `data/prix/*.csv` | historiques de prix quotidiens (source et fréquence par ligne) |
| `data/bundle.js` | paramètres + prix regroupés pour la page (généré, ne pas éditer) |
| `scripts/telecharger_prix.py` | téléchargement des prix (lecture seule) |
| `scripts/generer_bundle.py` | régénère `data/bundle.js` après une modification de `parametres.json` |
| `scripts/generer_fiche.py` | régénère `data/FICHE_DONNEES.md` |

## Rendre vos réponses permanentes

Vos réponses dans « Mettre à jour les données » sont gardées dans le navigateur (localStorage). Pour les figer dans le projet : bouton **Télécharger parametres.json**, remplacez `data/parametres.json` par le fichier téléchargé, puis lancez `python3 scripts/generer_bundle.py && python3 scripts/generer_fiche.py`.

## Test du moteur de liquidation

L'onglet **Aide & schémas** rejoue l'exemple officiel weETH (10 000 $ de collatéral, 5 500 $ empruntés) : chute de 30 % → liquidation partielle, chute de 35 % → liquidation totale. Le résultat du test est affiché (et écrit dans la console du navigateur).

## Contrôle cashback à faire (cahier des charges 2.5)

Exportez l'historique complet de vos transactions (app > Transactions > export ; help center « How to download your card transaction history »), puis donnez-moi le fichier : je recalculerai le cumul en USD au taux oracle au moment de la bascule 3 % → 1 % du 20/09/2026 et, si l'écart avec les 800 $ persiste, la question Q7 de `QUESTIONS_SUPPORT.md` est prête.
