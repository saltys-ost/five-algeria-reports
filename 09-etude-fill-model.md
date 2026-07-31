# 09 — Étude de code : modèle de fill, score de réplication, référence d'exécution

Étude **en lecture seule** de deux dépôts (`ent0n29/polybot` et
`caiovicentino/polymarket-mcp-server`), clonés en isolé, **aucun code exécuté**. Objectif :
en tirer ce qui sert directement notre palier 1 et notre bot v1. Écrit en langage simple.

Provenance : tout ce qui suit est `[lu dans le code]` (pas mesuré). Les fichiers cités :
`polybot/research/calibrate_maker_fill_model.py`, `polybot/research/replication_score.py`,
`polymarket-mcp-server/src/polymarket_mcp/auth/{signer,client}.py` et `.../config.py`
(+ `utils/safety_limits.py`, `tools/trading.py` pour l'application des garde-fous).

---

# A. Le modèle de fill (`calibrate_maker_fill_model.py`)

**À quoi il sert.** Estimer la **probabilité qu'un ordre maker soit exécuté** — exactement
l'inconnue décisive du projet (H2). Le script calibre ce chiffre à partir des ordres que le bot
a **réellement posés** et de ce qui leur est arrivé.

## A.1 Les variables utilisées

Le modèle repose sur **une seule variable explicative** :

- **la distance au meilleur achat, en « ticks »** — `ticks_above_best_bid = (prix posé −
  meilleur bid au moment de la pose) ÷ taille du tick`. C'est un **proxy de la place dans la
  file d'attente** : plus on pose près (ou au-dessus) du meilleur bid, mieux on est servi.

Il ne considère que des ordres **maker à l'achat placés dans le spread** (`best_bid ≤ prix <
best_ask`). Il enregistre aussi, sans les mettre dans le modèle : prix posé, taille, meilleur
bid/ask à la pose, taille du tick, l'instant du 1er fill, la taille du 1er fill, la taille
demandée.

**Ce qu'il n'utilise PAS** (et qui pourrait compter) : la **profondeur devant** (combien de
parts sont déjà en file au même prix), la **volatilité**, l'**heure**, la **taille** de l'ordre,
l'**identité du marché**. C'est une simplification assumée.

## A.2 La forme du modèle et sa calibration

- **Modèle géométrique « par sondage ».** On imagine que, à chaque coup d'œil au carnet (un
  « poll », par défaut toutes les **250 ms**), l'ordre a une probabilité `p` d'être exécuté.
  À partir de la **latence médiane** du premier fill, on remonte à `p` :
  `p = 1 − 0,5^(1/n)` où `n = latence médiane ÷ 250 ms`.
- **Effet de la distance.** Pour chaque « bucket » de distance `k` (en ticks), on calcule un
  `p`. Puis on ajuste une droite sur `log(p)` : cela donne `p(k) = p0 × mult^k` —
  `p0` = probabilité de base au meilleur bid, `mult` = multiplicateur par tick gagné.
- **Fraction exécutée.** En bonus, il estime la part typiquement remplie au premier fill
  (`taille du 1er fill ÷ taille demandée`) — pour modéliser les exécutions **partielles**.
- **Données & période.** Il lit **ses propres** relevés dans une base ClickHouse
  (`strategy_gabagool_orders` = poses, `executor_order_status` = fills), sur une **fenêtre
  glissante de 24 h** par défaut (ou un intervalle précis), avec un minimum de **50 échantillons
  par bucket** de distance. Le résultat sort sous forme de réglages `executor.sim`.

En clair : **on pose des ordres, on note ce qui arrive, on en déduit une probabilité de fill
en fonction de la distance au marché.** C'est précisément la démarche « enregistrer nos propres
ordres pour calibrer ».

## A.3 Tableau de relevé prêt à l'emploi (une ligne par ordre posé)

Pour calibrer **le même type de modèle** sur nos cycles manuels — et **en mieux** (voir A.4) —
il faut noter, pour **chaque** ordre posé, les colonnes suivantes. Une ligne = un ordre.

| Colonne | Ce qu'on écrit | Pourquoi |
|---|---|---|
| `id_ordre` | identifiant unique (ou n° de ligne) | relier pose et exécution |
| `horodatage_pose` | date-heure à la milliseconde | base de la latence |
| `marche` | titre court du marché | contexte, filtrage |
| `token` | jeton + issue (YES / NO) | identifier la jambe |
| `cote` | BUY ou SELL | le modèle du repo ne gère que BUY ; on veut les deux |
| `prix_pose` | prix de l'ordre | — |
| `taille_posee` | nombre de parts demandé | dénominateur du fill partiel |
| `tick_size` | pas de prix du marché | pour calculer la distance en ticks |
| `best_bid_pose` | meilleur achat à l'instant de la pose | distance & contexte |
| `best_ask_pose` | meilleure offre à l'instant de la pose | spread & contexte |
| `profondeur_devant` | parts déjà en file au même prix | **vraie** priorité de file (le repo l'ignore) |
| `volatilite_5min` | écart-type du milieu sur 5 min avant la pose | tester si la volatilité compte |
| `horodatage_1er_fill` | date-heure du 1er fill, **ou vide si jamais exécuté** | latence **et** non-fills |
| `taille_1er_fill` | parts exécutées au 1er fill | fraction remplie |
| `taille_totale_exec` | parts exécutées en tout (fin de vie de l'ordre) | fill complet vs partiel |
| `horodatage_fin` | instant d'annulation / expiration / complétion | durée de vie |
| `statut_final` | EXÉCUTÉ / PARTIEL / ANNULÉ / EXPIRÉ / **NON_EXÉCUTÉ** | **corrige le biais du repo** |
| `note` | événement de marché (news, gros trade…) | expliquer les cas extrêmes |

*(La distance en ticks et la latence se recalculent depuis ces colonnes — pas besoin de les
saisir.)*

## A.4 Limites et hypothèses discutables (repérées dans le code)

1. **Biais de survie — le plus grave.** Le script ne regarde **que les ordres qui ont été
   exécutés** (jointure interne sur les fills). Les ordres **jamais servis sont exclus**. Il
   mesure donc « à quelle vitesse, **sachant que** ça a fini par remplir », pas « quelle est la
   probabilité de remplir ». Pour nous, c'est justement le taux de non-fill qui compte → notre
   tableau **note tous les ordres, exécutés ou non** (colonne `statut_final`).
2. **Hypothèse « sans mémoire ».** Le modèle géométrique suppose une probabilité constante à
   chaque poll. En vrai, les fills arrivent **par à-coups** (un gros trade balaie le niveau).
3. **Médiane seulement.** Il n'utilise que la latence médiane par bucket → il jette la forme de
   la distribution (une moyenne cache les cas lents).
4. **Une seule variable.** Ignore profondeur devant, volatilité, taille, heure, marché. La
   distance en ticks est un **proxy** de la file, pas la vraie position dans la file.
5. **Dépendant de la cadence de poll.** Le `p` par poll dépend du rythme d'observation (250 ms) —
   ce n'est pas une propriété du marché seul.
6. **Ajustement fragile.** `p(k) = p0·mult^k` peut dépasser 1 ou être instable avec peu de
   buckets.

**Conclusion A :** la méthode est la bonne (calibrer sur nos propres ordres), mais on doit
**enregistrer aussi les non-fills** et, si possible, la **profondeur devant** — deux choses que
le repo laisse de côté.

---

# B. Le score de réplication (`replication_score.py`)

**Ce que c'est vraiment.** Ce n'est **pas** un juge de rentabilité. C'est une mesure de
**ressemblance de style** entre un candidat (notre bot) et un trader cible : « est-ce que je
trade **comme** lui ? ». Le code le dit lui-même : les fills publics n'exposent ni les
annulations ni les cotations, donc ce n'est qu'un **contrôle rapide des écarts évidents**.

## B.1 Les critères comparés

Il compare la **distribution** des trades des deux, via une distance simple (L1), sur :

- **le mix de marchés** (types : BTC 15 min, BTC 1 h, ETH…) ;
- **le mix d'issues** (part YES / NO) ;
- **le mix d'exécution** (maker / taker — quand la donnée `ws_exec_type` existe) ;
- **la distribution des tailles** (top 15 tailles) ;
- **le timing** (secondes avant la fin, par tranches de 5 min) — calculé mais **hors du score
  final**.

Le score final = moyenne des écarts, ramenée sur 0–100 (plus haut = plus proche).

## B.2 Ce qui est réutilisable pour notre run 10 (copy-trading)

- **Les variables de STYLE** sont exactement celles qui séparent un **market maker** d'un
  **directionnel** : la **part maker/taker** (un MM est massivement maker → **non copiable**), la
  **fréquence** de trades, la **taille médiane**, le **nombre de marchés distincts**. → on
  reprend ces axes pour l'**étiquetage** « MM probable vs directionnel » du run 10.
- **L'outil de distance de distribution** servira **après** coup, pour vérifier qu'on copie
  vraiment le style visé (contrôle qualité de la copie).
- **Ce qu'il ne donne PAS**, et qu'il faut mesurer à part (cœur du run 10) : la **persistance de
  la performance** (le trader reste-t-il bon d'une période à l'autre ?) et la **profitabilité**.
  Le style se ressemble ; ça ne dit rien du gain.

*(Détail technique : le fichier lit une base ClickHouse et a un petit défaut d'import — sans
importance, on ne l'exécute pas ; on en reprend la logique, pas le code.)*

---

# C. Référence d'exécution (`polymarket-mcp-server`)

## C.1 L'authentification et la signature, en une direction

```
   CLÉ PRIVÉE (L1)  ─ prouve que je possède le wallet
        │
        │  signe un message texte « I control this wallet\n{nonce} »
        ▼
   SERVEUR CLOB  ─ délivre des identifiants L2 : api_key + api_secret + passphrase
        │
        │  (ces identifiants se créent UNE fois, puis se réutilisent)
        ▼
   REQUÊTES AUTHENTIFIÉES (L2)  ─ chaque appel (poster / annuler / lire ses ordres,
        │                          positions, solde) est signé en HMAC avec l'api_secret
        ▼
   POSER UN ORDRE
        │  1. construire l'ordre : salt, maker, signer, taker, tokenId,
        │     makerAmount, takerAmount, expiration, nonce, feeRateBps, side, signatureType
        │  2. signer en EIP-712 (données typées) avec la clé privée
        │  3. envoyer au CLOB (type GTC / FOK / GTD)
        ▼
   ORDRE AU CARNET
```

Deux niveaux, donc : **L1** = la clé privée prouve la propriété du wallet et signe chaque
**ordre** ; **L2** = des identifiants dérivés (api_key/secret/passphrase) signent chaque
**requête HTTP**. Trois types de signataire existent (`signatureType`) : **EOA** (0, wallet
simple), **Proxy Polymarket** (1), **Gnosis Safe** (2) — important car les wallets Polymarket
web sont souvent des proxys, pas des EOA.

## C.2 Les garde-fous de config, et où ils s'appliquent

Déclarés dans `config.py`, **appliqués** dans `utils/safety_limits.py` et `tools/trading.py`
(pas seulement affichés) :

- **`DEMO_MODE`** (défaut `false`) : en mode démo, le code substitue une **clé/adresse factices**
  → lecture seule, aucun vrai wallet requis.
- **`validate_order()`** rejette un ordre si : sa valeur dépasse **`MAX_ORDER_SIZE_USD`**
  (déf. 1000) ; l'exposition totale dépasserait **`MAX_TOTAL_EXPOSURE_USD`** (déf. 5000) ;
  l'exposition **par marché** dépasserait **`MAX_POSITION_SIZE_PER_MARKET`** (déf. 2000) ; la
  **liquidité** du marché est sous **`MIN_LIQUIDITY_REQUIRED`** ; le **spread** dépasse
  **`MAX_SPREAD_TOLERANCE`** (déf. 0,05).
- **Porte de confirmation** (`tools/trading.py`) : si `ENABLE_AUTONOMOUS_TRADING = false` (défaut),
  **tout** ordre exige `confirm=true` ; si activé, seuls les ordres au-dessus de
  **`REQUIRE_CONFIRMATION_ABOVE_USD`** (déf. 500) l'exigent. La porte **bloque** l'ordre, elle
  ne fait pas que journaliser.
- **Hygiène de la clé** : la clé n'est **jamais imprimée** (masquée dans `to_dict`) et les
  messages d'erreur évitent de divulguer sa valeur.

## C.3 Ce qu'on réutilise tel quel vs ce qu'on réécrit — et pourquoi

**On réutilise (comme référence) :**
- La **liste des champs de l'ordre EIP-712** (salt, maker, signer, taker, tokenId, makerAmount,
  takerAmount, expiration, nonce, feeRateBps, side, signatureType) — c'est le contrat exact du
  CTF Exchange.
- Le **schéma en deux niveaux L1 → L2** et la **création unique** des identifiants.
- Le **schéma de garde-fous** (DEMO_MODE, plafonds, porte de confirmation, masquage de la clé) et
  le fait qu'ils soient **appliqués avant la pose**, pas juste déclarés.

**On délègue la signature à `py_clob_client`** (la librairie officielle) plutôt qu'au signeur
maison du dépôt. *Justification :* le `OrderSigner` maison utilise un domaine EIP-712 incomplet
(nom `ClobAuthDomain`, **sans `verifyingContract`**) — ça sert d'illustration mais **ne doit pas
être copié tel quel** pour signer un vrai ordre ; la bonne signature (domaine « Polymarket CTF
Exchange », adresse du contrat, gestion des proxys) est déjà faite, et testée, dans
`py_clob_client` (que le dépôt appelle d'ailleurs pour poster réellement).

**On réécrit plus strictement :**
- **Double verrou de sécurité** : le dépôt a un seul interrupteur (`ENABLE_AUTONOMOUS_TRADING`).
  Nous exigeons **deux** verrous (repo 9) : `enable_trading = false` **ET** `mock_trading = true`
  par défaut ; aucun ordre réel tant que les deux ne sont pas levés explicitement.
- **Anti-sniping et stops par période** : **absents** de ce dépôt. On les ajoute (repos 7 et 8) :
  pause sur saut de midpoint, mid filtré, cooldown, distance de repricing max ; stops
  journalier / mensuel / drawdown / halt.
- **Application en dur des plafonds** : on garde le **bon réflexe** de ce dépôt (vérifier
  `MAX_ORDER_SIZE` / `MAX_TOTAL_EXPOSURE` **avant** chaque pose) et on l'inscrit au cœur de notre
  boucle, jamais comme simple réglage affiché.

---

# D. Résumé — les 5 choses que ça change concrètement

1. **On sait comment mesurer H2 sur nos propres ordres** : un tableau de relevé (§ A.3), une
   ligne par ordre, à remplir dès les premiers cycles manuels du palier 1 — sans attendre un bot.
2. **On corrige le défaut du modèle de référence** : on enregistre **aussi les non-fills** (et la
   profondeur devant), pour mesurer une **vraie** probabilité d'exécution, pas seulement la
   vitesse des ordres déjà servis.
3. **Le run 10 (copy-trading) a ses critères d'étiquetage** : part maker/taker, fréquence,
   taille, nombre de marchés → séparer les **market makers (non copiables)** des directionnels ;
   la persistance de la performance reste à mesurer **à part**.
4. **On a une carte claire de l'exécution réelle** : L1 → L2 → signature EIP-712 → pose, avec la
   liste exacte des champs d'ordre — mais on **délègue la signature à `py_clob_client`** (le
   signeur maison du dépôt a un domaine incomplet).
5. **Nos garde-fous v1 sont fixés, en plus stricts** : double verrou `enable_trading=false` +
   `mock_trading=true`, plafonds `max_order_size` / `max_total_exposure` **appliqués en dur avant
   chaque pose**, porte de confirmation, plus anti-sniping et stops par période (absents du
   dépôt de référence).

---

*Étude de code en lecture seule, aucun dépôt exécuté. Les mécaniques Polymarket évoluent :
revérifier les champs d'ordre et le domaine de signature dans `py_clob_client` et la doc
officielle avant toute pose réelle.*
