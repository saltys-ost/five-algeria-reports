# Analyse de 20 dépôts GitHub — écosystème Polymarket & outils de trading

> **Cadre de l'analyse.** Audit en **lecture seule**. Chaque dépôt a été cloné en superficiel
> (`--depth 1`, blobs LFS ignorés) dans un dossier isolé, hors de tout projet existant.
> **Aucun code n'a été exécuté** : ni script, ni `npm install`, ni `pip install`, ni binaire.
> Seuls le code source, les manifestes de dépendances, les scripts d'installation et la
> documentation ont été lus. Chaque dépôt a d'abord passé un audit de sécurité (recherche
> d'exfiltration de clés/seed, endpoints inconnus, code obfusqué, hooks post-install,
> shell-outs, drainers) avant toute analyse fonctionnelle.
>
> **Grille de lecture.** L'analyse juge chaque dépôt **pour sa valeur propre**, comme s'il
> était découvert sans contexte — pas à travers le prisme d'une stratégie particulière.
>
> **Légende sécurité.** `SÛR` = rien d'anormal détecté · `DOUTE` = point à vérifier avant usage
> (expliqué) · `DANGER` = ne pas utiliser (expliqué).
> **Verdict d'exploitation.** `EXPLOITER` = valeur forte, mérite d'être creusé ·
> `INSPIRER` = idées/techniques à retenir · `IGNORER` = peu d'intérêt (et pourquoi).

---

# CATÉGORIE 1 — ANALYTICS (dépôts 1 à 5)

---

## 1. SII-WANGZJ/Polymarket_data — infrastructure de données + dataset 107 Go

