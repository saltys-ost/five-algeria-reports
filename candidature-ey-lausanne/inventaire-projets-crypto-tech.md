# Inventaire des projets crypto / tech exploitables en candidature

Relevé le 18 octobre 2026 à partir de tes sessions Claude Code (juin à octobre 2026), de tes trois dépôts GitHub
(`five-algeria-reports`, `polymarket-research`, `five-algeria`) et des fichiers qu'ils contiennent. Chaque fiche donne :
ce que c'est, les faits vérifiables que tu peux défendre en entretien, une formulation prête pour un CV, l'angle pour
une lettre, et les réserves.

Règle de présentation, valable partout : ces projets sont présentés comme de l'**analyse, de la vérification et de la
recherche**, jamais comme du trading. Un recruteur audit retient « rigueur de preuve, données sourcées, hypothèses
réfutées », pas « stratégie gagnante ». Tous ont été construits avec l'aide de Claude Code : en entretien, dis-le
simplement (« conçu et piloté avec un assistant de code ») et sois capable d'expliquer chaque chiffre.

---

## Niveau 1 : à mettre dans la candidature EY Genève (Services Financiers, actifs numériques)

### 1. Environnement de recherche autonome Polymarket (juil. – oct. 2026)

**Ce que c'est.** Un système complet de recherche sur un marché de prédiction décentralisé (Polymarket, blockchain
Polygon) : collecteur de données 24 h/24 sur un serveur Linux (carnets d'ordres, transactions, cotations, prix spot
Binance et Chainlink), base SQLite + Parquet compactée chaque nuit, tableau de bord privé, bot Telegram de rapport
matinal, et un « chercheur » nocturne qui formule des hypothèses, les teste en papier et consigne tout dans des fichiers
versionnés. Dépôt privé `polymarket-research` : 509 fichiers Python, environ 48 000 lignes, 37 hypothèses numérotées
(H-001 à H-037), un journal de décisions daté, un fichier d'errata.

**Faits vérifiables.**
- Univers mesuré : 12 139 événements actifs, 3 511 issues de carnets analysées (rapports 00 à 10, juillet 2026).
- Suivi 24 h de 15 marchés, suivi temps réel WebSocket de 45 marchés sur 4 h, 91 fenêtres détectées dont 45 nettes de frais.
- Étude de persistance de performance de wallets (corrélation de rang 0,15 : pas de persistance).
- Audit de sécurité en lecture seule de 20 dépôts open source avant toute utilisation (exfiltration de clés, code
  obfusqué, hooks d'installation), verdict par dépôt.
- Hypothèses rejetées par les données et documentées comme telles (H-005, H-009 : artefact du filtre d'exécutabilité
  détecté par un témoin placebo). Une hypothèse retenue puis déclassée quand l'échantillon a grandi (H-021).
- Règles non négociables écrites dans le brief : aucune clé privée sur la machine, aucun ordre réel, mémoire en fichiers
  texte, chaque chiffre avec sa provenance (mesuré / calculé / hypothèse).

**Formulation CV (2 lignes).** « Recherche quantitative sur un marché de prédiction décentralisé (Polymarket, Polygon) :
collecte 24 h/24 de carnets d'ordres et transactions, 37 hypothèses testées en papier avec seuil et date limite, chaque
résultat documenté avec sa provenance ; audit de sécurité de 20 dépôts open source avant usage. »

**Angle lettre.** La discipline de preuve : données sourcées, hypothèses falsifiables, résultats négatifs publiés,
traçabilité. C'est le vocabulaire de l'audit appliqué à des transactions on-chain.

**Réserves.** Ne mentionne ni capital engagé, ni « lot 4 exécuteur », ni clé privée : le projet s'arrête au papier. Si on
te demande « vous avez gagné de l'argent ? », la bonne réponse est « ce n'était pas l'objet : l'objet était de savoir si
une hypothèse tenait face aux données, et la plupart ne tenaient pas ».

### 2. Dossier d'analyse « MicroStrategy contre Bitcoin » (oct. 2026)

**Ce que c'est.** Un rapport d'analyse financière d'une société cotée dont le bilan est adossé au bitcoin : thèse en
clair, structure financière (dette convertible, actions privilégiées), historique depuis août 2020, année 2026, charges
et couverture, tests de résistance, grille d'invalidation (seuils vert / orange / rouge), comparaisons, routine de
suivi, « ce qu'on ne sait pas ». Rendu en page HTML à onglets avec scripts de calcul et données brutes.

**Faits vérifiables.**
- Indicateur central : mNAV (capitalisation / valeur des bitcoins détenus), médiane 1,52× depuis 2024, décomposition
  du rendement entre hausse du BTC par action et variation de la prime.
- Analyse de gouvernance (part des votes du fondateur, concentration des dépositaires : 41,5 / 38,6 / 19,9 %).
- Une passe de vérification de 34 contrôles en annexe, avec marquage des chiffres non retrouvés dans une source ouvrable.

**Formulation CV.** « Analyse financière d'une société cotée adossée au bitcoin (MicroStrategy) : structure de
financement, mNAV, tests de résistance, grille d'invalidation chiffrée, 34 contrôles de sources en annexe. »

**Angle lettre.** C'est exactement un sujet d'audit Services Financiers avec actifs numériques : comment évaluer et
contrôler un bilan dont l'actif principal est un crypto-actif. Si ton mémoire professionnel Audencia (M2, soutenance
juin 2027) n'est pas encore fixé, ce sujet est un candidat sérieux, et le dire dans la lettre a du poids.

