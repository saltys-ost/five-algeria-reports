# Vérifications publiques (V1 → V11) — faites par Claude Code le 2026-09-28

Méthode : lecture seule (recherche web, help center ether.fi, GitBook ether.fi, dépôt public `etherfi-protocol/cash-v3`, API xStocks, explorateurs et RPC publics en `eth_call`, API de devis Jupiter / CoW / Across, CoinGecko, DexScreener, GeckoTerminal, Kraken, Nasdaq). **Aucune transaction, aucun swap, aucune connexion de wallet.** Niveau de confiance : élevé / moyen / faible. Quand deux sources se contredisent, les deux sont montrées.

Accès bloqués depuis l'environnement d'exécution (à signaler, pas de conjecture) : pages de l'app `ether.fi/app/...` (429), `web.archive.org`, `assets.backed.fi` (géobloqué), 1inch (clé API), Odos (Cloudflare), Yahoo Finance (429), Stooq (connexion coupée), DefiLlama site (403 ; l'API `yields.llama.fi` fonctionne).

## Résumé

| # | Vérification | Statut | Confiance |
|---|---|---|---|
| V1 | Réseaux d'émission des xStocks et adresses SPYx/QQQx/TBLLx/GLDx | vérifié (CoinGecko incomplet : ne liste pas Optimism) | élevé |
| V2 | Adresses acceptées en collatéral par ether.fi sur OP Mainnet | vérifié on-chain ; **help center contradictoire** (tableau « Optimism » avec des adresses Scroll) | élevé |
| V2 | Réseaux acceptés dans « Add funds » | vérifié : xStocks **uniquement en wrappers sur Ethereum**, PAXG uniquement Ethereum | élevé |
| V3 | Le xStock acheté en externe est-il le token accepté ? | vérifié : **non** (collatéral = miroir ether.fi iwSPYx d'un wrapper wSPYx détenu sur Ethereum) | élevé |
| V3 | Pont officiel xStocks (xBridge, Chainlink CCIP) Solana↔EVM et EVM↔EVM | vérifié (existe, Optimism inclus) ; frais et délais **non publiés** | élevé / faible |
| V4 | Achat DEX Solana (Jupiter) SPYx/QQQx/GLDx : impact < 0,2 % de 500 à 10 000 € | vérifié | élevé |
| V4 | TBLLx sur DEX | vérifié : **illiquide** (impact 91–99,6 %) | élevé |
| V4 | Achat DEX EVM : pools AMM quasi vides ; devis CoW Ethereum (~1 % de spread) et Arbitrum (0,27 %) non garantis | vérifié mais contradictoire (devis sans pool visible) | moyen |
| V5 | Chaîne du Borrow Hub / Vault = OP Mainnet ; Hub `0x66753c4e…C572` (Aave V4) | vérifié | élevé |
| V5 | Chemin Solana → ether.fi : xBridge → Ethereum → wrap → dépôt Ethereum → pont automatique vers OP | vérifié (frais xBridge non publiés) | élevé / faible |
| V6 | Liquidité DEX suffisante sur une chaîne acceptée par ether.fi | vérifié : **non** (seul Ethereum + wrap mène au dépôt, liquidité AMM nulle) | élevé |
| V7 | eBTC et « BTC Yield » : deux tokens distincts (eBTC 0x657e… vs liquidBTC 0x5f46…) | vérifié | élevé |
| V7 | Origine de l'écart ~21 % observé (2 772,80 € pour « 0,03 BTC ») | **non tranché** : hypothèses ci-dessous | moyen |
| V8 | Prix de marché du jour (BTC, ETH, or, SPY, QQQ, BIL, eBTC, weETH, PAXG, ETHFI, xStocks) | vérifié | élevé |
| V9 | Tableau standard LTV / seuil / bonus du help center (19/06/2026) | vérifié | élevé |
| V9 | SPYx / QQQx / TBLLx / PAXG : seuils et bonus | **non documentés** ; lus on-chain (deux jeux de paramètres) et dans le code public | élevé (valeurs) / moyen (interprétation) |
| V10 | Frais Across USDC Ethereum→OP et Arbitrum→OP ; gas actuels | vérifié | élevé |
| V10 | Pont d'un xStock ERC-20 vers Optimism (Across, Standard Bridge) | vérifié : **aucune route** (Across : token non supporté ; Standard Bridge : tokens rebasing exclus) | élevé |
| V11 | Cashback : ETHFI, paliers Core EUR 3 % / 1 % / 0,1 %, lock 7 j, min 5 $, Travel 5 %, CGU 18/09/2026 | vérifié | élevé |
| V11 | Historique de la devise du cashback (wETH → USDC ? → ETHFI) | **contradictoire** (sources secondaires ; Wayback bloqué) | faible |
| Bonus | Taux d'emprunt USDC / EURC | non publié (secondaires : « ~4 % » vs « à partir de 1,17 % ») | faible |
| Bonus | APY Earn (DefiLlama) : LiquidETH 3,41 %, LiquidUSD 5,57 %, LiquidBTC 0,75 % ; Liquid EUR / RWA absents | vérifié (agrégateur) / non trouvé | moyen |

## V1 — Réseaux et adresses des xStocks (Backed Finance)

Source la plus précise : API publique xStocks `https://api.xstocks.fi/api/v2/public/assets/{SYMBOL}` (2026-09-28). Les xStocks EVM sont déployés **à la même adresse sur toutes les chaînes EVM** (Ethereum, Arbitrum, BNB, Mantle, Ink, X Layer, HyperEVM, **Optimism**) ; Solana en SPL Token-2022 ; Tron et TON. **Base : absent** (confirmé : `eth_getCode` vide sur Base).

| Token | Adresse EVM (toutes chaînes EVM) | Solana | Wrapper ERC-4626 Backed v1 / v2 |
|---|---|---|---|
| SPYx | `0x90a2a4c76b5d8c0bc892a69ea28aa775a8f2dd48` | `XsoCS1TfEyfFhfvj8EtZ528L3CaKBDBRqRapnBbDF2W` | v1 `0xc88fcd8b874fdb3256e8b55b3decb8c24eab4c02` ; v2 `0xe7e553cd128f0011777323a0b44a7b96ea1cb540` |
| QQQx | `0xa753a7395cae905cd615da0b82a53e0560f250af` | `Xs8S1uUs1zvS2p7iwtsG3b6fkhpvmwz4GYU3gWAmWHZ` | v1 `0xdbd9232fee15351068fe02f0683146e16d9f2cea` ; v2 `0x4c1ae29c159838fc1b224636e28e086eb69101f7` |
| TBLLx | `0x4cbf89ed7bb30b8a860fa86d3c96e9c72931299b` | `XsqBC5tcVQLYt8wqGCHRnAUUecbRYXoJCReD6w7QEKp` | v1 `0xcd932bf1c895b7143ec34df5ae7889d3853904d8` ; v2 `0x461b25b99606fe169d6f0dd6816650ef6536403e` |
| GLDx | `0x2380f2673c640fb67e2d6b55b44c62f0e0e69da9` | `Xsv9hRk1z5ystj9MhnA7Lq4vjSsLwzL2nxrwmwtD3re` | v1 `0x61532ce3f1df7fbf5ffb7b891d184226e85b37c6` ; v2 `0x735f1509bff25e27cd442b9bfb231324648ead9b` |

Vérifié on-chain (`name()/symbol()`) sur Optimism, Arbitrum, Ethereum. Supplies indicatives SPYx : 6 482 (OP) / 29 050 (Arbitrum) / 30 151 (Ethereum) ; Solana ≈ 95 000 (RWA.xyz). Contradiction mineure : CoinGecko ne liste pas Optimism pour ces tokens.
Sources : https://api.xstocks.fi/api/v2/public/assets/SPYx (QQQx, TBLLx, GLDx) · https://docs.xstocks.fi · https://docs.xstocks.fi/developers/wrapped-xstocks · https://xstocks.com/products · https://api.coingecko.com/api/v3/coins/sp500-xstock · RPC https://mainnet.optimism.io, https://arb1.arbitrum.io/rpc, https://mainnet.base.org, https://ethereum-rpc.publicnode.com. Confiance : élevé.

## V2 — Adresses acceptées en collatéral par ether.fi (OP Mainnet) et réseaux « Add funds »

Lecture on-chain du **Borrow Spoke Aave V4 d'ether.fi** `0xdffcC3536D932eb51Df51a7F5FA407c4270d5308` (26 réserves) et du LendGateway `0x01F8cDFb1694eA8fE4ED6c38a0fD78d1188E03F4`, 2026-09-28 :

| Actif | Adresse OP acceptée | Remarque |
|---|---|---|
| USDC | `0x0b2c639c533813f4aa9d7837caf62653d097ff85` | USDC natif Circle |
| EURC | `0xdcb612005417dc906ff72c87df732e5a90d49e11` | |
| weETH | `0x5a7facb970d094b6c7ff1df0ea68d99e6e73cbff` | |
| eBTC | `0x657e8c867d8b37dcc18fa4caead9c45eb088c642` | confirme la référence help center 0x657e…C642 |
| « SPYx » | `0xc1e636aae7d6b46229fc2c362d562610519e8d7c` = **iwSPYx** | miroir OFT LayerZero du wrapper wSPYx détenu sur Ethereum ; le SPYx Backed sur OP (`0x90a2…`) n'est **pas** enregistré |
| « QQQx » | `0x3c99d3a81b27583b2e26dbd387c10411f2763516` = iwQQQx | |
| « TBLLx » | `0x5f8b2d2b97ad4d63188f44965778f6004d5bc387` = iwTBLLx | |
| PAXG | `0x41a7f2bb9789199654c206f09392674c1af6676c` = iPAXG | PAXG n'existe pas nativement sur OP |
| GLDx / wGLDx | **non trouvé** comme réserve de collatéral | accepté en dépôt (wGLDx sur Ethereum) seulement |

**Contradiction** : le tableau « Contract Address (Optimism) » de l'article help center 304388 (màj 19/06/2026) donne pour USDC, weETH, WETH, USDT des adresses **sans code sur Optimism** qui répondent sur **Scroll** (tableau hérité de la migration Scroll → OP). Seuls EURC et eBTC y sont corrects.

Réseaux « Add funds » (help center art. 758804) : USDC depuis Ethereum, OP, Arbitrum, Base, BNB, Celo, Gnosis, HyperEVM, Katana, Mantle, Polygon, Scroll, Solana, Tempo ; EURC : Ethereum, Scroll, OP ; weETH / eBTC / WETH / ETHFI : Ethereum, Scroll, Base, OP ; **PAXG : Ethereum uniquement** ; **actions tokenisées : uniquement les wrappers wSPYx, wQQQx, wTBLLx, wGLDx… sur Ethereum** (aucun xStock accepté depuis Arbitrum, Base, Optimism, Solana).
Sources : https://help.ether.fi/en/articles/758804-supported-assets-and-networks-for-your-vault-with-cash · https://help.ether.fi/en/articles/833702-usdc-and-usdt-deposit-networks-and-addresses · https://help.ether.fi/en/articles/304388-how-does-collateral-and-borrowing-work · https://etherfi.gitbook.io/etherfi/products/cash/technical-documentation · https://etherfi.gitbook.io/etherfi/developers/contracts-and-integrations/deployed-contracts.md · https://github.com/etherfi-protocol/cash-v3 (`deployments/mainnet/10/`, PR #304) · RPC Scroll https://rpc.scroll.io. Confiance : élevé (adresses), moyen (exhaustivité).

## V3 — Même token ? Pont officiel ?

- **Non.** Le collatéral est `iwSPYx` / `iwQQQx` / `iwTBLLx` (tokens ether.fi, mint/burn LayerZero) représentant des parts de wrapper ERC-4626 Backed détenues sur Ethereum (adaptateur `StockOFTBridgeAdapter` `0x12e058A27Cd91699A285262F3c0ced7180bB2E4B`). Un SPYx acheté sur Solana, Arbitrum ou même sur Optimism doit être amené sur **Ethereum**, **wrappé en wSPYx** (https://defi.xstocks.fi/wrap), puis déposé sur l'adresse Ethereum du Vault ; ether.fi le ponte lui-même vers OP (PR #273, #287 du dépôt cash-v3). Version de wrapper (v1 `0xc88f…` ou v2 `0xe7e5…`) utilisée par ether.fi : **non trouvée** → à vérifier dans l'écran « Add funds » avant tout dépôt. Wrapper v1 wSPYx sur Ethereum vérifié on-chain : `asset()` = SPYx, 1 wSPYx = 1,00471 SPYx, `totalAssets` = 727,8 SPYx seulement.
- **xBridge** (Backed × Chainlink CCIP) : annoncé le 12/12/2025 (pilote Solana ↔ Ethereum) ; l'API `/api/v2/public/bridges` liste 9 réseaux (contrat `0x9ec0e4a4c411493773e01e2abf4d42395788846b` sur Ethereum, Arbitrum, BSC, Optimism, Mantle, Ink, X Layer, HyperEVM ; programme Solana `F2ZYgyh8YDG6rHo9F1T8Aw4WoTyy8eYN3GgM2LaPKcZN`) avec lanes EVM↔EVM et Solana↔EVM. **Frais et délais non publiés** ; repères génériques CCIP : ≈ 0,50 $ (Ethereum → autre), 1,50 $ (→ Ethereum), + gas ; latence ≈ finalité source (Ethereum ~15 min, Solana < 1 s) + exécution.
Sources : https://api.xstocks.fi/api/v2/public/bridges · https://xstocks.fi/us/news/introducing-the-xbridge · https://www.coindesk.com/web3/2025/12/12/backed-chainlink-launch-xbridge-to-move-tokenized-stocks-between-solana-and-ethereum · https://docs.chain.link/ccip/billing · https://docs.chain.link/ccip/ccip-execution-latency · https://github.com/etherfi-protocol/cash-v3/pull/273, /pull/287, /pull/304 · https://etherscan.io/token/0xc88fcd8b874fdb3256e8b55b3decb8c24eab4c02. Confiance : élevé (token différent, Ethereum obligatoire) ; faible (frais xBridge).

## V4 — Achat DEX sans exchange centralisé (devis du 2026-09-28 ~09:50 UTC, avant l'ouverture de Wall Street)

**(a) Solana — Jupiter / Raydium / Orca**

| Token | Pool principal | TVL | Vol. 24 h | Frais pool | Liquidité agrégée Jupiter |
|---|---|---|---|---|---|
| SPYx | Raydium CLMM SPYx/USDC `6truu3rZ…nDDE` | 3,11 M$ | 1,58 M$ | 0,10 % | 4,71 M$ |
| QQQx | Raydium CLMM QQQx/USDC `GMjGLWzv…U1aG` | 2,26 M$ | 449 k$ | 0,10 % | 2,09 M$ |
| GLDx | Raydium CLMM GLDx/USDC `78ReVNML…hyze` | 0,93 M$ | 1,67 M$ | 0,10 % | 0,83 M$ |
| TBLLx | aucun pool avec réserve mesurable | ~0 | 0 | — | **2,50 $** |

Devis Jupiter Lite (`lite-api.jup.ag/swap/v1/quote`, USDC → token, prix effectif en USDC par token, impact de prix) :

| Token | 570 USDC (≈ 500 €) | 1 140 USDC (≈ 1 000 €) | 5 700 USDC (≈ 5 000 €) | 11 400 USDC (≈ 10 000 €) | Spread achat/vente |
|---|---|---|---|---|---|
| SPYx | 771,57 (0,0002 %) | 771,58 (0 %) | 771,62 (0,00001 %) | 771,64 (0,00005 %) | 0,02–0,03 % |
| QQQx | 740,60 | 740,61 | 740,69 | 740,77 (0,0003 %) | 0,04–0,06 % |
| GLDx | 380,74 (0,09 %) | 380,74 (0,09 %) | 380,84 (0,12 %) | 380,93 (0,15 %) | 0,11–0,16 % |
| TBLLx | 1 214,92 (**impact 91 %**) | 2 429,82 (95,6 %) | 12 148 (99,1 %) | 24 293 (99,6 %) | inutilisable (NAV ≈ 105 $) |

Frais Solana : ≈ 0,0006 $ par signature, priority fee médiane 0, création de compte de token ≈ 0,24 $ une fois ; Jupiter Lite `platformFee: null`.

**(b) EVM — Ethereum / Arbitrum / Base / Optimism**
- Pools AMM (Uniswap v3/v4) : Ethereum SPYx < 2 000 $ de réserve, volume 0 ; QQQx < 1 000 $ ; wSPYx ~35 k$ sur paires exotiques, volume 0. **Arbitrum, Optimism : aucun pool. Base : aucun contrat canonique** (un pool « GLDX/WETH » sur Base à une adresse non Backed → suspect). HyperEVM : wSPYx/USDC 53 k$ + 24 k$ ; wQQQx 17 k$.
- Devis CoW Swap (`api.cow.fi`, `verified:false`, liquidité de solvers RFQ, **non garantie**) : Ethereum SPYx 772,95 → 769,04 USDC (570 → 11 400 USDC), vente 763,73 → spread ≈ 1 %, fee 3–4 USDC ; QQQx 742,38 → 738,70 ; GLDx 383,40 → 381,57 ; TBLLx 3 033,7 (pas de liquidité) ; **wSPYx directement : 920,7 → 1 320,6 (+19 % à +70 %)** → inachetable, il faut acheter SPYx puis wrapper. Arbitrum : SPYx 768,9 (spread 0,27 %, fee 0,03 USDC). Base : « NoLiquidity ». 1inch : clé API requise ; Odos : bloqué.
- Contradiction : CoW cote Arbitrum sans impact jusqu'à 11 400 USDC alors qu'aucun pool n'est visible ; Ethereum cote plus bas (769) que Solana (771,6). Les deux sont rapportés.
- Hors séance US : trading on-chain 24/7 (Kraken FAQ, docs xStocks) ; émission/rachat primaire 24/5, min 5 000 $. Spreads « plus larges hors séance… historiquement < 1 % d'écart à l'ouverture du lundi » (Kraken) ; « 3–5 % sur des titres individuels le week-end » (Eco). **Aucune série chiffrée trouvée.**
Sources : https://api.dexscreener.com/latest/dex/search?q=SPYx · https://api.geckoterminal.com/api/v2/search/pools?query=SPYx · https://lite-api.jup.ag/swap/v1/quote · https://api.cow.fi/mainnet/api/v1/quote (arbitrum_one, base) · https://api-v3.raydium.io/pools/info/ids · https://api.orca.so/v2/solana/pools · https://support.kraken.com/articles/xstocks-faq · https://docs.xstocks.fi/docs/frequently-asked-questions · https://eco.com/support/en/articles/15083158-kraken-xstocks-explained · https://app.rwa.xyz/platforms/xstocks. Confiance : élevé (Solana, illiquidité TBLLx, absence de pools EVM) ; moyen (devis CoW).

## V5 — Chemin jusqu'à ether.fi, chaîne du Borrow Hub

- Chaîne actuelle : **OP Mainnet** (migration Scroll → OP début 2026). Borrow Hub = instance Aave V4 dédiée : Hub `0x66753c4e3fC84f1eD0e3C267C927284E9d90C572` (« ether.fi: Borrow Hub », proxy créé le 30/07/2026, ~164,8 M$) — **confirme le 0x6675…C572 observé** ; Spoke `0xdffcC353…5308` ; LendGateway `0x01F8cDFb…03F4` ; Vault utilisateur = `EtherFiSafe` (factory `0xF4e147Db…d8CF`) ; TopUpDest OP `0x3a6A7245…6B87`. Lancement public 13/08/2026.
- Acheté sur Solana : xBridge Solana → Ethereum → wrap wSPYx → dépôt sur l'adresse Ethereum du Vault → pont automatique LayerZero vers OP (iwSPYx). Ponter vers Optimism directement ne sert à rien (dépôt « unsupported »).
- Acheté sur Ethereum : wrap → dépôt Ethereum → pont automatique. Arbitrum : xBridge vers Ethereum d'abord. Base : SPYx n'existe pas.
- Alternative : achat in-app (intégration xStocks, minimum 10 $, indisponible US/UK/Canada). Le module `AcrossSwapModule` du Vault explique les transferts **Across** vers/depuis Optimism vus on-chain par l'utilisateur.
- Retrait des actions : OP → Ethereum via `StockWithdrawModule` (`0xB9D4cdD2…AcA3`) et `StockUnwrapper` (`0x4Fc4a684…cD448`), après le délai de retrait Cash. Retraits cross-chain généraux : « jusqu'à 1 h ».
Sources : https://thedefiant.io/news/defi/ether-fi-migrates-to-optimism-s-op-mainnet-from-scroll · https://optimism.io/blog/etherfi-upgrades-to-aave-v4-on-op-mainnet · https://governance.aave.com/t/arfc-deploy-a-dedicated-aave-v4-whitelabel-instance-fully-managed-by-etherfi-on-op-mainnet-to-power-ether-fi-cash/25314 · https://optimistic.etherscan.io/address/0x66753c4e3fC84f1eD0e3C267C927284E9d90C572 · https://help.ether.fi/en/articles/637846-fund-your-vault-with-crypto · https://help.ether.fi/en/articles/755637-what-are-xstocks · https://help.ether.fi/en/articles/382174-cross-chain-withdrawals · https://github.com/etherfi-protocol/cash-v3 (`src/across/AcrossSwapModule.sol`, `src/stock-withdraw/*`, PR #268, #273, #287). Confiance : élevé.

## V6 — Liquidité DEX sur une chaîne acceptée : **non**

Seul Ethereum (+ wrap) mène à un dépôt ether.fi, et sa liquidité AMM est nulle ; CoW Swap (solvers) cote SPYx/QQQx/GLDx sur Ethereum avec ~1 % de spread mais sans garantie d'exécution. Solana est la seule liquidité profonde (SPYx 4,7 M$, QQQx 2,1 M$, GLDx 0,8 M$) mais non déposable directement. Répartition de la valeur xStocks (RWA.xyz, 28/09/2026) : Solana 404,9 M$, Ethereum 159,7 M$, Ink 11,0 M$, HyperEVM 4,9 M$, Mantle 4,6 M$, Arbitrum 2,2 M$, Base 1,2 M$. Confiance : élevé.

## V7 — eBTC vs « BTC Yield » ; écart de ~21 %

- **Deux produits, deux tokens.** eBTC = LRT Bitcoin d'ether.fi, `0x657e8C867D8B37dCC18fA4Caead9C45EB088C642` (même adresse sur Ethereum, Base, Arbitrum, Optimism, Scroll…) ; `getRate()` de l'Accountant mainnet = **1 eBTC ≈ 1,0041 BTC** (28/09/2026). « BTC Yield » = **Liquid BTC Vault**, token `liquidBTC` `0x5f46d540b6eD704C3c8789105F30E075AA900726` (Ethereum + Optimism) ; `getRate()` = **1 liquidBTC ≈ 1,0344 BTC**. Le vault accepte eBTC, WBTC, LBTC, cbBTC : déposer de l'eBTC dans BTC Yield donne des parts liquidBTC, pas de l'eBTC.
- Collatéral : les deux sont acceptés — eBTC 52 / 72 / 5 % ; LiquidBTC 50 / 70 / 5 % (help center 19/06/2026).
- Prix publics 28/09/2026 09:44 UTC (CoinGecko) : BTC 82 631 $ / **72 629 €** ; eBTC 82 740 $ / **72 725 €** (0,99835 BTC ; marché mince : volume 24 h ~49 k$). La valeur Markets observée (73 065,76 €) est cohérente (< 0,5 %). **C'est la valeur « BTC Yield » (2 772,80 € pour 0,03 → 92 427 €/unité) qui est anormale.**
- Hypothèses (aucune tranchée) : (1) **quantité affichée tronquée** : 2 772,80 € ÷ 72 725 = 0,0381 BTC-équivalent ; un solde réel de ~0,0369 liquidBTC (× 1,0344) affiché « 0.03 » expliquerait tout — vérifier le solde exact ; (2) prix de part liquidBTC > 1 BTC : n'explique que +3,4 % ; (3) **prix figé** : BTC ≈ 92 400 € uniquement entre le 17/10 et le 11/11/2025 (ou ≈ 92 400 $ les 18–20/11/2025 et 13–20/01/2026) ; (4) confusion USD/EUR : 0,03 × 82 631 $ = 2 479 $ → rejetée ; (5) libellé en ETH → rejeté ; (6) sources de prix différentes (oracle Cash vs NAV Accountant) : quelques %, pas 21 %.
- CoinGecko ne liste pas liquidBTC ; la série 365 j eBTC est dans `data/prix/eBTC.csv`.
Sources : https://help.ether.fi/en/articles/304388-how-does-collateral-and-borrowing-work · https://help.ether.fi/en/articles/593396-ebtc · https://help.ether.fi/en/articles/517109-how-liquid-works · https://etherfi.gitbook.io/etherfi/products/liquid/live-vaults/liquid-btc-vault · https://etherfi.gitbook.io/etherfi/developers/contracts-and-integrations/deployed-contracts.md · https://www.coingecko.com/en/coins/ether-fi-staked-btc · RPC publicnode / mainnet.optimism.io (`getRate`, `symbol`). Confiance : élevé (tokens, adresses, LTV) ; moyen (origine de l'écart).

## V8 — Prix de marché du 2026-09-28 (~09:43 UTC)

| Actif | USD | EUR | Source |
|---|---|---|---|
| BTC | 82 634 | 72 632 | CoinGecko `simple/price` |
| eBTC | 82 740 | 72 725 | CoinGecko (écart +0,13 % vs BTC) |
| ETH | 2 640,1 | 2 320,54 | CoinGecko |
| weETH | 2 915,74 | 2 562,81 | CoinGecko (ratio weETH/ETH ≈ 1,104, normal) |
| PAXG | 4 157,99 | 3 654,70 | CoinGecko |
| ETHFI | 0,6654 | 0,5849 | CoinGecko ; ATH 8,53 $ (27/03/2024), ATL 0,2665 $ (05/06/2026) |
| SPY (ETF) | 771,35 (clôture 25/09) | — | Nasdaq `api.nasdaq.com` |
| SPYx (Jupiter, vente 1 token) | 771,41 | — | Jupiter Lite |
| QQQx / GLDx (Jupiter) | 740,32 / 380,31 | — | Jupiter Lite |
| EUR/USD BCE | 1,1403 (25/09/2026) | — | https://api.frankfurter.dev/v1/2026-09-28?base=EUR&symbols=USD |

Historiques 5 ans dans `data/prix/` (Kraken pour BTC/ETH/PAXG/ETHFI/HYPE ; Nasdaq pour SPY/QQQ/BIL/GLD ; CoinGecko 365 j pour SPYx/QQQx/TBLLx/GLDx/eBTC/weETH). Confiance : élevé.

## V9 — Paramètres de risque du collatéral

- **Tableau standard vérifié** (help center art. 304388, màj 19/06/2026) : USDC/USDT/EURC/frxUSD 90/95/1 % ; eUSD/LiquidUSD/LiquidReserve 80/90/2 ; LiquidEUR/LiquidRWA 70/90/2 ; wETH/weETH 55/75/3,5 ; eBTC 52/72/5 ; LiquidETH/LiquidBTC 50/70/5 ; wHYPE 45/65/4 ; beHYPE 40/60/5 ; ETHFI/sETHFI/OP 20/50/5. Mécanique : 50 % du collatéral liquidé d'abord, puis le reste si toujours insolvable.
- **SPYx / QQQx / TBLLx / PAXG : non documentés** (help center, GitBook, forum de gouvernance). Trouvés on-chain et dans le code public, **deux jeux de paramètres** :

| Actif (token ether.fi) | Borrow Spoke Aave V4 (28/09/2026) : collateralFactor / bonus max | Legacy DebtManager `0x0078C5…9553` et PR cash-v3 : LTV / seuil / bonus | LTV vu dans l'app par l'utilisateur |
|---|---|---|---|
| iwSPYx | 78 % / 10 % | 73 / 78 / 7,5 % (PR #273, 07/08/2026) | 67 % |
| iwQQQx | 78 % / 10 % | 73 / 78 / 7,5 % (PR #276) | 66 % |
| iwTBLLx | 80 % / 10 % | 70 / 80 / 10 % (PR #283, « risk-signed-off 2026-08-12 ») | 70 % |
| iPAXG | 80 % / 10 % | 75 / 80 / 6 % (PR #273) | non relevé |
| iPAXGy | 75 % / 10 % | 67 / 75 / 10 % (PR #326) | — |
| repères Spoke | USDC 90 / 5 % ; EURC 90 / 7,5 % ; weETH 75 / 10 % ; eBTC 72 / 12,5 % | | |

Interprétation (docs Aave V4) : pas de LTV séparée ; `collateralFactor` = facteur du Health Factor (liquidable si HF < 1) ; le bonus est un maximum (enchère hollandaise). ether.fi impose `LendGateway.minHealthFactor()` = **1,1** → capacité d'emprunt effective ≈ CF ÷ 1,1 (≈ 70,9 % pour SPYx/QQQx, 72,7 % pour TBLLx/PAXG), ce qui ne coïncide pas exactement avec les 67 / 66 % vus dans l'app. Plafonds de dépôt : 2 000 iwSPYx, 2 000 iwQQQx, 20 000 iwTBLLx, 300 iPAXG. Oracles Chainlink SPY/QQQ/TBLL/PAXG, staleness 3 jours (risque de lecture « fail-closed » pendant les jours fériés US > 72 h). Ces paramètres sont modifiables à tout moment par le curateur.
**Retenu dans l'app** : LTV = valeur vue dans l'app (statut DÉFAUT), seuil = 78 / 78 / 80 / 80 % (statut VÉRIFIÉ, les deux jeux concordent), bonus = 10 % (max on-chain, prudent). À confirmer par le support (question Q1).
Sources : https://help.ether.fi/en/articles/304388-how-does-collateral-and-borrowing-work · https://help.ether.fi/en/articles/764890-the-basics-of-borrowing · https://help.ether.fi/en/articles/558503-monitoring-your-borrow-position-and-liquidation-risk · https://aave.com/docs/aave-v4/positions · https://aave.com/docs/aave-v4/positions/liquidations · https://github.com/etherfi-protocol/cash-v3 (`scripts/wspyx-paxg/README.md`, `scripts/stock-listing/StockLendAssets.sol`, `scripts/aave-v4/SupportTbllxCollateral.s.sol`, PR #273, #276, #283, #304, #313, #326) · lecture on-chain Spoke/LendGateway/DebtManager via https://mainnet.optimism.io. Confiance : élevé (valeurs), moyen (interprétation).

## V10 — Frais de pont et gas (2026-09-28 ~09:45 UTC)

- **Across (USDC)** : Ethereum → Optimism et Arbitrum → Optimism : 0,0573 / 0,1143 / 0,5703 / 1,1403 USDC pour 570 / 1 140 / 5 700 / 11 400 USDC (**≈ 0,010 %** + 0,0003 $ de gas destination, LP fee 0), fill 2–17 s ; limites 0,50 → 96 749 USDC. Gas d'origine à la charge de l'utilisateur : Ethereum ≈ 0,4–0,6 $, Arbitrum ≈ 0,02–0,05 $. 0,5 ETH Ethereum → OP : 0,0083 %.
- **xStock via Across : impossible** (`Unsupported token on given origin chain`). Optimism Standard Bridge : exclut les tokens rebasing (les xStocks EVM le sont) → non viable. Arbitrum → Optimism officiel : n'existe pas. xBridge CCIP : voir V3.
- **Gas** : Ethereum base fee 0,83–1,13 gwei (Safe/Propose 1,13, Fast 1,47) → transfert ERC-20 ≈ 0,22 $, approve ≈ 0,16 $, swap ≈ 0,51 $ (150 k gas) à 0,86 $ (250 k), dépôt Standard Bridge ≈ 0,62 $ ; Arbitrum ≈ 0,05 $ par swap ; Optimism et Base < 0,01 $ ; Solana ≈ 0,0006 $ + 0,24 $ de compte de token une fois.
Sources : https://app.across.to/api/suggested-fees · https://app.across.to/api/available-routes · https://app.across.to/api/limits · https://docs.across.to/introduction/fees · https://docs.optimism.io/app-developers/bridging/standard-bridge · RPC `eth_feeHistory` / `eth_gasPrice` · https://api.etherscan.io/v2/api?chainid=1&module=gastracker&action=gasoracle. Confiance : élevé.

## V11 — Cashback : monnaie, paliers, règles ; historique ETHFI

- **Devise actuelle : ETHFI** (help center « How does cashback work? », art. 262374, màj **2026-09-24**) : « Every qualifying transaction with your Cash card, asset traded, or USD/EUR borrowed earns cashback in ETHFI » ; converti « at the current price » au règlement ; **lock 7 jours** ; **minimum 5 $ pour claim** ; « Trade and borrow cashback also follow the 7-day lock period » (cashback sur trades et emprunts documenté, **taux non publiés**).
- **Paliers Core (texte exact)** : « USD: First $2,000 / EUR: First $800 (USD equivalent, not €) → 3 % ; USD $2,001–$3,000 / EUR $801–$1,500 → 1 % ; USD above $3,000 → 0.5 % / EUR above $1,500 → 0.1 % ». Un seul compteur mensuel USD + EUR. Luxe : 3 % jusqu'à 10 000 $ (EUR 3 000 $ équiv.), Pinnacle : 50 000 $ (EUR 16 000). Note EUR : « adjusted cashback rate to balance 0% FX rate benefit ».
- **Travel** (art. 334714, màj 16/09/2026) : taux carte + 2 % bonus sur hôtels éligibles (3 % + 2 % = 5 %) ; Category Cashback 10/20/30 % (Luxe/Pinnacle/VIP), Core non éligible (art. 776152, màj 27/09/2026).
- **CGU « Cashback Rewards Program »** (GitBook, Last Updated September 18, 2026) : récompense en tokens « or other digital assets as determined by Ether.fi », valeur USD fixée à la transaction, quantité de tokens au moment où la récompense n'est plus pending ; seuil de claim « determined by Provider » ; expiration après 6 mois d'inactivité ; préavis 30 jours ; plafond mensuel possible.
- **Historique de la devise (contradictoire, sources secondaires)** : wETH selon cryptocardguy (14/06/2026) et airdropalert (« now pays out in ETHFI rather than wETH », 14/09) ; USDC selon kkinvesting (24/08), defycard, spendnode (11/09), KuCoin/Bitget (10/09 : « switches card cashback from USDC to ETHFI ») ; ETHFI depuis la refonte tokenomics annoncée les 10–11/09/2026 (cashback financé par des rachats). Chronologie plausible mais non prouvée : wETH (jusqu'à ~juin 2026) → USDC (été 2026) → ETHFI (11/09/2026). Les CGU du 05/02/2026 mentionnaient des tokens SCR (Scroll).
- **ETHFI** (CoinGecko 28/09/2026) : 0,6654 $ / 0,5849 € ; ATH 8,53 $ (27/03/2024) ; ATL 0,2665 $ (05/06/2026) ; 90 j EUR : 0,2799 € (02/07) → 0,6544 € (20/09).
Sources : https://help.ether.fi/en/articles/262374-how-does-cashback-work · https://help.ether.fi/en/articles/825725-why-is-my-cashback-locked-and-when-can-i-claim-it · https://help.ether.fi/en/articles/334714-ether-fi-travel · https://help.ether.fi/en/articles/776152-membership-level-benefits · https://help.ether.fi/en/articles/823083-how-does-category-cashback-work · https://help.ether.fi/en/articles/604957-eur-purchases-0-fx-rate · https://etherfi.gitbook.io/etherfi/legal/ether.fi-legal/ether.fi-cash-cashback-rewards-program-u.s.-and-international · https://www.kucoin.com/news/flash/ether-fi-ethfi-surges-16-5-amid-tokenomics-overhaul · https://coinmarketcap.com/top-stories/6aa569c69743041163798e63/ · https://www.spendnode.io/blog/etherfi-membership-tier-upgrades-boosted-cashback-september-2026/ · https://cryptocardguy.com/cards/ether-fi/ · https://kkinvesting.io/en/posts/etherfi-cash-card-review/ · https://airdropalert.com/blogs/ether-fi-card-review/ · https://api.coingecko.com/api/v3/coins/ether-fi. Confiance : élevé (état actuel) ; faible (historique).

## Bonus — Taux d'emprunt et APY Earn

- Taux d'emprunt : « variable, set by the underlying lending market (Aave v4) », « check the current rate in the app » (help center art. 326983 màj 20/08/2026, art. 764890 màj 25/08/2026). Secondaires non vérifiables : « 4 % APY » (cardpilled 27/09), « ~4 % » (crypto.news 13/08), « starts at 1.17 % » (airdropalert 14/09). **EURC : non trouvé.** Dune `dune.com/ether_fi/etherfi-cash` : 909,9 M$ de dépenses cumulées, 24,26 M$ de cashback, 112 475 cartes ; pas de taux.
- APY Earn (DefiLlama `yields.llama.fi/pools`, 28/09/2026) : LiquidETH **3,41 %** (TVL 363,5 M$), LiquidUSD **5,57 %** (26,6 M$), LiquidBTC **0,75 %** (11,45 M$), eBTC 0,23 %, weETH 2,34 %, LiquidHYPE 1,30 %. **Liquid EUR et Liquid RWA absents** (RWA : « up to 6.26 % » selon airdropalert). Rates on-chain : liquidBTC 1,0344 BTC/part ; eBTC 1,0041.
Sources : https://yields.llama.fi/pools · https://defillama.com/protocol/ether.fi-liquid · https://dune.com/ether_fi/etherfi-cash · https://help.ether.fi/en/articles/326983-understanding-your-cash-card-borrow-mode-vs-direct-pay-mode · https://etherfi.gitbook.io/etherfi/products/liquid/live-vaults/liquid-euro-vault.md · https://www.cardpilled.com/cards/etherfi. Confiance : moyen (APY) ; faible (taux d'emprunt).

## Contrôles propres à ce projet

- **Rendement réel BTC Yield** : 0,0004 BTC sur 0,03 BTC en ~2 mois ≈ 8 %/an, incompatible avec 1,2 % (app) et 0,75 % (DefiLlama) → non utilisé par le moteur ; lié à l'anomalie V7 (solde probablement tronqué). Question Q3.
- **Rendement réel Euro Yield** : 0,07 € sur 16,90 € en 32 jours ≈ 4,7 %/an, cohérent avec 5,2–6,25 % (arrondi sur un petit montant).
- **Seuil de bascule cashback** : les transactions visibles avant le 20/09 totalisent ~183 € (≈ 209 $), très en dessous de 800 $ → export complet à faire (voir README, étape « Contrôle cashback »).
- **Sources de prix indisponibles depuis ce conteneur** : Stooq et Yahoo Finance (le script les garde en repli pour votre machine) ; CoinGecko limité à 365 jours sans clé → Kraken et Nasdaq utilisés pour les 5 ans.