**1. Identité.** [github.com/SII-WANGZJ/Polymarket_data](https://github.com/SII-WANGZJ/Polymarket_data).
Auteurs : équipe académique (Shanghai Innovation Institute, Westlake, SJTU, Fudan, HIT).
Dernier commit : 2026-01-01. Licence MIT. Python 3.12+. Documentation README **excellente**
(tableaux de formats, tailles, schémas). Dataset hébergé sur HuggingFace (107 Go, 1,1 milliard
de trades, 268 000+ marchés). Le dépôt GitHub contient **le code**, pas les données (le dossier
`data/` est vide, juste un `.gitkeep`) : la donnée se télécharge séparément ou se re-fetch avec
l'outil. C'est un projet de recherche publié, pas un produit commercial.

**2. Verdict sécurité : SÛR.** Aucun hook d'installation, aucune référence à une clé privée ou
une seed, aucun endpoint suspect. Les scripts `scripts/*.sh` sont de simples lanceurs
(`fetch_markets.sh`, `continuous_start.sh`…). Les fetchers tapent la blockchain Polygon (RPC) et
la Gamma API publique. Aucune écriture ailleurs que dans `data/` et `logs/`. Projet purement
extractif et lisible.

**3. Résumé (2 phrases).** C'est une usine à données Polymarket : elle aspire l'intégralité de
l'historique de trading depuis la blockchain Polygon et l'API Gamma, puis le range en fichiers
Parquet propres et prêts à analyser. Elle fournit aussi le dataset complet déjà constitué (107 Go)
en téléchargement.

**4. Fonctionnement de bout en bout.** (a) *Source* : le fetcher `rpc.py` lit directement les
logs d'événements `OrderFilled` du contrat Polymarket sur la blockchain Polygon (via un nœud RPC),
et `gamma.py` récupère les métadonnées de marchés sur l'API Gamma publique. (b) *Décodage* :
`processors/decoder.py` décode les logs binaires bruts de la blockchain en champs lisibles
(prix, tailles, maker/taker, hash d'ordre, frais). (c) *Nettoyage & liaison* :
`processors/cleaner.py` et `trades.py` relient chaque trade à son marché, comblent les jetons
manquants, calculent les frais maker/taker/protocole. (d) *Stockage* : écriture en Parquet
compressé (`sort_parquet.py`, `merge_parquet.py`) avec écriture incrémentale et reprise sur
incident (auto-save du progrès). (e) *Mode continu* : `continuous_fetch.py` synchronise les
nouveaux trades toutes les ~2 s. Sortie : 5 datasets prêts à l'emploi, dont `orderfilled.parquet`
(31 Go, événements bruts) et `trades.parquet` (32 Go, trades enrichis).
*Notions* : **Parquet** = format de fichier colonne compressé, idéal pour analyser des milliards
de lignes rapidement. **RPC** = interface pour interroger directement une blockchain.

**5. Logique économique.** Le dépôt ne gagne pas d'argent en soi : c'est une **matière première**.
Sa valeur vient de ce qu'il donne accès à la donnée *on-chain* que les sources tierces gratuites
n'ont pas (numéro de bloc, frais détaillés, hash d'ordre). Toute stratégie fondée sur le
comportement historique — détection de traders performants, backtests, calibration de modèles —
a besoin exactement de ce genre de granularité. « Échoue » seulement au sens où stocker et traiter
107 Go demande des moyens (disque, RAM, temps) hors de portée d'une petite machine.

**6. Architecture.** `polymarket/fetchers/` (rpc + gamma) = collecte · `polymarket/processors/`
(decoder, cleaner, trades) = transformation · `polymarket/tools/` (fetch continu, merge, sort,
refetch des blocs échoués) = maintenance des fichiers · `polymarket/cli/` = interface en ligne de
commande (49 Ko dans `main.py`, c'est le chef d'orchestre) · `scripts/*.sh` = raccourcis.

**7. Ce qu'on peut en réutiliser.** (a) Le **dataset lui-même**, comme base de tout backtest ou
étude comportementale sérieuse. (b) La **méthode de décodage on-chain** des événements
`OrderFilled` — précieuse si l'on veut la vérité des frais et des exécutions plutôt que des prix
d'API approximatifs. (c) Le pattern de collecte **résumable + incrémentale** en Parquet, réutilisable
pour tout collecteur maison. (d) Le tableau « vs third-party » documente exactement quels champs
manquent aux sources gratuites.

**8. Limites & angles morts.** Volume écrasant (107 Go) : inutilisable sans pipeline de traitement.
Re-fetch complet depuis la blockchain = très long et suppose un accès RPC fiable (potentiellement
payant à ce débit). Dataset figé « avant 2026 » : pour du récent, il faut re-fetch. Aucune stratégie
fournie — c'est de la donnée brute, tout le travail d'analyse reste à faire.

**9. Note de proximité.** *(facultatif)* Fournit la donnée on-chain qui manque aux mesures faites
jusqu'ici uniquement via API (Gamma/CLOB).

---

## 2. evan-kolberg/prediction-market-backtesting — moteur de backtest (NautilusTrader)

**1. Identité.** [github.com/evan-kolberg/prediction-market-backtesting](https://github.com/evan-kolberg/prediction-market-backtesting).
Auteur : Evan Kolberg. Dernier commit : 2026-05-16, **très actif** (v4.1-alpha, historique de
versions détaillé). Licence mixte MIT + LGPL-3.0. Python 3.12 + Rust (édition 2024). Bâti sur
**NautilusTrader** (moteur de trading algorithmique professionnel open-source). Documentation
abondante (site mkdocs, UML, guides). C'est le dépôt le plus « pro » de la catégorie.

**2. Verdict sécurité : SÛR.** Aucun hook d'installation, aucune manipulation de clé, aucun
endpoint suspect. Rust + Python, code structuré en crates et modules. Pas de shell-out douteux.
La partie « live sandbox » pour marchés BTC 5 min est explicitement du *sandbox* (simulation),
pas de l'exécution réelle sur un compte.

**3. Résumé (2 phrases).** C'est un simulateur qui rejoue l'historique des marchés Polymarket
tick par tick pour tester une stratégie *avant* d'y risquer de l'argent, avec une modélisation
fine des frais et du carnet d'ordres. Il fournit en prime une bibliothèque de 15 stratégies déjà
codées et un moteur de graphiques de performance très complet.

**4. Fonctionnement de bout en bout.** (a) *Données* : chargement de l'historique (support d'un
fournisseur « Telonex », caches locaux, replay du carnet d'ordres avec deltas + trades). (b)
*Moteur* : NautilusTrader simule un marché — il fait « rejouer » les prix et les ordres passés
comme s'ils se déroulaient en direct, applique la stratégie choisie, et modélise les frais et le
slippage. (c) *Stratégies* : chaque fichier de `strategies/` définit une logique (voir §7). (d)
*Runners* : les « EXPERIMENT » dans `backtests/` décrivent un test (marché, période, paramètres) ;
un menu interactif (`main.py`) les découvre automatiquement. (e) *Sortie* : graphiques riches —
équité totale et par marché, ticks de P&L, allocation, prix YES avec fills achat/vente colorés,
drawdown, ratio de Sharpe, rendements mensuels, et un « avantage de Brier cumulé » (qualité
prédictive). *Notion* : **backtest** = rejouer le passé pour mesurer ce qu'une stratégie aurait
rapporté ; **NautilusTrader** = moteur de simulation/exécution algorithmique réputé.

**5. Logique économique.** Ne gagne pas d'argent directement : c'est l'outil qui **évite d'en
perdre**. Une stratégie qui « semble » gagnante à l'œil peut être détruite par les frais, le
slippage ou un biais de sélection ; le backtest chiffre tout ça avant le capital réel. Sa valeur
économique = filtrer les fausses bonnes idées. « Échoue » si les données historiques sont
imparfaites (carnet reconstitué approximatif) ou si le futur ne ressemble pas au passé
(surapprentissage).

**6. Architecture.** `crates/` = code Rust (conversion de données rapide, cœur performant) ·
`strategies/` = les logiques de trading en Python · `backtests/` = les scénarios de test
(EXPERIMENT) · `live/` = plomberie sandbox temps réel (BTC 5 min) · `prediction_market_extensions/`
= adaptateurs Polymarket pour Nautilus · `internal/` + `docs/` = outillage et documentation.

**7. Ce qu'on peut en réutiliser (le plus précieux du lot).** La **bibliothèque de stratégies**
déjà écrites, chacune étant une idée de trading à comprendre : `binary_pair_arbitrage`
(arbitrage YES/NO), `microprice_imbalance` (déséquilibre du carnet), `mean_reversion`,
`vwap_reversion`, `rsi_reversion`, `breakout`, `threshold_momentum`, `final_period_momentum`
(momentum en fin de marché), `panic_fade` (prendre le contre-pied des paniques), `deep_value`,
`late_favorite_limit_hold`, `account_trade_replay` (rejouer les trades d'un compte). C'est un
catalogue d'inefficiences à étudier. Réutilisable aussi : la modélisation des frais, le replay de
carnet, les graphiques de performance.

**8. Limites & angles morts.** Dépendance lourde à NautilusTrader (courbe d'apprentissage réelle,
surtout pour un non-développeur). Rust à compiler. La qualité du backtest dépend entièrement de la
qualité du carnet historique reconstitué — un carnet approximatif donne des résultats
faussement rassurants. « alpha » (version instable) sur plusieurs modules. Certains modèles/données
restent privés.

**9. Note de proximité.** *(facultatif)* Permettrait de backtester rigoureusement toute stratégie
avant de risquer le capital réel.

---

## 3. ent0n29/polybot — infrastructure de trading + rétro-ingénierie de stratégies

**1. Identité.** [github.com/ent0n29/polybot](https://github.com/ent0n29/polybot).
Auteur : Antonio Stano. Dernier commit : 2026-02-21. Architecture **microservices Java 21** +
pipeline de données. Documentation soignée. Se présente comme la fondation d'un futur produit
« AWARE » (intelligence sur les traders, indices, miroir de fonds). Ambitieux et structuré.

**2. Verdict sécurité : SÛR.** Un seul `subprocess` en Python, uniquement pour lire le hash git
courant (`git rev-parse HEAD`) dans un script de snapshot — anodin. Les scripts
`start-all-services.sh` / `stop-all-services.sh` orchestrent des conteneurs Docker locaux. Aucune
manipulation de clé suspecte, aucun endpoint d'exfiltration. Note d'usage : lancer la stack
suppose Docker, Java 21, Maven — mais **on n'exécute rien ici**, on lit.

**3. Résumé (2 phrases).** C'est une plateforme complète (« qualité production ») pour ingérer en
temps réel tous les trades de Polymarket, faire tourner des stratégies de market making et
d'exécution, et surtout **rétro-analyser les stratégies des autres traders** pour les scorer et
les répliquer. Le tout en microservices Java avec base analytique ClickHouse et supervision Grafana.

**4. Fonctionnement de bout en bout.** (a) *Ingestion* : un service `ingestor` capte les trades
de marché et d'utilisateurs et les pousse dans un bus d'événements (Redpanda) puis dans
**ClickHouse** (base de données analytique très rapide pour de gros volumes). (b) *Stratégie* :
le `strategy-service` héberge la logique de market making — on y trouve des configs parlantes :
`GabagoolMarketDiscovery` (sélection de marchés à animer), `CompleteSetConfig` (jouer sur le
complete-set : 1 YES + 1 NO = 1 $, donc split/merge), `TakerConfig`, `SizingConfig`,
`BankrollConfig` (gestion du capital), `TimingConfig`, `MarketInventory`/`OrderState` (suivi des
positions et des ordres vivants). (c) *Exécution* : `executor-service` passe les ordres (modes
papier et réel). (d) *Analyse/recherche* : le dossier `research/` (Python) contient le joyau —
`replication_score.py` et `replication_score_orders.py` calculent à quel point on peut **répliquer**
la performance d'un trader donné, plus `calibrate_maker_fill_model.py` (modéliser la probabilité
qu'un ordre maker soit exécuté), `deep_analysis.py`, `paper_trading_dashboard.py`. (e) *Supervision* :
Grafana + Prometheus + Alertmanager.
*Notions* : **microservices** = l'appli est découpée en petits services indépendants qui
communiquent ; **ClickHouse** = base de données taillée pour analyser des milliards de lignes ;
**Redpanda** = file d'événements temps réel (compatible Kafka).

**5. Logique économique.** Deux moteurs. (1) *Market making* : poser des ordres des deux côtés et
capter le spread + les récompenses de liquidité ; les configs `CompleteSet`/`Bankroll`/`Sizing`
montrent une gestion sérieuse du risque et de l'inventaire. (2) *Réplication* : identifier les
traders réellement performants (pas chanceux) via un score, puis copier/mirrorer leur logique —
l'inefficience exploitée est que **la performance des bons traders est en partie persistante et
observable on-chain**. « Échoue » si le market making se fait ramasser par un flux toxique
(adverse selection), ou si le score de réplication confond chance et compétence.

**6. Architecture.** `ingestor-service` (collecte) · `strategy-service` (cerveau MM) ·
`executor-service` (bras qui passe les ordres) · `analytics-service` (mesures) ·
`infrastructure-orchestrator-service` (coordination) · `polybot-core` (socle commun) ·
`research/` (Python : rétro-ingénierie, calibration, backtests) · `monitoring/` (Grafana/Prometheus).

**7. Ce qu'on peut en réutiliser.** (a) L'idée et le code du **score de réplication** d'un trader —
une méthode pour distinguer talent et chance. (b) Le **modèle de probabilité d'exécution d'un ordre
maker** (`calibrate_maker_fill_model.py`) — précisément la question ouverte de toute stratégie de
pose d'ordres. (c) L'architecture d'inventaire MM (`MarketInventory`, `OrderState`, configs de
sizing/bankroll) comme modèle mental d'un market maker propre. (d) Le pipeline ClickHouse pour
qui voudrait analyser de gros volumes.

**8. Limites & angles morts.** Lourdeur : stack Java + Docker + ClickHouse + Redpanda = très loin
d'un script simple, exigeant à opérer pour un non-développeur. Beaucoup de « future work »
(le produit AWARE n'existe pas encore). Le mode réel implique de vraies clés — à n'envisager que
bien plus tard et avec prudence.

**9. Note de proximité.** *(facultatif)* Le modèle de fill maker et l'inventaire MM touchent
directement les questions ouvertes des stratégies de pose d'ordres.

---

## 4. pmxt-dev/pmxt — API unifiée multi-plateformes (« le ccxt des marchés prédictifs »)

**1. Identité.** [github.com/pmxt-dev/pmxt](https://github.com/pmxt-dev/pmxt).
Éditeur : pmxt-dev (projet actif, quasi commercial : Discord, Product Hunt, DOI Zenodo, publication
npm `pmxtjs` + SDK Python). Dernier commit : 2026-07-18 (auto-update CI, v2.54.0). Licence MIT.
Se veut le **ccxt** (la librairie unifiée bien connue du trading crypto) mais pour les marchés
prédictifs : une seule interface pour Polymarket, Kalshi, Limitless, Opinion, Myriad, etc.

**2. Verdict sécurité : SÛR — avec une CAUTION importante à comprendre.** Aucun code covert, aucun
hook d'installation malveillant. Les `subprocess` ne font que gérer un *sidecar* local du SDK
(chercher/tuer le processus `bundled.js` via `pgrep`/`taskkill`) — normal. **Le point d'attention** :
le SDK Python accepte une `private_key` et, en **mode « hosted trading »**, la place dans un
dictionnaire de credentials envoyé aux serveurs de pmxt (`api.pmxt.dev` / `trade.pmxt.dev`).
Ce n'est **pas** de l'exfiltration cachée — c'est le design assumé d'un service hébergé — **mais
confier une clé privée réelle à un tiers est un risque de garde d'actifs majeur**. Règle d'usage :
n'utiliser que le **mode self-host / signature locale** (venue-native credentials), **jamais**
transmettre une clé d'un wallet qui détient des fonds au mode hébergé. Endpoints observés :
`api.pmxt.dev`, `trade.pmxt.dev`, `localhost` (sidecar). → **DOUTE si mode hosted ; SÛR en lecture
de données / self-host.**

**3. Résumé (2 phrases).** pmxt donne une interface unique et cohérente pour lire les données
(et passer des ordres) sur une douzaine de plateformes de marchés prédictifs, sans réapprendre
l'API de chacune. C'est l'équivalent, pour les marchés prédictifs, de ce que ccxt est au trading
crypto.

**4. Fonctionnement de bout en bout.** (a) *Unification* : le SDK expose des méthodes normalisées
(marchés, prix, trades, carnet, historique) qui, sous le capot, traduisent vers l'API native de
chaque plateforme. (b) *Deux modes* : **lecture de données** (public, sans clé — sûr et utile) ;
**trading**, soit *self-host* (la signature des ordres reste locale, avec les identifiants natifs
de la plateforme), soit *hosted* (pmxt gère l'exécution côté serveur, ce qui implique de leur
fournir des credentials — cf. §2). (c) *Sidecar* : en Python, un petit serveur Node (`bundled.js`)
est lancé localement pour faire tourner la logique commune ; `server_manager.py` le démarre, le
surveille et nettoie les processus orphelins. Sortie : des objets de données normalisés, exploitables
en Python ou JS.

**5. Logique économique.** Outil d'infrastructure : il ne trade pas, il **abaisse le coût
d'intégration**. Sa valeur = pouvoir comparer et agir sur plusieurs plateformes d'un seul code —
prérequis de tout arbitrage inter-plateformes (ex. Polymarket ↔ Kalshi ↔ Limitless). L'inefficience
qu'il aide à exploiter est le **décalage de prix entre plateformes** sur un même événement.
« Échoue » comme dépendance : un service hébergé peut changer ses conditions, et le mode hosted
concentre le risque de clé.

**6. Architecture.** `core/` = logique commune · `sdks/python/` + `sdks/` (JS via `pmxtjs`) =
librairies clientes · `server_manager.py` = gestion du sidecar local · `_hosted_routing.py` =
routage des appels vers le service hébergé · `tools/`, `docs/`, `ARCHITECTURE.md`.

**7. Ce qu'on peut en réutiliser.** (a) La **couche d'abstraction multi-plateformes** en lecture,
pour surveiller le même événement sur plusieurs venues à la fois. (b) Le mapping des endpoints
natifs de chaque plateforme (utile même sans utiliser pmxt : ça documente qui expose quoi). (c)
Le pattern « une API, plusieurs venues » comme modèle pour un moniteur d'arbitrage inter-plateformes.

**8. Limites & angles morts.** Le mode hosted et sa garde de clé (cf. §2) sont le principal risque.
Dépendance à un tiers actif mais jeune. La couverture « trading » varie selon les plateformes
(certaines en lecture seule). Abstraction = on perd parfois des champs natifs spécifiques.

**9. Note de proximité.** *(facultatif)* Serait la brique d'un moniteur d'arbitrage entre
Polymarket et d'autres plateformes.

---

## 5. txbabaxyz/collectmarkets2 — collecteur CSV & stats d'un wallet

**1. Identité.** [github.com/txbabaxyz/collectmarkets2](https://github.com/txbabaxyz/collectmarkets2).
Auteur : « Richie » (txbabaxyz). Dernier commit : 2026-02-21. Python 3.10+. Un seul fichier
principal (`collector.py`, ~650 lignes) + `requirements.txt` + `wallets.example.txt`. Petit,
simple, lisible — l'anti-thèse des microservices. Documentation README claire et suffisante.

**2. Verdict sécurité : SÛR.** Le seul motif « alarmant » du grep est `os.system('clear')` — une
simple commande pour effacer l'écran du terminal (menu interactif), totalement anodine. Aucune clé,
aucune seed, aucune écriture réseau sortante autre que les requêtes GET à l'API publique Polymarket.
`wallets.txt` ne contient que des **adresses publiques** (pas de clés). Source unique :
`https://data-api.polymarket.com/activity`. Rien de sensible.

**3. Résumé (2 phrases).** C'est un petit utilitaire interactif qui télécharge tout l'historique
de trades d'une ou plusieurs adresses Polymarket et l'exporte en CSV rangés par marché, avec des
graphiques et des statistiques. Idéal pour observer ce que fait un wallet donné, sans rien installer
de lourd.

**4. Fonctionnement de bout en bout.** (a) *Entrée* : un fichier `wallets.txt` listant des couples
`nom,adresse`. (b) *Collecte* : pour chaque adresse, appels paginés à `data-api.polymarket.com/activity`,
avec déduplication automatique des transactions. (c) *Mode cyclique* : possibilité de relancer la
collecte à intervalle régulier (toutes les 1/5/10 min, N cycles), en fusionnant les marchés vus
plusieurs fois et en dédupliquant — utile pour suivre un wallet dans le temps. (d) *Sortie* : CSV
organisés par marché ; puis visualisation — nuage de points (prix vs temps, taille du point =
montant USDC), accumulation cumulée de contrats, statistiques ; filtre qualité qui ignore les
marchés à moins de 30 trades. Menu en ligne de commande pour tout piloter.

**5. Logique économique.** Ne trade pas : c'est de l'**observation**. Sa valeur = comprendre le
comportement d'un trader (quand il entre, à quel prix, quelle taille, sur quels marchés) — première
étape avant toute idée de copy-trading ou d'étude de flux. L'inefficience sous-jacente : les traders
performants laissent une trace publique on-chain qu'on peut lire gratuitement. « Échoue » seulement
si l'on croit que le passé d'un wallet prédit son futur sans le vérifier.

**6. Architecture.** Un fichier `collector.py` faisant tout : menu interactif, collecte paginée,
déduplication, export CSV, tracé matplotlib, mode cyclique. `requirements.txt` (requests, pandas,
matplotlib probable). `wallets.example.txt` = gabarit. Simplicité radicale = facile à lire et à
adapter.

**7. Ce qu'on peut en réutiliser.** (a) Un **exemple minimal et propre** d'appel à
`data-api.polymarket.com/activity` avec pagination + déduplication — directement copiable. (b) Le
mode cyclique de suivi d'un wallet. (c) Le filtre qualité « ≥30 trades » comme garde-fou simple
contre les marchés illiquides. (d) Bon patron pédagogique pour un débutant : un script lisible qui
fait une chose bien.

**8. Limites & angles morts.** Fait peu (collecte + graphes), sans analyse avancée ni scoring.
Mono-fichier = peu extensible tel quel. Dépend d'un unique endpoint (si l'API change, ça casse).
Pas de tests. Aucune notion de stratégie — c'est un observateur, pas un décideur.

**9. Note de proximité.** *(facultatif)* Exemple direct et réutilisable d'accès à l'API `activity`
pour observer des wallets.

---

# CATÉGORIE 2 — BOTS DE TRADING (dépôts 6 à 10)

---

## 6. alsk1992/CloddsBot — terminal de trading agentique multi-chaînes (« Clodds »)

**1. Identité.** [github.com/alsk1992/CloddsBot](https://github.com/alsk1992/CloddsBot) (npm : `clodds`).
« AI-powered trading terminal for prediction markets, crypto & futures » — *Claude + Odds = Clodds*.
Node ≥ 22, TypeScript 5.3, MIT. Construit pour le hackathon Colosseum. Revendique **119+ « skills »**,
1000+ marchés, ~10 700 clones en 14 jours. Contient `AUDIT.md` (auto-audit daté), `SECURITY.md`,
`Dockerfile`, 25 fichiers de tests (dont « trading safety », « risk-guards »). C'est de loin le dépôt
le plus vaste et le plus ambitieux du lot.

**2. Verdict sécurité : SÛR sur le code, mais DOUTE fort à l'usage (surface d'attaque énorme).**
Points vérifiés : (a) **aucune exfiltration** — les clés privées ne sont jamais empaquetées dans un
appel réseau/Telegram ; les occurrences de `PRIVATE_KEY` sont soit des messages d'erreur (« il faut
définir X »), soit un usage local pour signer (`ethers.Wallet`). (b) Le **hook `postinstall`** exécute
du code à l'installation, mais seulement pour **mettre en cache un modèle d'embedding** local
(`@xenova/transformers`, MiniLM) — pas malveillant, mais **ça exécute du code et télécharge un modèle
dès `npm install`**. (c) Nombreux `child_process`/`execSync` : c'est le **système de skills** — l'agent
lance des commandes shell par conception. (d) Parle à ~15 hôtes externes (Anthropic, Telegram,
CoinGecko, RPC de Base/Polygon/Solana, predict.fun, opinion.trade, drift, pump.fun…). *Conclusion* :
rien ne prouve une intention malveillante (projet connu, documenté, testé, avec docs de sécurité),
**mais** un agent qui exécute du shell, tourne un postinstall, et manipule des clés multi-chaînes est
**intrinsèquement à haut risque pour un non-développeur possédant un wallet financé**. → **À étudier,
pas à exécuter près du vrai wallet.**

**3. Résumé (2 phrases).** Clodds est un « terminal » de trading piloté par IA (Claude) : on lui parle
en langage naturel et il agit via une bibliothèque de 119+ compétences couvrant marchés prédictifs,
crypto et futures sur de nombreuses plateformes. C'est autant un framework d'agent qu'un bot de trading.

**4. Fonctionnement de bout en bout.** (a) *Interface* : chat (terminal / WebChat / canaux comme
Telegram) ; l'utilisateur exprime une intention. (b) *Cerveau* : un agent LLM (Anthropic) interprète et
choisit des **skills**. (c) *Skills* : modules autonomes (`src/skills/…`) — lecture de marchés, passage
d'ordres sur diverses venues, DeFi (Kamino/Solana), etc. ; chacun peut appeler des API ou exécuter des
commandes. (d) *Mémoire* : base vectorielle locale (LanceDB) + embeddings (transformers.js) pour se
souvenir du contexte. (e) *Exécution* : pour trader, il faut fournir des clés par variables
d'environnement (`EVM_PRIVATE_KEY`, `OPINION_PRIVATE_KEY`…) ; la signature se fait localement. (f)
*Garde-fous* : tests de « risk-guards » et « trading safety ». *Notions* : **skill/agent** = l'IA choisit
des outils pour accomplir une tâche ; **base vectorielle** = mémoire par similarité sémantique ;
**postinstall** = script lancé automatiquement après `npm install`.

**5. Logique économique.** Ne repose pas sur une inefficience unique : c'est une **plateforme** pour en
exploiter plusieurs (arbitrage inter-venues, signaux, DeFi) via des skills. Sa valeur = rapidité
d'action et couverture multi-plateformes pilotée en langage naturel. « Échoue » de multiples façons : un
LLM qui hallucine un ordre, une skill boguée, une dépendance compromise — et comme il touche à des clés,
l'échec peut être coûteux. Le risque opérationnel domine le risque de marché.

**6. Architecture.** `src/skills/` (les 119+ compétences, dont `bundled/lighter`, etc.) ·
`src/agents/` (orchestration LLM, handlers par venue : opinion, predict.fun…) · `src/extensions/`
(task-runner, google-auth, mémoire LanceDB…) · `src/permissions/` (contrôle d'accès des skills) ·
`src/feeds/` (flux de données, ex. Kalshi) · `src/identity/` (erc8004) · tests, Docker, docs.

**7. Ce qu'on peut en réutiliser.** (a) L'**architecture agent + skills + permissions** comme modèle de
conception. (b) Les **handlers par venue** documentent concrètement comment parler à predict.fun,
opinion.trade, Kalshi, etc. (c) Le **modèle de risk-guards / trading-safety** (tests) est instructif.
(d) L'intégration mémoire vectorielle locale. À prendre comme **source d'idées**, pas comme binaire à
lancer.

**8. Limites & angles morts.** Surface d'attaque massive (shell + postinstall + clés multi-chaînes +
15 hôtes). Très lourd (Node 22, nombreuses dépendances, SDKs DeFi). Un LLM dans la boucle
d'exécution = risque d'action erronée. Marketing appuyé (compteur de clones, hackathon). **À ne pas
exécuter avec le vrai wallet** : pour un non-développeur, le rapport risque/bénéfice de le faire tourner
est défavorable.

**9. Note de proximité.** *(facultatif)* Illustre l'intégration d'un LLM comme pilote de trading — mais
son usage direct est déconseillé vu le wallet réel.

---

## 7. lihanyu81/polymarket_lp_tool — outil de récompenses de liquidité (repricing d'ordres)

**1. Identité.** [github.com/lihanyu81/polymarket_lp_tool](https://github.com/lihanyu81/polymarket_lp_tool).
Auteur : « 臭臭Panda » ([@Chosmos110](https://x.com/Chosmos110)). Python **+ réécriture Rust**
(`rust_mm_bot`), pile `tokio + reqwest + tokio-tungstenite`. README bilingue (中文/EN) détaillé et
honnête sur les limites. Petit et ciblé (~2 Mo).

**2. Verdict sécurité : SÛR.** La clé est lue depuis l'environnement (`POLYMARKET_PRIVATE_KEY` /
`PRIVATE_KEY`) et reste locale pour signer les actions CLOB. Seuls hôtes sortants : `api.telegram.org`
(notifications/commande) et `api.polygonscan.com` (lecture on-chain). Aucun hook d'installation, aucun
code obfusqué. Un lien de parrainage Polymarket (optionnel) figure dans le README — sans effet sur le
code. Rien d'anormal.

**3. Résumé (2 phrases).** Cet outil **surveille et re-price** vos ordres limites déjà posés sur
Polymarket pour maximiser les **récompenses de liquidité**, sans jamais créer l'ordre initial (vous le
posez à la main sur le site). Il décide, à chaque tick, de **garder / annuler / annuler-et-reposer** en
fonction du carnet et de la « demi-largeur » de récompense — avec de vraies protections anti-sniping.

**4. Fonctionnement de bout en bout.** (a) *Portée* : une whitelist de jetons (ou, à défaut, les jetons
de vos ordres ouverts actuels, rafraîchie périodiquement). (b) *Lecture* : le carnet est suivi
(REST côté Python, **WebSocket-first** côté Rust : canaux market + user, avec réconciliation REST). (c)
*Décision* : logique de pricing « coarse/fine » déterministe ; comparaison à la demi-largeur de la zone
qui score des récompenses ; actions simplifiées **keep / cancel / cancel+replace (même taille)**. (d)
*Protections anti-sniping* (le point fort) : pause si le midpoint saute, confirmation d'un mid stable,
midpoint filtré EMA/médiane, cooldown après exécution, distance de repricing max par mise à jour — tout
cela pour éviter d'être « ramassé » lors d'un mouvement brutal (adverse selection). (e) *Contrôle* :
commandes Telegram (`/status /orders /pnl /set_rule`) + panneau web (Python). *Notion* :
**récompenses de liquidité** = Polymarket paie quotidiennement les ordres limites proches du milieu,
exécutés ou non ; l'enjeu est de rester dans la zone qui score sans se faire exécuter au mauvais moment.

**5. Logique économique.** Revenu = **loyer de liquidité** versé par Polymarket pour la présence
d'ordres proches du midpoint. L'inefficience/incitation exploitée est explicite : la plateforme
subventionne la liquidité. Le risque clé — et c'est là que l'outil met son intelligence — est l'**adverse
selection** : un ordre trop bien placé se fait exécuter juste avant un mouvement, transformant le loyer
en perte directionnelle. D'où l'arsenal anti-sniping. « Échoue » si l'enveloppe de récompense du marché
est faible face au capital déjà en compétition, ou si les protections sont mal réglées.

**6. Architecture.** `passive_liquidity/` (cœur Python : `clob_factory.py` = client signé, pricing,
risque) · `run_passive_bot.py` / `run_web_panel.py` (lanceurs) · `rust_mm_bot/` (réécriture Rust
modularisée : pricing/execution/risk/telegram/persistence/runtime) · fichiers de test de pricing/orderbook.

**7. Ce qu'on peut en réutiliser (fort intérêt).** (a) La **logique anti-sniping** (jump filter,
mid EMA/médiane, cooldown, max-chase) — réponse concrète au risque n°1 du farming de récompenses. (b) La
mécanique **keep/cancel/replace** pilotée par la demi-largeur de récompense. (c) Le modèle
**WebSocket-first + réconciliation REST**. (d) La discipline « ne pas créer l'ordre initial
automatiquement » = garde-fou prudent. Directement pédagogique pour qui étudie les récompenses de
liquidité.

**8. Limites & angles morts.** Ce n'est **pas** un MM entièrement automatique (par choix) : il faut poser
les ordres soi-même. Version Rust « expérimentale » (à valider en petite taille). Dépend de l'API
d'ordres sous clé (donc suppose une clé active). Pas de backtest fourni. La qualité dépend du réglage
des seuils.

**9. Note de proximité.** *(facultatif)* Correspond très directement à une stratégie de récompenses de
liquidité, avec précisément la brique anti-adverse-selection qui manquait aux mesures théoriques.

---

## 8. MrFadiAi/Polymarket-bot — bot copy-trading + arbitrage, orienté débutant

**1. Identité.** [github.com/MrFadiAi/Polymarket-bot](https://github.com/MrFadiAi/Polymarket-bot) —
« Polymarket Trading Bot v3.1 ». Auteur : [@Mr_CryptoYT](https://x.com/Mr_CryptoYT). TypeScript,
Node ≥ 18. README bilingue (EN/AR) très pédagogique (« de A à Z »), plus `BEGINNER_GUIDE.md`,
`QUICKSTART.md`, `SDK_DOCUMENTATION.md`, tests vitest, dashboard. Pensé pour un utilisateur non technique.

**2. Verdict sécurité : SÛR.** Clé lue depuis `POLYMARKET_PRIVATE_KEY` (env), usage local
(`ethers.Wallet`) ; **mode `dryRun`** disponible (une clé factice `0x111…` sert au mode lecture). Hôtes
sortants = RPC Polygon variés + `api.goldsky.com` (subgraph d'indexation) + explorateurs — tous
légitimes. Une URL `custom-bridge.example.com` est un **placeholder** d'exemple. Aucun hook
d'installation, aucune exfiltration. Rien d'anormal.

**3. Résumé (2 phrases).** Ce bot suit automatiquement les **meilleurs traders** (copy-trading) et
exploite des écarts de prix (arbitrage « DipArb »), avec une **gestion du risque à 4 niveaux** et un
filtrage « smart money ». Il est explicitement conçu pour être installé et compris par un débutant, avec
un tableau de bord et un guide pas-à-pas.

**4. Fonctionnement de bout en bout.** (a) *Détection de traders* : identifie et filtre les « smart
money » — ne suit que les traders au **taux de gain ≥ 60 %**, **profit factor ≥ 1,5** et cohérents ;
un détecteur de « whale » évite de copier un coup de chance isolé. (b) *Copie* : réplique leurs entrées
avec un **dimensionnement dynamique** (réduit après pertes, augmente après gains). (c) *Arbitrage
(DipArb)* : capte des écarts, avec **taille minimale ≥ 1,50 $** (garantir la sortie) et seuils de profit
tenant compte du **gas**. (d) *Risque* : système à 4 couches — stop journalier 5 %, mensuel 15 %,
drawdown 25 %, **halt total à 40 %** de perte cumulée. (e) *Données* : trades on-chain via subgraph
Goldsky + RPC Polygon ; exécution signée localement ; **dashboard** temps réel. *Notion* : **subgraph
(Goldsky)** = service qui indexe la blockchain pour requêter l'historique facilement ; **profit factor**
= gains bruts ÷ pertes brutes.

**5. Logique économique.** Deux moteurs. (1) *Copy-trading* : la performance des bons traders est
partiellement persistante ; les filtres « smart money » cherchent à séparer talent et chance. (2)
*Arbitrage/DipArb* : écarts temporaires exploités avec contraintes de sortie et de coûts. La couche de
risque est le vrai différenciateur : elle borne la casse. « Échoue » si les filtres laissent passer des
traders chanceux, si les écarts se referment avant exécution (frais/gas), ou en cas de flux toxique.

**6. Architecture.** `src/services/` (`market-service`, `trading-service`, `arbitrage-service`…) =
cœur métier · `poly-sdk/` = SDK Polymarket maison · `bot-with-dashboard.ts` / `bot-config.ts` =
lanceurs · `dashboard/` = interface · `examples/`, `docs/`, guides.

**7. Ce qu'on peut en réutiliser.** (a) La **gestion du risque à 4 couches** (stops journalier/mensuel/
drawdown/halt) — réutilisable telle quelle dans n'importe quelle stratégie. (b) Les **critères de
filtrage « smart money »** (win rate, profit factor, cohérence, anti-whale-chance) pour qualifier un
trader avant de le copier. (c) Le **mode `dryRun`** comme bonne pratique. (d) Un SDK Polymarket lisible
et une doc débutant de qualité.

**8. Limites & angles morts.** Le copy-trading a un décalage temporel (on copie après coup) et suppose la
persistance de la performance — hypothèse à vérifier. Marketing (« Ultimate ») et auteur « influenceur »
à prendre avec recul. Qualité des signaux dépend de la donnée subgraph. Pas de backtest fourni pour
valider les seuils par défaut.

**9. Note de proximité.** *(facultatif)* La couche de gestion du risque et les filtres « smart money »
sont réutilisables quelle que soit la stratégie retenue.

---

## 9. HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits — moteur Rust multi-venues (10 stratégies)

**1. Identité.** [github.com/HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits](https://github.com/HarrierOnChain/Prediction-Markets-Trading-Bot-Toolkits).
Rust (tokio), MIT, ~3 400 lignes de Rust réel. README multilingue (EN/中文/Русский) très marketing,
avec **funnel Telegram** vers un service « géré » / copy-trading (« let us run it for you »,
« Early Access »). 7 venues « live », interface TUI. `SECURITY.md`, CI Rust.

**2. Verdict sécurité : SÛR sur le code — DOUTE sur le service géré.** Le code est **réel et
autonome** : `service/clob.rs` implémente la **vraie signature EIP-712** des ordres Polymarket
(alloy_signer local, HMAC L2), avec un garde-fou explicite (« le hot path ne transmettra pas d'ordre
signé tant que `enable_trading` et non-`mock_trading` ne sont pas activés »). Les **défauts sont sûrs** :
`enable_trading:false`, `mock_trading:true`. Aucun motif de danger, aucune exfiltration, hôtes = APIs
Polymarket + Telegram. **La réserve** : le README pousse fortement vers un **service géré / copy-trading
sur Telegram** — c'est-à-dire confier son capital ou ses clés à un tiers anonyme (« HarrierOnChain »).
Le **code open-source** est légitime ; **le service commercial associé** demande la prudence habituelle
(ne pas confier de clés/fonds à un tiers Telegram).

**3. Résumé (2 phrases).** C'est un **moteur d'exécution Rust unique** sur lequel tournent **10 bots de
stratégie** (arbitrage, market making, imbalance, copy-trading, whale, sniping de résolution…), avec une
couche de risque commune et des adaptateurs par venue. Le dépôt open-source est complet et fonctionnel ;
un service payant « géré » est proposé en parallèle.

**4. Fonctionnement de bout en bout.** (a) *Cœur* : un moteur asynchrone (tokio) + une couche de risque
partagée ; ajouter un marché = écrire **un adaptateur**. (b) *Données* : services `clob`, `midprice`,
`position_monitor` — carnet, midpoint, suivi des positions (config par défaut : APIs Gamma/CLOB/Data +
WS Polymarket). (c) *Stratégies* (dans `src/bot/`) : `arbitrage`, `cross_market_arb`, `directional_arb`,
`orderbook_imbalance`, `spread_farming`, `market_maker`, `copy_trading`, `whale_signal`,
`resolution_sniper`, `sports_execution` — dix logiques distinctes. (d) *Exécution* : signature EIP-712
locale, envoi à Polymarket **seulement** si le trading réel est explicitement activé. (e) *Interface* :
TUI (terminal) avec dashboard ; contrôle de la copie via config (`wallets_to_track`, `copy_size`,
seuils adaptatifs). *Notion* : **EIP-712** = standard de signature de données typées d'Ethereum, requis
par le contrat d'échange Polymarket ; **TUI** = interface en mode texte dans le terminal.

**5. Logique économique.** Boîte à outils : chacune des 10 stratégies vise une inefficience différente
(écart inter-marchés, déséquilibre de carnet, spread, suivi de whale…). Valeur = un socle d'exécution
propre réutilisable pour dix approches. « Échoue » selon la stratégie (adverse selection en MM, écarts
qui se referment en arbitrage, faux signaux en copy). Le **risque distinct** ici n'est pas le code mais le
**funnel** : la tentation de déléguer à un tiers Telegram.

**6. Architecture.** `src/bot/` (10 stratégies) · `src/service/` (`clob` signature/exécution,
`midprice`, `position_monitor`, `strategy`) · `src/ui/` (TUI) · `src/models.rs`, `utils.rs` ·
`config.json` / `config.yaml.example` (défauts sûrs) · `landing/` (page marketing).

**7. Ce qu'on peut en réutiliser (fort intérêt d'apprentissage).** (a) Une **référence Rust propre de la
signature EIP-712 des ordres Polymarket** — rare et précieuse pour comprendre l'exécution réelle. (b)
**Dix stratégies** lisibles côte à côte sur un moteur commun = catalogue d'idées et de structure. (c) Le
pattern **moteur unique + adaptateurs par venue**. (d) Les défauts de config sûrs (`mock_trading`) comme
bonne pratique.

**8. Limites & angles morts.** Le **funnel service-géré/copy-trading Telegram** est le principal risque
(ne jamais confier clés/fonds). Rust à compiler (barrière pour non-dev). README très promotionnel — juger
sur le code, pas sur les badges. Couverture réelle des venues « live » à vérifier au cas par cas.

**9. Note de proximité.** *(facultatif)* La référence de signature EIP-712 et le bot `spread_farming`/
`market_maker` recoupent l'exécution réelle d'ordres maker.

---

## 10. Composio-HQ/polymarket-kalshi-arbitrage-bot — arbitrage Polymarket ↔ Kalshi *(non auditable dans cette session)*

**1. Identité.** [github.com/Composio-HQ/polymarket-kalshi-arbitrage-bot](https://github.com/Composio-HQ/polymarket-kalshi-arbitrage-bot).
**⚠️ Ce dépôt n'a pas pu être récupéré dans cette session** : le proxy Git le refuse (hors du périmètre
de la session, limité à un seul propriétaire), `add_repo` refuse les ajouts inter-propriétaires, et
l'accès web direct renvoie 404/bloqué. Une recherche web ne retrouve pas ce dépôt précis sous
Composio-HQ (nombreux homonymes chez d'autres auteurs) — il a pu être **renommé, archivé, rendu privé ou
supprimé**. **Par honnêteté, je ne décris pas un code que je n'ai pas lu.**

**2. Verdict sécurité : INDÉTERMINÉ (non audité).** Je ne peux pas garantir l'innocuité d'un dépôt que
je n'ai pas pu inspecter. Avertissement de contexte : la catégorie « polymarket-kalshi-arbitrage-bot »
compte de **très nombreux clones homonymes** de qualité et d'intention variables (certains sont des
vitrines renvoyant vers un binaire/Telegram payant). Toute récupération future devra repartir d'un audit
complet.

**3. Ce qu'on peut en dire sans l'avoir lu.** Composio est un éditeur connu d'outillage pour agents IA ;
un tel dépôt serait vraisemblablement une **démonstration** de leur SDK orchestrant un arbitrage entre
Polymarket et Kalshi (détection d'écart de prix sur un même événement, puis exécution des deux jambes).
L'inefficience visée par cette classe d'outils est le **décalage de prix inter-plateformes** sur des
événements équivalents (typiquement marchés BTC courts). Ce paragraphe est **contextuel**, pas un audit.

**4. Recommandation.** Pour obtenir un vrai dossier sur ce dépôt : démarrer une **nouvelle session
ayant ce dépôt comme source initiale** (il sera alors clonable et auditables en lecture seule comme les
autres). Voir aussi, à titre de comparaison de catégorie, les homonymes publics
[ImMike/polymarket-arbitrage](https://github.com/ImMike/polymarket-arbitrage) (Python, surveille
10 000+ marchés) et [TopTrenDev/polymarket-kalshi-arbitrage-bot](https://github.com/TopTrenDev/polymarket-kalshi-arbitrage-bot)
(Rust) — **non audités eux non plus**, cités seulement pour situer la catégorie.

---

# CATÉGORIE 3 — MÉTÉO (dépôts 11 à 15)

---

## 11. AruneshDev/Automated-Trading-System-Kalshi-Weather-Model — projet ML universitaire (Kalshi démo)

**1. Identité.** [github.com/AruneshDev/Automated-Trading-System-Kalshi-Weather-Model](https://github.com/AruneshDev/Automated-Trading-System-Kalshi-Weather-Model).
Auteur : Arunesh Kumar Lal (étudiant). C'est un **rendu de cours** (« CS-542 Principles of Machine
Learning — Common Task Report ») : notebooks Jupyter, tableurs Excel, CSV, captures d'écran, un ZIP,
un rapport. **Ce n'est pas un bot exécutable**, mais une étude ML documentée sur la prédiction de
température, tradée sur la **plateforme démo (papier) de Kalshi**.

**2. Verdict sécurité : DOUTE — identifiants réels commités.** Aucun code malveillant. **Mais** le
dépôt contient un fichier `[credentials].txt` versionné, avec un `client_id`, un `client_secret`, un
`authorization_code` et un `redirect_uri` OAuth (accès API Kalshi démo). Ce sont **les identifiants de
l'étudiant**, pas une menace pour vous — mais c'est un **exemple de très mauvaise hygiène** (secrets
publiés). *À retenir : ne jamais réutiliser ces identifiants, et surtout ne jamais commiter les vôtres.*
Les seuls hôtes externes sont les endpoints OAuth Google/Kalshi (authentification). → sans danger à
lire, mais illustre l'erreur à ne pas faire.

**3. Résumé (2 phrases).** C'est le rapport d'un projet étudiant qui prédit la température maximale de
quatre villes (NYC, Miami, Austin, Chicago) avec des modèles ML (XGBoost) et trade ces prédictions sur
Kalshi en démo. Sa valeur est **pédagogique** (méthode ML de bout en bout), pas opérationnelle.

**4. Fonctionnement de bout en bout.** (a) *Semaine 1* : trading manuel sur Kalshi démo à partir de
prévisions issues de sources en ligne. (b) *Semaine 2* : identification de **cinq sources de données**,
collecte d'historique, entraînement d'un modèle de température max, visualisation prédit vs réel. (c)
*Semaine 3* : automatisation partielle des trades sur la démo. Les notebooks (`Final_Prediction_Model`,
`Xg_boost Training`, `MSE of Settled Trades`) montrent l'entraînement et l'évaluation (erreur MSE sur
les trades réglés). Sortie : `predicted_temperature_max.csv` + graphiques + rapport.

**5. Logique économique.** L'idée exploitée : un modèle météo bien calibré peut battre le prix implicite
d'un marché de température quand ce dernier est mal ajusté. C'est exactement la thèse des marchés météo.
Mais ici tout est en **démo/papier** — aucune preuve de rentabilité réelle, échantillon minuscule
(quatre villes, quelques semaines). « Échoue » dès que la météo est incertaine ou le marché efficient.

**6. Architecture.** Pas d'architecture logicielle : un ensemble de notebooks + données + rapport. Le
« système automatisé » est un notebook qui enchaîne prédiction → passage d'ordre sur l'API démo.

**7. Ce qu'on peut en réutiliser.** (a) La **méthodologie ML** : features météo → XGBoost → prédiction
de température max → comparaison au marché. (b) L'idée de mesurer le **MSE des trades réglés**
(calibration a posteriori). (c) La liste de **cinq sources de données** météo à croiser. Utile comme
brique conceptuelle pour une stratégie météo maison.

**8. Limites & angles morts.** Pas un outil réutilisable (coursework). Identifiants commités
(anti-exemple de sécurité). Kalshi (US), pas Polymarket. Échantillon minuscule, pas de validation
robuste, pas de gestion du risque. Résultats en démo, non transposables tels quels.

**9. Note de proximité.** *(facultatif)* Bon rappel méthodologique pour formaliser une stratégie météo,
sans valeur opérationnelle directe.

---

## 12. yangyuan-zhen/PolyWeather — stack pro d'intelligence météo multi-sources (produit)

**1. Identité.** [github.com/yangyuan-zhen/PolyWeather](https://github.com/yangyuan-zhen/PolyWeather)
(« PolyWeather Pro », site [polyweather.top](https://polyweather.top/)). Le dépôt le plus riche de la
catégorie (~85 Mo) : backend Python, frontend, extension navigateur, `contracts/`, Docker, `CLAUDE.md`,
docs bilingues. **C'est un produit commercial** avec abonnements (Pro 29,9 USDC/mois), points, parrainage
et **checkout on-chain** (contrats Polygon USDC).

**2. Verdict sécurité : SÛR.** Les `subprocess` sont anodins : lancer son propre `bot_listener.py`, et
exécuter `docker logs` dans un panneau d'ops protégé par contrôle d'accès. Les `eval` détectés sont
`model.eval()` (mode évaluation PyTorch) et `EVAL` Redis (Lua serveur) — normaux. Hôtes = services météo
officiels (MGM Turquie, CMA/NMC Chine, JMA Japon, HKO Hong Kong, Wunderground…), Telegram, plus des
**placeholders** (`example.supabase.co`, `rpc-1.example`). Pas d'exfiltration, pas de hook d'installation.
*Réserve non sécuritaire* : c'est un **service payant** — le code est ouvert mais l'usage complet passe
par un abonnement.

**3. Résumé (2 phrases).** PolyWeather est une **station d'intelligence météo temps réel** pour les
marchés de température : elle agrège des dizaines de sources officielles (stations d'aéroport, réseaux
nationaux), calcule des probabilités par tranche de température, et les compare au prix du marché pour
signaler un « edge ». C'est un produit complet (terminal web, extension, alertes Telegram, abonnements
on-chain).

**4. Fonctionnement de bout en bout.** (a) *Ingestion multi-sources* : observations 1-min/10-min de
stations officielles (AMSC/AMOS runway, HKO, JMA AMeDAS, MGM, CMA, CWA…), prévisions (TAF, DEB hourly
consensus), replay via Redis Stream/SSE. (b) *Modélisation* : « DEB hourly consensus » comme trajectoire
horaire préférée + une probabilité gaussienne héritée par tranche (`Gaussian μ` + distribution complète
par bucket). (c) *Signal* : `model probability − market-implied probability` = l'edge ; matching strict
au bucket de marché (exact / range / or-higher / or-lower). (d) *Diffusion* : terminal temps réel
(charts par ville, heure locale), extension navigateur (prévision multi-jours), **pushs Telegram
bilingues** avec température de la piste de règlement. (e) *Monétisation* : abonnements payés en USDC
via contrats Polygon, réconciliation automatique on-chain, dashboard d'ops. *Notions* : **METAR/TAF** =
messages météo aéronautiques standardisés ; **SSE** = flux temps réel serveur→navigateur ; **bucket** =
tranche de température d'un marché.

**5. Logique économique.** Deux niveaux. (1) *Pour le trader* : disposer d'une lecture météo plus fine
et plus rapide que le marché sur les **stations exactes de règlement** (le détail qui fait la différence :
un marché se règle sur une station précise, pas sur « la météo de la ville »). (2) *Pour l'éditeur* :
vendre cet avantage informationnel par abonnement. L'inefficience exploitée = **latence et imprécision
du prix de marché face à l'observation officielle**. « Échoue » si le marché intègre déjà l'info, ou si
la station de règlement diverge du modèle.

**6. Architecture.** `src/` (analyse, modèles, ingestion) · `web/` (backend d'ops, temps réel Redis/SSE)
· `frontend/` (terminal React) · `extension/` (navigateur) · `contracts/` (paiement on-chain) ·
`bot_listener.py` (bot Telegram) · Docker/deploy.

**7. Ce qu'on peut en réutiliser (fort intérêt conceptuel).** (a) L'idée centrale : **modéliser la
station exacte de règlement**, pas la ville — et la liste des réseaux officiels par pays (HKO, JMA,
MGM, CMA, AMOS…). (b) Le calcul d'**edge = proba modèle − proba marché** avec matching strict au bucket.
(c) L'ingestion **TAF/METAR** et le consensus horaire. (d) L'architecture temps réel SSE/Redis pour un
terminal. Beaucoup d'idées transposables, même sans payer l'abonnement.

**8. Limites & angles morts.** Produit **payant/fermé à l'usage** (le code est visible mais l'exploitation
complète passe par l'abonnement et l'infra). Très lourd (Docker, Redis, frontend, contrats). Orienté
villes asiatiques/aéroports. Dépendance à de nombreuses sources externes (fragile si l'une tombe).

**9. Note de proximité.** *(facultatif)* La modélisation « station de règlement exacte » et l'edge
proba-modèle/proba-marché sont directement pertinents pour une stratégie météo.

---

## 13. nicolastinkl/hermes_weatherbot — bot météo autonome (ECMWF + Kelly, auto-apprentissage)

**1. Identité.** [github.com/nicolastinkl/hermes_weatherbot](https://github.com/nicolastinkl/hermes_weatherbot).
« WeatherBet — Powered by Hermes Agent ». Python 3.13, MIT. Trois versions (`bot_v1/v2/v3.py`),
`config.json`, scripts start/stop, tableau de bord de simulation HTML. Se présente comme **vitrine du
framework « Hermes Agent »** (autonomie, auto-apprentissage). Petit et lisible.

**2. Verdict sécurité : SÛR.** Aucun motif de danger, aucun hook d'installation. La clé/wallet est lue
depuis `.env` et sert localement à trader sur le CLOB Polymarket. Hôtes : `weather.visualcrossing.com`
(prévisions), `api.telegram.org` (alertes), `1rpc.io` (RPC public Polygon). Présence d'un dossier
`pip_tmp` (résidu de paquets) — à ignorer, sans risque à la lecture. Rien d'anormal. *Attention d'usage* :
c'est un bot **« fully autonomous »** qui exécute de vrais ordres si on lui donne une vraie clé — la
prudence habituelle s'impose (démarrer en simulation, petite taille).

**3. Résumé (2 phrases).** Ce bot autonome compare la prévision météo (ECMWF/Visual Crossing) à la
probabilité implicite des marchés de température Polymarket sur 6 villes US, calcule une valeur espérée
(EV), et **parie automatiquement** quand l'EV dépasse un seuil. Il ajuste seul sa fraction de Kelly et
son seuil d'EV à partir de l'historique (auto-apprentissage revendiqué).

**4. Fonctionnement de bout en bout.** (a) *Boucle 60 min* : scan des marchés de température des 6 villes
(NYC, Chicago, Miami, Dallas, Seattle, Atlanta). (b) *Signal* : la prévision implique une probabilité ;
si elle diffère du prix, calcul de l'**EV**. (c) *Décision* : pari auto si EV > seuil, taille par
**fraction de Kelly**. (d) *Exécution* : ordre sur le CLOB Polymarket (clé du `.env`), règlement on-chain.
(e) *Auto-apprentissage* : ajuste Kelly et le seuil d'EV selon les résultats passés ; mémoire persistante
des trades. (f) *Contrôle* : alertes et pilotage Telegram. *Notions* : **EV (valeur espérée)** = gain
moyen anticipé d'un pari ; **fraction de Kelly** = règle de dimensionnement optimale selon l'edge et la
probabilité.

**5. Logique économique.** Classique des marchés météo : **un modèle météo peut être mieux calibré que
le marché** sur des échéances courtes ; l'EV positive naît de cet écart. Le dimensionnement Kelly vise à
maximiser la croissance du capital sans se ruiner. « Échoue » si la prévision n'a pas de réel edge
(marché déjà efficient), si Kelly est trop agressif (variance destructrice), ou si l'auto-apprentissage
surapprend un historique court.

**6. Architecture.** `bot_v1/v2/v3.py` (versions successives, v3 = courante) · `config.json` (seuils) ·
`start_bot_v3.sh` / `stop_bot_v3.sh` (lanceurs) · `simulation.json` + dashboard HTML (suivi papier) ·
`data/` (logs d'apprentissage).

**7. Ce qu'on peut en réutiliser.** (a) Le squelette **prévision → EV → Kelly → ordre** clair et lisible,
excellent pour comprendre une stratégie météo de bout en bout. (b) La boucle d'**auto-ajustement de Kelly
et du seuil d'EV** (à regarder de près, mais idée intéressante). (c) L'intégration **Telegram** comme
télécommande. (d) Le mode simulation/dashboard avant le réel.

**8. Limites & angles morts.** « Autonome » = risque si lâché sur un vrai wallet sans surveillance.
Auto-apprentissage sur historique court = surapprentissage probable. Une seule source météo
(Visual Crossing/ECMWF) sans consensus multi-modèles. Pas de modélisation de la **station de règlement
exacte** (contrairement à #12). RPC public partagé (`1rpc.io`) = fragile en charge.

**9. Note de proximité.** *(facultatif)* Montre concrètement le calcul EV + Kelly d'une stratégie météo,
brique réutilisable.

---

## 14. suislanchez/polymarket-kalshi-weather-bot — bot multi-stratégies (GFS 31 membres + BTC 5 min)

**1. Identité.** [github.com/suislanchez/polymarket-kalshi-weather-bot](https://github.com/suislanchez/polymarket-kalshi-weather-bot).
Backend Python (FastAPI) + frontend React, déploiement Railway/Vercel. `RESEARCH.md`,
`VALIDATED_RESEARCH.md`, `ARCHITECTURE.md`. Revendiqué **100 % gratuit à faire tourner** (sources
gratuites, clé Kalshi optionnelle). Deux stratégies : météo **et** BTC 5 min.

**2. Verdict sécurité : SÛR.** L'authentification Kalshi utilise un **chemin de fichier de clé privée**
(`KALSHI_PRIVATE_KEY_PATH`) — c'est la clé RSA d'API Kalshi, standard, qui reste locale. Aucun hook
d'installation, aucune exfiltration. Hôtes : Open-Meteo (GFS), et des API d'échanges crypto publiques
(Coinbase, Kraken, Binance, Bybit, CoinGecko) pour les bougies BTC — toutes en **lecture publique**.
`0.0.0.0` = serveur local. Rien d'anormal.

**3. Résumé (2 phrases).** Ce bot cherche des inefficiences de prix sur deux terrains : les marchés de
**température** (Kalshi KXHIGH + Polymarket) via un **ensemble météo GFS à 31 membres**, et les marchés
**BTC 5 minutes** via l'analyse de microstructure (RSI, VWAP, momentum). Il dimensionne en Kelly
fractionnaire, suit sa calibration au **score de Brier**, et offre un dashboard React + un mode simulation.

**4. Fonctionnement de bout en bout.** (a) *Stratégie météo* : toutes les 5 min, scan des marchés
température ; l'**ensemble GFS 31 membres** (Open-Meteo) estime la probabilité qu'un seuil de température
soit franchi ; trade si l'edge > 8 %. Les marchés Kalshi sont auto-découverts par tickers de série
(`KXHIGHNY`, `KXHIGHCHI`…). (b) *Stratégie BTC 5 min* : toutes les 60 s, bougies 1 min de
Coinbase/Kraken/Binance → RSI, momentum (1/5/15 min), VWAP, croisement SMA, skew → signal composite
pondéré ; trade si edge > 2 %. (c) *Dimensionnement* : Kelly fractionnaire (15 %) avec plafond par trade.
(d) *Calibration* : suivi prédictions vs résultats via **score de Brier**. (e) *Interface* : dashboard
React 3 colonnes + **mode simulation** (bankroll virtuel, courbes d'équité). *Notion* : **ensemble GFS**
= 31 scénarios météo légèrement perturbés donnant une distribution de probabilités ; **score de Brier** =
mesure de la qualité d'une prévision probabiliste.

**5. Logique économique.** Deux inefficiences distinctes. (1) *Météo* : la distribution d'un ensemble à
31 membres estime mieux la proba d'un seuil que le prix de marché — l'edge > 8 % filtre le bruit. (2)
*BTC 5 min* : micro-signaux techniques sur très court terme là où le marché binaire réagit avec latence.
La double plateforme (Kalshi + Polymarket) permet de jouer le même événement là où c'est le mieux
valorisé. « Échoue » si le seuil d'edge est mal calibré (faux positifs), si la latence d'exécution mange
l'edge BTC, ou si l'ensemble est biaisé.

**6. Architecture.** `backend/` (FastAPI : `api/main.py`, `data/kalshi_client.py`, `config.py`,
stratégies) · `frontend/` (React dashboard) · `main.py`/`run.py` (lanceurs) · `Procfile`/`railway.json`/
`vercel.json` (déploiement) · `RESEARCH.md`/`VALIDATED_RESEARCH.md` (justification chiffrée).

**7. Ce qu'on peut en réutiliser (fort intérêt).** (a) L'usage d'un **ensemble GFS 31 membres** pour une
proba de seuil calibrée — plus robuste qu'une prévision unique. (b) Le suivi de calibration au **score de
Brier** (la bonne métrique pour juger un modèle probabiliste). (c) L'**auto-découverte des marchés Kalshi
par tickers de série**. (d) La séparation propre backend/stratégies/dashboard et le mode simulation.
(e) Les fichiers `RESEARCH.md` documentent une démarche de validation.

**8. Limites & angles morts.** Deux stratégies = deux fois plus de surface à valider. La partie BTC 5 min
est très sensible à la latence (difficile à réaliser hors infra rapide). Seuils d'edge (2 %/8 %) à
re-valider soi-même. Kalshi = US (accès/KYC). Pas de modélisation fine de la station de règlement
(comme #12).

**9. Note de proximité.** *(facultatif)* L'ensemble GFS + calibration Brier sont des briques directement
utiles à une stratégie météo rigoureuse.

---

## 15. MoonsatProtocol/Polymarket-Weather-Bot — bot météo Kelly minimaliste (NWS)

**1. Identité.** [github.com/MoonsatProtocol/Polymarket-Weather-Bot](https://github.com/MoonsatProtocol/Polymarket-Weather-Bot).
« Kelly Weather Trading Bot ». TypeScript, petit et net (~1 Mo). `simulation.json`, `config.json`,
`index.html`. Scanne les prévisions **NWS** (service météo US) et simule des trades pour suivre la
performance.

**2. Verdict sécurité : SÛR.** La clé est lue depuis `.env` (`POLYMARKET_PRIVATE_KEY`), validée
(64 hex) et gardée localement ; le proxy wallet est une adresse publique. Le mode par défaut est
**papier** (aucun ordre) ; `--live` lance une **simulation** avec 1 000 $ virtuels. Seul hôte : RPC
Polygon. Aucun hook, aucune exfiltration. Rien d'anormal.

**3. Résumé (2 phrases).** Ce petit bot scanne les prévisions NWS, repère les marchés de température
Polymarket mal évalués et **simule** les trades dans `simulation.json` pour affiner la stratégie avant le
réel. C'est la version épurée et lisible de la stratégie météo + Kelly, idéale pour débuter.

**4. Fonctionnement de bout en bout.** (a) *Données* : prévisions NWS (`api.weather.gov`) pour 6 villes
(NYC, Chicago, Miami, Dallas, Seattle, Atlanta). (b) *Parsing marché* : `parsing.ts` interprète les
questions Polymarket (« X°F or below / or higher / between A-B ») pour en extraire les seuils. (c)
*Signal* : compare la proba issue du forecast au prix ; entre si l'écart dépasse `ENTRY_THRESHOLD`
(0,15), sort à `EXIT_THRESHOLD`, avec fenêtre `MIN_HOURS_TO_RESOLUTION`. (d) *Dimensionnement* : Kelly.
(e) *Sortie* : mode papier (signaux seulement) par défaut ; `--live` = simulation à 1 000 $ écrite dans
`simulation.json`. *Notion* : **NWS** = service météo national américain, données gratuites et fiables.

**5. Logique économique.** Même thèse météo que #13/#14, en plus simple : forecast NWS mieux calibré que
le prix ⇒ edge, dimensionné en Kelly. La valeur du dépôt est sa **clarté** : on voit toute la chaîne en
peu de code. « Échoue » si le marché est efficient, si le parsing des questions rate un format, ou si le
seuil d'entrée est mal réglé.

**6. Architecture.** `src/index.ts` (boucle + validation clé) · `src/config.ts` (config via `.env`) ·
`src/parsing.ts` (extraction des seuils de température depuis la question) · `simulation.json` (journal
de perf) · `index.html` (petit affichage).

**7. Ce qu'on peut en réutiliser.** (a) `parsing.ts` : un **parseur prêt à l'emploi des questions de
température Polymarket** (below/higher/between) — directement utile. (b) Le squelette
**forecast → seuil d'entrée/sortie → Kelly → simulation.json** minimal et clair. (c) Le pattern
« paper par défaut, simulation explicite » comme garde-fou. Excellent point de départ pédagogique.

**8. Limites & angles morts.** Très basique : une seule source (NWS), pas de consensus d'ensemble, pas de
station de règlement fine, pas de gestion du risque au-delà de Kelly. Éditeur « MoonsatProtocol » peu
identifiable. `--live` reste de la simulation — pour du réel, il faudrait brancher l'exécution (et
assumer le risque).

**9. Note de proximité.** *(facultatif)* Le parseur de questions de température et le squelette
forecast→Kelly sont réutilisables tels quels.

---

# CATÉGORIE 4 — IA (dépôts 16 à 20)

---

## 16. TauricResearch/TradingAgents — cadre multi-agents LLM pour l'analyse de marché

**1. Identité.** [github.com/TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents).
Éditeur : Tauric Research (projet reconnu, rapport technique « Trading-R1 » sur arXiv). Python,
pyproject, Docker, CI. **Très actif** (v0.3.1 en 2026-07). Multi-fournisseurs LLM (Claude, GPT, Gemini,
Grok, DeepSeek, Ollama…). Notable : la v0.3.0 a ajouté un **vendor de données Polymarket** et FRED.

**2. Verdict sécurité : SÛR.** Aucun motif de danger, aucun hook d'installation, pas de manipulation de
clé de wallet (ce sont des **clés d'API LLM**, pas des clés on-chain). Mentions explicites de
durcissement sécurité dans le changelog (path-traversal, look-ahead filtering). Code propre et testé.

**3. Résumé (2 phrases).** TradingAgents simule une **salle de marché d'agents IA** : plusieurs LLM jouent
des rôles (analystes, chercheurs, trader, gestionnaire de portefeuille, gestionnaire de risque) qui
débattent d'un actif avant de rendre une décision argumentée. C'est un framework de **raisonnement
collectif** sur une décision de trading, pas un bot d'exécution.

**4. Fonctionnement de bout en bout.** (a) *Données* : le framework agrège des sources (marché, news,
sentiment, fondamentaux, et désormais **Polymarket**, FRED…) via un registre de vendors vérifié. (b)
*Agents spécialisés* : Analyste sentiment (« grounded »), Analyste news, Analyste fondamental, etc.
produisent des lectures structurées. (c) *Débat* : un « Research Manager » arbitre des vues haussière/
baissière ; le « Trader » propose une position ; le « Portfolio/Risk Manager » valide ou tempère. (d)
*Orchestration* : LangGraph (graphe d'agents) avec reprise sur checkpoint, journal de décisions
persistant, budget de retries LLM. (e) *Sortie* : une **décision notée** (échelle à cinq niveaux) avec
son raisonnement. *Notions* : **LangGraph** = bibliothèque pour orchestrer des agents en graphe ;
**agent LLM** = un modèle jouant un rôle avec des outils.

**5. Logique économique.** Ne repose pas sur une inefficience de marché précise : c'est une **méthode de
décision**. L'hypothèse est qu'un débat structuré multi-perspectives réduit les erreurs d'un LLM unique
(biais, hallucination) et produit des thèses mieux étayées. Sa valeur = qualité et traçabilité du
raisonnement. « Échoue » si les agents partagent les mêmes biais (illusion de consensus), si les données
sont mauvaises, ou si l'on confond éloquence et exactitude.

**6. Architecture.** `tradingagents/` (agents, graphe, vendors de données, catalogue de modèles) ·
`cli/` (interface) · `main.py`/`test.py` · Docker · tests/CI. Le registre de vendors (dont Polymarket)
est le point d'extension.

**7. Ce qu'on peut en réutiliser.** (a) Le **pattern « agents en débat »** pour analyser un marché
prédictif (ex. faire raisonner plusieurs perspectives sur un événement Polymarket). (b) Le **vendor de
données Polymarket** déjà intégré = exemple d'accès propre. (c) L'orchestration LangGraph avec reprise et
journal de décisions. (d) L'Analyste sentiment « grounded » (ancré sur des sources) comme brique
anti-hallucination.

**8. Limites & angles morts.** Coûteux en tokens (plusieurs agents par décision). Un débat éloquent n'est
pas une preuve de rentabilité — aucune garantie d'edge. Orienté actions/crypto à l'origine ; l'usage
Polymarket est récent et à éprouver. Ne passe pas d'ordres (c'est de l'analyse, pas de l'exécution).

**9. Note de proximité.** *(facultatif)* Le vendor Polymarket + le pattern de débat pourraient outiller
une lecture qualitative d'événements (ex. incohérences logiques entre marchés).

---

## 17. caiovicentino/polymarket-mcp-server — serveur MCP pour trader Polymarket via Claude (45 outils)

**1. Identité.** [github.com/caiovicentino/polymarket-mcp-server](https://github.com/caiovicentino/polymarket-mcp-server).
Auteur : Caio Vicentino (communautés crypto BR). Python, pyproject, Docker, **très** documenté (des
dizaines de `.md` — ambiance hackathon/« Powered by Claude Code »). Expose **45 outils** MCP en 5
catégories (découverte, analyse, trading, portefeuille, monitoring) + un panneau web de config.

**2. Verdict sécurité : SÛR (outil de trading réel — prudence d'usage).** Vérifié : la clé
`POLYGON_PRIVATE_KEY` **n'apparaît dans aucune requête sortante** (grep vide) ; elle est lue depuis
`.env`, validée (64 hex) et utilisée **localement** par le signer pour signer les ordres CLOB. Un
**`DEMO_MODE=true`** offre un accès lecture seule sans clé. Seuls hôtes contactés : les API Polymarket
(clob/gamma/data) + un CDN (jsdelivr, pour le dashboard). Garde-fous de config présents
(`max_order_size_usd`, `max_total_exposure_usd`). *Réserve d'usage* : c'est un **outil de trading en
argent réel piloté par un LLM** — donner une vraie clé à un agent qui peut `place_order`/`cancel` exige
des plafonds stricts, des tests en `DEMO_MODE`, et une grande prudence.

**3. Résumé (2 phrases).** Ce serveur MCP branche Polymarket sur Claude : on demande en langage naturel
d'analyser un marché, de voir ses positions ou de passer/annuler des ordres, et Claude appelle l'un des
45 outils correspondants. C'est le **pont IA ↔ trading** le plus directement opérationnel du lot pour
Polymarket.

**4. Fonctionnement de bout en bout.** (a) *Protocole MCP* : le serveur expose des « outils » que Claude
peut appeler (Model Context Protocol). (b) *Lecture* (sans clé, `DEMO_MODE`) : `get_markets`,
`get_market`, `get_orderbook`, `get_price` — découverte et analyse via Gamma/CLOB/Data. (c)
*Authentification* : avec `POLYGON_PRIVATE_KEY`, `create_api_credentials`/`get_client` construisent un
client CLOB signant localement. (d) *Trading* : `place_order`, `cancel_order`, `cancel_all_orders`,
`get_orders`, `get_positions`, `get_balance` — passage et gestion d'ordres réels. (e) *Monitoring* :
WebSocket temps réel + dashboard web de config (plafonds d'exposition). *Notion* : **MCP (Model Context
Protocol)** = standard permettant à un assistant IA d'utiliser des outils externes de façon structurée.

**5. Logique économique.** N'a pas d'edge propre : c'est un **exécuteur** qui rend n'importe quelle
stratégie actionnable en langage naturel depuis Claude. Sa valeur = vitesse d'itération (analyser →
décider → agir sans coder chaque appel). Le **risque** est symétrique : un LLM qui se trompe peut passer
un mauvais ordre réel — d'où l'importance des plafonds et du `DEMO_MODE`. « Échoue » par erreur d'agent
plus que par erreur de marché.

**6. Architecture.** `src/polymarket_mcp/auth/` (`signer.py` = signature locale, `client.py` = client
CLOB + méthodes marché/ordres/positions) · `config.py` (validation clé, `DEMO_MODE`, plafonds) ·
`web/` (dashboard de config) · monitoring WebSocket · nombreux `.md` de doc.

**7. Ce qu'on peut en réutiliser (fort intérêt opérationnel).** (a) Un **exemple complet et lisible de
client CLOB signé** (auth/credentials/signer) — référence précieuse pour l'exécution réelle. (b) Le
découpage en **45 outils** documente exactement toutes les opérations Polymarket disponibles. (c) Le
pattern **`DEMO_MODE` + plafonds d'exposition** comme garde-fous. (d) Le monitoring WebSocket. À étudier
d'abord en lecture seule.

**8. Limites & angles morts.** Sur-documentation « hackathon » (qualité de code à vérifier au-delà des
`.md`). Trading réel piloté par LLM = **risque opérationnel élevé** : à n'activer qu'avec des plafonds
serrés et après tests `DEMO_MODE`. Dépend de la stabilité de l'API CLOB. Auteur/communauté à évaluer
avant de confier une clé.

**9. Note de proximité.** *(facultatif)* C'est le pont le plus direct pour piloter Polymarket depuis
Claude ; la référence de signature CLOB est réutilisable pour l'exécution réelle.

---

## 18. mvanhorn/last30days-skill — skill IA de veille « 30 derniers jours » (signaux sociaux)

**1. Identité.** [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill).
Auteur : mvanhorn. C'est un **Agent Skill** (installable dans Claude Code, Cursor, Copilot, Gemini CLI…
via marketplace). Python (pyproject, uv.lock), pipeline « v3 », `SKILL.md` comme source de vérité,
intégration Hermes/MCP. Se décrit comme « moteur de recherche piloté par un agent, noté par les upvotes,
les likes et l'argent réel — pas par des éditeurs ».

**2. Verdict sécurité : SÛR — avec CAUTION vie privée.** Aucune exfiltration : le point sensible est
`scripts/lib/chrome_cookies.py`, qui **extrait localement** les cookies des navigateurs Chromium
(déchiffrement via le Keychain macOS) pour **s'authentifier à X/Twitter** (`xurl_x.py`) et récupérer des
contenus récents. **Les cookies ne sont envoyés nulle part à l'extérieur** (grep d'envoi réseau vide) —
ils servent uniquement, en local, à appeler X avec votre session. Ce n'est pas malveillant, **mais lire
la session de votre navigateur est intrusif** : à n'installer qu'en connaissance de cause, idéalement
avec un compte X dédié. Nombreux `subprocess` = appels à des outils locaux (openssl, xurl) — normaux.

**3. Résumé (2 phrases).** Cette skill produit, à la demande d'un agent, un **panorama des 30 derniers
jours** sur un sujet en interrogeant les signaux sociaux réels (X, upvotes, likes) plutôt que des articles
éditoriaux. Elle vise l'information fraîche et « ce que les gens pensent maintenant », utile pour un
événement de marché prédictif.

**4. Fonctionnement de bout en bout.** (a) *Déclenchement* : commande `/last30days <sujet>` dans un hôte
d'agent. (b) *Authentification sociale* : `chrome_cookies.py` récupère localement les cookies de session
(X) du navigateur ; `xurl_x.py` s'en sert pour requêter X. (c) *Collecte & scoring* : agrège les contenus
récents et les **pondère par signaux réels** (upvotes, likes, « argent réel »), pour trier le pertinent
du bruit. (d) *Restitution* : un rapport de tendance des 30 derniers jours. Pipeline « v3 » décrit dans
`SKILL.md`. *Notion* : **Agent Skill** = capacité empaquetée qu'un assistant IA peut invoquer ; **xurl** =
outil d'appel de l'API X.

**5. Logique économique.** Indirecte : sur un marché prédictif, **l'information récente et le sentiment
social** peuvent précéder le prix. Un flux de veille fraîche, filtré par des signaux réels, aide à repérer
un basculement d'opinion avant qu'il ne soit pleinement price-in. « Échoue » si les signaux sociaux sont
bruités/manipulés (bots, hype), ou si le sujet est peu discuté publiquement.

**6. Architecture.** `skills/last30days/` (le cœur : `SKILL.md`, `scripts/` avec `lib/chrome_cookies`,
`xurl_x`, `corpus`, `env`, `subproc`…) · `mcp/` (intégration) · `hooks/`, `fixtures/`, `tests/`, docs.

**7. Ce qu'on peut en réutiliser.** (a) L'idée d'une **veille sociale scorée par engagement réel** comme
signal amont d'un marché d'événement. (b) Le format **Agent Skill** portable (installable dans Claude
Code) comme modèle pour empaqueter ses propres outils. (c) La mécanique d'agrégation + scoring de corpus.
À reprendre en étant conscient du volet cookies.

**8. Limites & angles morts.** Accès aux **cookies du navigateur** = friction et risque vie privée (compte
X dédié recommandé). Dépend de l'accès à X (fragile si l'API change). Signaux sociaux manipulables.
Pertinence variable selon le sujet. Pas un outil de trading — un outil d'information amont.

**9. Note de proximité.** *(facultatif)* Pourrait alimenter une lecture qualitative d'événements
d'actualité tradés sur Polymarket.

---

## 19. pydantic/pydantic-ai — framework de construction d'agents IA (Pydantic)

**1. Identité.** [github.com/pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai).
Éditeur : **Pydantic** (l'équipe derrière la librairie de validation Python la plus utilisée). MIT,
énorme base de code testée, docs pro ([ai.pydantic.dev](https://ai.pydantic.dev/)). Standard de
l'industrie, très haute confiance. « GenAI Agent Framework, the Pydantic way. »

**2. Verdict sécurité : SÛR.** Les motifs `base64.b64decode` détectés sont **tous légitimes** : décodage
d'images et de contenus binaires MCP (protocole d'outils), pas d'obfuscation. Aucun hook d'installation
malveillant, pas de manipulation de clé on-chain. Projet de référence, maintenu par une équipe reconnue,
CI complète. Le plus fiable du lot.

**3. Résumé (2 phrases).** Pydantic AI est une **boîte à outils pour construire des agents IA fiables**
en Python : définir des outils typés, valider les entrées/sorties d'un LLM, et orchestrer des workflows
« qualité production ». C'est une **fondation d'ingénierie**, pas un bot de trading.

**4. Fonctionnement de bout en bout.** (a) *Définition d'agent* : on déclare un agent, ses outils
(fonctions Python) et le **schéma typé** de ses sorties. (b) *Validation* : Pydantic garantit que ce que
le LLM renvoie respecte la structure attendue (sinon rejet/reprise) — fiabilité accrue. (c)
*Multi-modèles* : support de nombreux fournisseurs (Claude, OpenAI, Google…) via une interface unifiée.
(d) *Graphes & évals* : `pydantic_graph` (workflows) et `pydantic_evals` (tests d'agents). (e) *Sortie* :
des applications d'agents robustes et testables. *Notion* : **sortie typée/validée** = on force le LLM à
répondre dans un format vérifiable, ce qui réduit drastiquement les erreurs d'intégration.

**5. Logique économique.** Aucune directe : c'est un **socle technique**. Sa valeur = fiabiliser et
accélérer la construction de tout agent (analyse, recherche, exécution) qu'on voudrait bâtir soi-même,
avec des garanties de structure. « Échoue » seulement comme choix d'ingénierie (courbe d'apprentissage,
dépendance à un framework).

**6. Architecture.** `pydantic_ai_slim/` (le cœur : agents, modèles, MCP, messages) · `pydantic_graph/`
(orchestration de workflows) · `pydantic_evals/` (évaluation d'agents) · `clai/` (CLI) · `examples/`,
`docs/`, tests exhaustifs.

**7. Ce qu'on peut en réutiliser.** (a) Le **framework lui-même** pour bâtir proprement un agent maison
(ex. un analyste d'événements Polymarket à sorties typées). (b) Le pattern de **sortie validée** comme
garde-fou anti-hallucination. (c) `pydantic_evals` pour **tester** un agent de façon reproductible. (d)
L'intégration MCP native (se marie avec le serveur #17). Base solide pour tout ce qui est « agent ».

**8. Limites & angles morts.** Ce n'est **pas** une solution clé en main : il faut coder l'agent. Sans
rapport avec le trading en soi — c'est de l'outillage. Framework en évolution rapide (API qui bouge).
Overkill pour un simple script.

**9. Note de proximité.** *(facultatif)* Serait le socle propre pour construire un agent d'analyse maison
à sorties fiables.

---

## 20. assafelovic/gpt-researcher — agent de recherche autonome (rapports sourcés)

**1. Identité.** [github.com/assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher).
Auteur : Assaf Elovic. Projet **très populaire et mature** (multi-langues, Docker, SECURITY.md, évals,
`deep_agents`). MIT. « The first open deep research agent » — recherche web et locale, rapports factuels
**avec citations**.

**2. Verdict sécurité : SÛR.** Motifs anodins : un `base64.b64decode` pour la génération d'images, un
`subprocess.run` dans le **runner d'évaluations**. Aucune manipulation de clé on-chain, pas de hook
d'installation malveillant. Projet reconnu avec politique de sécurité. Haute confiance.

**3. Résumé (2 phrases).** GPT Researcher mène une **recherche approfondie autonome** sur un sujet :
il planifie, interroge de nombreuses sources web (et locales), recoupe, puis rédige un **rapport détaillé,
factuel et sourcé** avec citations. Il vise vitesse, déterminisme et réduction des hallucinations par le
travail parallèle d'agents.

**4. Fonctionnement de bout en bout.** (a) *Planification* (Plan-and-Solve) : décompose la question en
sous-questions. (b) *Recherche parallèle* : plusieurs agents interrogent des moteurs/sources
simultanément (web + documents locaux via RAG), scrapent et extraient. (c) *Recoupement* : agrège,
déduplique, hiérarchise l'information par pertinence et fiabilité. (d) *Rédaction* : produit un rapport
long et structuré **avec citations** (traçabilité des sources). (e) *Extensibilité* : `deep_agents`,
évals, suivi de coûts (ex. tracking Anthropic). *Notions* : **RAG (Retrieval-Augmented Generation)** =
donner au LLM des documents récupérés pour qu'il réponde sur des faits plutôt que de mémoire ;
**agent autonome** = enchaîne recherche/lecture/synthèse sans intervention.

**5. Logique économique.** Indirecte : sur un marché prédictif, une **recherche factuelle rapide et
sourcée** sur un événement (contexte, base rates, signaux récents) améliore la qualité d'une thèse.
La valeur = compresser des heures de recherche en minutes, avec citations vérifiables. « Échoue » si les
sources sont mauvaises/biaisées, ou si l'on prend le rapport pour une vérité sans vérifier les citations.

**6. Architecture.** `gpt_researcher/` (cœur : agents, providers LLM, retrievers, scrapers) · `backend/`
(API/serveur) · `deep_agents/` (agents avancés) · `cli.py` (ligne de commande) · `evals/` (évaluation) ·
Docker/fullstack · docs multi-langues.

**7. Ce qu'on peut en réutiliser (fort intérêt).** (a) L'agent tel quel pour **produire une note de
recherche sourcée sur un événement** avant de trader (contexte, précédents, dernières nouvelles). (b) Les
**retrievers/scrapers** et le pattern de recherche parallèle. (c) Le **suivi de coûts** LLM. (d)
L'exigence de **citations** comme discipline anti-hallucination. Directement utile pour la phase « je
comprends avant de décider ».

**8. Limites & angles morts.** Consomme des tokens et des appels de recherche (coût). Qualité tributaire
des sources et des moteurs branchés. Ne trade pas — c'est un outil de **compréhension**, pas de décision
automatique. Vérifier les citations reste nécessaire (un rapport bien écrit peut citer une source faible).

**9. Note de proximité.** *(facultatif)* Colle exactement à la méthode « décortiquer un sujet avec une IA,
comprendre avant de décider ».

---

# TABLEAU DE SYNTHÈSE — 20 dépôts

| # | Dépôt | Sécurité | Catégorie | En 5 mots | Verdict |
|---|---|---|---|---|---|
| 1 | SII-WANGZJ/Polymarket_data | 🟢 SÛR | Analytics | Dataset on-chain 107 Go complet | **EXPLOITER** |
| 2 | evan-kolberg/prediction-market-backtesting | 🟢 SÛR | Analytics | Backtest Nautilus, 15 stratégies | **EXPLOITER** |
| 3 | ent0n29/polybot | 🟢 SÛR | Analytics | Infra MM + réplication traders | **EXPLOITER** |
| 4 | pmxt-dev/pmxt | 🟡 SÛR* | Analytics | API unifiée multi-plateformes | **INSPIRER** |
| 5 | txbabaxyz/collectmarkets2 | 🟢 SÛR | Analytics | Collecteur CSV d'un wallet | **INSPIRER** |
| 6 | alsk1992/CloddsBot | 🟡 DOUTE usage | Bots | Terminal agentique IA multi-chaînes | **INSPIRER** |
| 7 | lihanyu81/polymarket_lp_tool | 🟢 SÛR | Bots | Récompenses liquidité + anti-sniping | **EXPLOITER** |
| 8 | MrFadiAi/Polymarket-bot | 🟢 SÛR | Bots | Copy-trading + arbitrage, risque | **EXPLOITER** |
| 9 | HarrierOnChain/…Toolkits | 🟡 SÛR* | Bots | Moteur Rust, 10 stratégies | **INSPIRER** |
| 10 | Composio-HQ/…kalshi-arbitrage | ⚪ NON AUDITÉ | Bots | Arbitrage Polymarket↔Kalshi (inaccessible) | **—** |
| 11 | AruneshDev/…Kalshi-Weather | 🟡 DOUTE (secrets commités) | Météo | Projet ML universitaire, démo | **INSPIRER** |
| 12 | yangyuan-zhen/PolyWeather | 🟢 SÛR* | Météo | Station météo pro multi-sources | **EXPLOITER** |
| 13 | nicolastinkl/hermes_weatherbot | 🟢 SÛR | Météo | Bot autonome ECMWF + Kelly | **INSPIRER** |
| 14 | suislanchez/…kalshi-weather-bot | 🟢 SÛR | Météo | GFS 31 membres + BTC | **EXPLOITER** |
| 15 | MoonsatProtocol/…Weather-Bot | 🟢 SÛR | Météo | Météo NWS + Kelly minimaliste | **INSPIRER** |
| 16 | TauricResearch/TradingAgents | 🟢 SÛR | IA | Multi-agents LLM d'analyse | **INSPIRER** |
| 17 | caiovicentino/polymarket-mcp-server | 🟢 SÛR* | IA | Trader Polymarket via Claude | **EXPLOITER** |
| 18 | mvanhorn/last30days-skill | 🟡 SÛR (cookies) | IA | Veille sociale 30 jours | **INSPIRER** |
| 19 | pydantic/pydantic-ai | 🟢 SÛR | IA | Framework d'agents IA fiables | **INSPIRER** |
| 20 | assafelovic/gpt-researcher | 🟢 SÛR | IA | Recherche autonome sourcée | **EXPLOITER** |

**Légende sécurité :** 🟢 SÛR · 🟡 SÛR* = sûr mais avec une réserve d'usage (tiers, service payant,
cookies, funnel) · 🟡 DOUTE = point à corriger/comprendre avant usage · ⚪ non audité (inaccessible dans
cette session). *Aucun dépôt classé DANGER : aucun drainer, aucune exfiltration de clé n'a été détectée
dans les 19 dépôts lisibles.*

**Rappels de sécurité transversaux :**
1. **pmxt (#4)** : ne jamais utiliser le **mode hosted** avec une clé qui détient des fonds (elle part
   chez pmxt) — mode signature locale uniquement.
2. **CloddsBot (#6)** : surface d'attaque énorme (postinstall exécutant du code, skills lançant du shell,
   clés multi-chaînes) — **à étudier, pas à exécuter** près du vrai wallet.
3. **Toolkits (#9)** : code sûr, mais **funnel Telegram vers un service géré/copy-trading** — ne jamais
   confier clés ou fonds à ce tiers.
4. **Kalshi-Weather (#11)** : contient des **identifiants OAuth commités** (démo) — anti-exemple ; ne pas
   réutiliser, et ne jamais commiter les vôtres.
5. **poly_mcp (#17)** : trading réel piloté par LLM — n'activer qu'avec **plafonds stricts** et après
   tests en **`DEMO_MODE`**.
6. **last30days (#18)** : lit les **cookies de votre navigateur** (localement, non exfiltrés) pour
   accéder à X — compte X dédié recommandé.
7. **Règle générale** : tous ces bots signent avec une clé lue depuis `.env`. Un wallet **dédié**, à
   solde minimal, séparé du wallet principal, est la précaution de base pour tout test.

---

# TOP 5 — les dépôts les plus intéressants (tous usages confondus)

Classement par **valeur propre** (qualité, profondeur, réutilisabilité), indépendamment de toute
stratégie particulière.

### 🥇 1. ent0n29/polybot (#3) — la mine d'or « rétro-ingénierie + market making »
Ce qui le rend remarquable : au-delà d'un simple bot, il apporte deux choses rares et précieuses — un
**score de réplication** pour distinguer les traders talentueux des chanceux, et un **modèle de
probabilité d'exécution d'un ordre maker** (`calibrate_maker_fill_model.py`), qui est *la* question que
tout poseur d'ordres se pose. S'y ajoutent une vraie architecture de market making (inventaire, sizing,
bankroll, complete-set) et un pipeline data sérieux (ClickHouse). Lourd à opérer, mais l'or est dans les
**idées et le code de `research/`**, lisibles sans rien lancer.

### 🥈 2. evan-kolberg/prediction-market-backtesting (#2) — l'outil qui évite de perdre
Remarquable par sa maturité (bâti sur NautilusTrader, très actif) et surtout par sa **bibliothèque de
15 stratégies déjà écrites** — un catalogue d'inefficiences à comprendre une par une
(`binary_pair_arbitrage`, `microprice_imbalance`, `panic_fade`, `final_period_momentum`…). C'est
l'infrastructure qui permet de **tester avant de risquer du capital**, avec une modélisation fine des
frais et du carnet. Un backtest rigoureux est ce qui sépare une intuition d'une stratégie.

### 🥉 3. lihanyu81/polymarket_lp_tool (#7) — la réponse concrète à l'adverse selection
Remarquable parce qu'il traite **le** risque n°1 du farming de récompenses de liquidité :
l'anti-sniping. Sa logique explicite (pause sur saut de midpoint, mid filtré EMA/médiane, cooldown
post-exécution, distance de repricing max) est exactement la brique qui manque à une analyse purement
théorique des récompenses. Petit, ciblé, lisible, en Python **et** Rust — pédagogique et directement
utile.

### 4. caiovicentino/polymarket-mcp-server (#17) — le pont IA ↔ Polymarket le plus opérationnel
Remarquable comme **exécuteur** : 45 outils qui rendent Polymarket pilotable en langage naturel depuis
Claude, avec une **référence complète de client CLOB signé localement**, un `DEMO_MODE` lecture seule et
des plafonds d'exposition. C'est le chaînon manquant entre « analyser avec une IA » et « agir », à
condition d'une prudence stricte (plafonds, démo d'abord). La référence de signature est réutilisable
même sans adopter tout le serveur.

### 5. assafelovic/gpt-researcher (#20) — comprendre vite et bien, avec sources
Remarquable par sa maturité et son utilité transversale : il produit une **recherche approfondie,
factuelle et sourcée** sur n'importe quel sujet en minutes. Il colle exactement à la démarche
« décortiquer un sujet avec une IA, comprendre avant de décider » : contexte d'un événement, précédents,
signaux récents — le tout **avec citations vérifiables**, ce qui discipline contre l'hallucination.

**Mentions honorables :** *PolyWeather (#12)* pour l'idée cruciale de modéliser la **station de règlement
exacte** ; *SII-WANGZJ/Polymarket_data (#1)* comme **matière première** on-chain de tout backtest sérieux ;
*Polymarket-bot (#8)* pour sa **gestion du risque à 4 couches** réutilisable partout.

---

*Fin du rapport. 19 dépôts audités en lecture seule (aucun exécuté) ; le 20ᵉ (Composio-HQ) n'était pas
accessible dans cette session et n'a donc pas été audité — voir sa fiche pour la marche à suivre.*