**Réserves.** Présente-le comme une analyse de risque et de valorisation, pas comme une recommandation d'achat.

### 3. Poste de pilotage dérivés BTC : liquidations Hyperliquid et options Deribit (sept. 2026)

**Ce que c'est.** Un moteur de collecte et de calcul (orchestrateur à cadence variable, FastAPI, Parquet) qui
reconstruit la carte des liquidations à partir des positions réelles publiées par Hyperliquid, suit les ordres de
protection, et calcule les grecques et le profil d'exposition gamma des options Deribit. Tableau de bord privé, jamais
exposé sur internet.

**Faits vérifiables.**
- Validation des grecques contre Deribit sur 50 options, zéro désaccord ; deux pièges documentés (delta brut, arrondis).
- Bug de signe trouvé par un test (le charm), golden test sur une chaîne figée et ses 22 mesures, 38 tests automatisés.
- Carte des liquidations : 4 000 comptes interrogés par cycle, couverture mesurée (31 % à 300 comptes, 62 % à 4 000),
  taux de couverture toujours affiché, et un correctif pour dire explicitement ce que la fenêtre ±30 % laisse dehors
  (1 069 positions, 1,59 milliard de dollars).
- Trois erreurs d'unités détectées et corrigées chez un fournisseur de données (open interest, taux, période de règlement).

**Formulation CV.** « Outil de suivi des risques sur dérivés bitcoin : reconstruction des liquidations à partir de
positions réelles (Hyperliquid), grecques d'options validées contre Deribit sur 50 options, tests automatisés, taux de
couverture affiché sur chaque mesure. »

**Angle lettre.** « Une valeur sans son âge n'est pas une information » : chaque donnée porte sa source et son heure.
Honnêteté des données, détection d'erreurs de fournisseur. Très bon exemple de « contrôle de cohérence ».

### 4. Simulateur de rentabilité d'un produit de crédit DeFi (ether.fi Cash, sept. 2026)

**Ce que c'est.** Application locale qui compare sur 36 ou 48 mois quatre façons de payer ses dépenses (carte bancaire
classique contre carte adossée à un collatéral crypto, avec cashback, intérêts, rendement du collatéral et risque de
liquidation), scénarios fixes et Monte Carlo à 10 000 trajectoires. Chaque paramètre porte un statut (confirmé /
vérifié / défaut / inconnu), sa source et sa date.

**Faits vérifiables.**
- Onze vérifications publiques V1 à V11 (help center, dépôt public du protocole, appels `eth_call` sur RPC publics,
  API de devis), avec niveau de confiance et, quand deux sources se contredisent, les deux montrées.
- Plusieurs incohérences relevées dans la documentation officielle du protocole (tableau d'adresses Optimism avec des
  adresses Scroll, devise du cashback contradictoire, seuils de liquidation non documentés lus on-chain).
- Moteur de liquidation testé sur l'exemple officiel (chute de 30 % : liquidation partielle, 35 % : totale).
- Aucune transaction, aucun wallet connecté : lecture seule.

**Formulation CV.** « Modèle de rentabilité et de risque d'un produit de crédit adossé à des actifs numériques :
onze vérifications de paramètres contre la documentation et la chaîne, incohérences documentaires relevées, moteur de
liquidation testé, Monte Carlo 10 000 trajectoires. »

**Angle lettre.** Confronter la documentation d'un acteur à ce que la chaîne dit réellement, c'est une procédure
d'audit. À citer si tu veux un exemple de « contrôle sur pièces » appliqué à la DeFi.

### 5. Radar de tokens : lecture fondamentale des protocoles (oct. 2026)

**Ce que c'est.** Un screener de protocoles crypto fondé sur leurs revenus : frais sur 30 jours, revenus annualisés,
part des frais conservée, « mois de frais » (capitalisation / frais), rachats et destructions de tokens avec un système
de preuve (mesuré, estimé, on-chain, par règle), archive d'offre sur 7 jours pour suivre les destructions, glossaire.
Sources : DefiLlama, CoinGecko, DexScreener. Tests automatisés (17 tests).

