# 00 — État des lieux

Synthèse de départ du dossier, d'après `docs/HISTORIQUE-PROJET.md` (arrêté au
28 juillet 2026). En cas de contradiction, **`CLAUDE.md` et `docs/ERRATA.md`
font autorité** sur les autres documents de `docs/`.

Chaque chiffre porte sa provenance : `[mesuré run N]`, `[doc officielle]`,
`[correction pilote]`, `[calculé]`, `[hypothèse]`.

---

## Mesuré

- **Univers (run 1, Gamma)** — 12 139 événements actifs, 4 476 negRisk, dont
  99,4 % avec frais activés et 28 % « augmented ». `[mesuré run 1]`
  Le croisement espéré « negRisk × sans frais » **n'existe pas** (26 événements).
  Les marchés à 128 issues n'ont qu'~15 issues significatives, le reste = poussières.
- **Carnets (run 2, CLOB, 200 événements stratifiés, 3 511 issues)** —
  **53 % des issues n'ont pas de carnet bilatéral** : c'est le fait structurel
  du projet. `[mesuré run 2]`
  - Hypothèse « déviation Gamma = carnets vides » **réfutée** (4,8 vs 5,5
    vides/événement entre strates far/close).
  - Là où un carnet existe, prix Gamma = milieu CLOB (écart médian 0,0000).
    La péremption de Gamma est une **absence** de prix, pas un prix décalé.
  - Σ asks > 1 partout (c'est le spread cumulé, pas une opportunité), min 1,03.
  - 9/200 événements avec Σ bids > 1, mais tués par les frais taker hors
    catégorie sans frais.
- **Persistance (run 3, suivi 2 h de 20 paniers)** — Σ asks jamais < 1,00 sur
  la fenêtre. `[mesuré run 3, biaisé]`
  **Réserve :** la sélection des 20 paniers était biaisée — classée par Σ asks−1,
  qui est une somme de spreads, donc un tri par **illiquidité**. La bonne
  métrique retenue est le **spread moyen par issue = (Σ asks − 1) / nb d'issues
  cotées**. `[correction pilote]`

*(Données brutes correspondantes dans `data/` — gitignorées.)*

---

## Ouvert (et décisif)

- **Probabilité d'exécution d'un ordre maker** — jamais approchée ; ne se mesure
  qu'en **posant de vrais ordres**. C'est l'inconnue qui bloque l'évaluation de
  presque toutes les stratégies. `[hypothèse — H2/H3 dans docs/hypotheses-a-mesurer.md]`
- **Enveloppe de liquidity rewards par marché ÷ capital déjà en compétition**
  dans la zone qui score — **mesurable en lecture seule** (c'est l'objet du run 4).
- **Stratégies non chiffrées avec données réelles** (statuts corrigés par
  l'ERRATA ; les « éliminations » antérieures étaient sans fondement) :
  - **A / B / D** : entrée au carnet (taker / maker / mixte) → sortie **merge**
    (garantie, rend 1,00 $ immédiatement — l'objection du capital immobilisé
    tombe). A et B sont la **même** stratégie, deux rôles d'exécution.
  - **C4** : inventaire negRisk acquis par split+convert (garanti, gratuit si
    univers complet) → **market making** multi-issues en sortie maker (zéro
    frais). Rouverte ; la plus prometteuse selon l'historique. Rappel : ce n'est
    **pas** un arbitrage — sélection adverse sur le résidu à la sortie.
  - **F** : split 1 $ → poster **les deux** ventes maker (YES et NO) au-dessus
    du milieu. Neutre si 0 ou 2 exécutions ; pari directionnel (~24:1) si une
    seule → n'a de sens qu'avec les deux jambes.
  - **G** : F posée sur des marchés à liquidity rewards → loyer quotidien.
    **À étudier en premier** : seule stratégie dont le revenu ne dépend **pas**
    de la probabilité d'exécution (payée pour la présence, exécuté ou non).
  - **H** : incohérences logiques entre marchés — en attente.
  - **E** : écartée à la demande du pilote (veut de l'automatique).

---

## Prochaine étape

- **Run 4 — scan des liquidity rewards** (`scripts/04_…`), en lecture seule :
  pour chaque marché à rewards, mesurer l'enveloppe quotidienne, `max_spread`,
  `min_size`, et le capital déjà présent dans la zone qui score, afin d'estimer
  le rendement de la présence (levier de la stratégie G). `[d'après HISTORIQUE-PROJET.md]`

## Garde-fous permanents (rappel CLAUDE.md)

Lecture seule, aucune clé, aucun ordre posé à ce stade — aucun n'a jamais été
posé, aucun capital engagé. Vérifier les noms de champs en direct, cadence
≤ 3 req/s, échantillonnage à graine fixe, tout chiffre porte sa provenance.