**Formulation CV.** « Screener fondamental de protocoles crypto : frais, revenus, rachats et destructions de tokens
avec niveau de preuve par donnée, détection d'offres instables, tests automatisés. »

**Angle lettre.** Lire un protocole comme une entreprise (chiffre d'affaires, part conservée, retour aux porteurs) et
exiger une preuve pour chaque annonce de rachat. Bon complément de la fiche 2.

**Réserves.** Utilise « analyse fondamentale », jamais « sous-évalué » ou « à acheter ».

---

## Niveau 2 : à utiliser seulement pour un poste fintech, data ou quant (pas pour un Big 4 audit)

Ces projets sont solides mais portent le mot « trading » sur le front. Pour EY Audit, ils affaibliraient le
positionnement « auditeur » que le reste du dossier construit. Pour une fintech, une plateforme crypto ou un fonds, ils
deviennent des atouts.

### 6. Plateforme de backtesting et campagne de recherche d'edge (juin – juil. 2026)

Plateforme locale de replay et de backtest (FastAPI, JavaScript, DuckDB), 120 tests automatisés, protocole de recherche
in-sample / out-of-sample avec témoin, stress de glissement ×2 et corroboration sur six instruments. Conclusion écrite :
aucun avantage statistique confirmé. C'est le point à retenir : une campagne qui conclut « non » honnêtement.

**Formulation (fintech).** « Harnais de backtest avec protocole IS/OOS, témoin et stress ; conclusion négative
documentée sur six instruments. »

### 7. OF Radar : scanner d'order flow sur perpétuels crypto (juil. 2026)

Radar qui qualifie des contextes (régimes prix × open interest, vérifications de carnet, détection de basis) et mesure
le taux de réussite de chaque setup après coup. Explicitement « un radar, pas un robot » : 47 tests, aucune exécution.

### 8. Indicateurs TradingView en Pine Script (juil. et sept. 2026)

VWAP multi-jours glissant paramétrable (quatre fenêtres, toute unité de temps), publié dans ce dépôt avec un mode
d'emploi ; indicateur ICT/SMC audité et corrigé. Preuve de capacité à écrire du code de calcul financier propre.

---

## Niveau 3 : hors crypto, utiles pour une ligne « projets » ou un entretien

### 9. Étude de faisabilité d'un centre de football à 5 à Alger (juil. – sept. 2026)

Dépôt `five-algeria` : étude de faisabilité, dossier de financement ANADE à trois associés, simulation du dossier,
synthèse partageable. Montre la modélisation financière d'un projet réel et la lecture d'un cadre administratif
étranger. Pour un recruteur, c'est de l'entrepreneuriat chiffré, sans lien crypto.

### 10. Business plan de citernes d'eau en Guadeloupe (juil. 2026)

Même registre : hypothèses de prix, apport, volumes. Une ligne au plus, si tu veux une rubrique « projets
entrepreneuriaux ».

### 11. Outils de révision Audencia (sept. – oct. 2026)

Site de révision avec fiches, QCM et flashcards (11 chapitres, 175 QCM, 79 flashcards), révisions DSCG marché
financier. Pas pour un CV, mais une bonne anecdote d'entretien sur ta façon d'apprendre et d'outiller ton travail.

Sans intérêt pour une candidature : stratégie vidéo IA, dépannage PC, questions juridiques ou automobiles personnelles,
et l'activité d'investissement personnelle (bourse, DeFi, DCA), à ne jamais faire figurer.

---

## Comment les intégrer sans surcharger

- **CV EY Genève** : une rubrique « Projets personnels : actifs numériques » avec deux entrées au maximum, Polymarket
  (fiche 1) et MicroStrategy (fiche 2) ; une troisième ligne courte possible pour ether.fi (fiche 4) si la place le
  permet. Le radar dérivés (fiche 3) sert d'exemple en entretien.
- **Lettre EY Genève** : un paragraphe, deux projets cités, un chiffre chacun, le mot « vérification » au centre.
- **Mémoire professionnel** : la fiche 2 est un sujet tout trouvé (« Comptabilité et audit d'un bilan adossé au
  bitcoin »). Si tu le retiens, cela donne au recruteur une trajectoire cohérente du CV au diplôme.
- **Autres candidatures** (fintech, plateforme crypto, data) : ajouter les fiches 3 à 8, et déplacer la rubrique
  « projets » juste après l'expérience principale.

## À confirmer avant usage

1. Les dates de début et de fin de chaque projet (j'ai celles des sessions, pas celles de ton travail hors session).
2. Que tu assumes publiquement les projets Polymarket et MicroStrategy sous ton nom (dépôt privé pour le premier).
3. Si tu veux rendre `polymarket-research` montrable, il faudrait une relecture du dépôt pour retirer toute trace de
   secrets, d'adresses de serveur et de discussions sur un capital réel avant de donner l'accès à qui que ce soit.
