# 05a — Shortlist rewards (re-filtrage du run 4)

_Généré le 2026-07-29 — lecture seule, aucune nouvelle collecte (source : data/04_rewards_markets.csv). Provenance [mesuré run 4]._

## Critères de filtrage

`capital_in_zone > 0` · profondeur non nulle au meilleur niveau des deux côtés (bid ET ask présents sur YES et NO) · `S ≤ 0.06` · `E ≥ 20 $/j` · `amplitude_24h ≤ 0.15`. Tri par `E/(K+1000)` décroissant.

## Décompte de survivants par critère (indépendamment)

- Marchés en entrée : **500**
- passent « capital_in_zone>0 » : **463**
- passent « profondeur bilatérale » : **495**
- passent « S<=0.06 » : **475**
- passent « E>=20 » : **285**
- passent « vol_24h<=0.15 » : **347**
- **tous critères réunis : 176**

## Liste filtrée complète (triée par rendement E/(K+1000))

| # | question | cat | E/j | K (zone) | rend. | S | vol24h | max_spr(¢) | min_size | fin |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | US x Iran Effective Ceasefire by August 31? | Iran | 250 | 904 | 0.1313 | 0.05 | 0.07 | 3.5 | 200 | 2026-08-31 |
| 2 | Will no qualifying diplomatic US-Iran meeting  | Politics | 142 | 1634 | 0.0539 | 0.021 | 0.1015 | 4.5 | 20 | 2026-09-30 |
| 3 | Iran military action against a Gulf State on J | Iran | 60 | 612 | 0.0372 | 0.02 | 0.075 | 4.5 | 200 | 2026-07-30 |
| 4 | Will GPT-6 be released by September 30, 2026? | sam altman | 50 | 582 | 0.0316 | 0.04 | 0.15 | 3.5 | 200 | 2026-06-30 |
| 5 | US x Iran Effective Ceasefire by August 14? | Iran | 200 | 5543 | 0.0306 | 0.02 | 0.09 | 4.5 | 200 | 2026-08-14 |
| 6 | Israel x Iran ceasefire continues through Augu | Iran | 200 | 5624 | 0.0302 | 0.01 | 0.05 | 2.5 | 200 | 2026-08-31 |
| 7 | Israel x Iran ceasefire continues through Augu | Iran | 100 | 2385 | 0.0295 | 0.01 | 0.06 | 2.5 | 200 | 2026-08-15 |
| 8 | Iran full airspace closure by August 15? | Iran | 100 | 2545 | 0.0282 | 0.02 | 0.085 | 4.5 | 20 | 2026-08-15 |
| 9 | Will the highest temperature in Seoul be 29°C  | Weather | 28 | 216 | 0.0230 | 0.03 | 0.15 | 4.5 | 100 | 2026-07-29 |
| 10 | US x Iran diplomatic meeting by August 15, 202 | Politics | 100 | 3494 | 0.0222 | 0.03 | 0.05 | 4.5 | 200 | 2026-08-15 |
| 11 | Will the highest temperature in Hong Kong be 2 | Weather | 93 | 3187 | 0.0222 | 0.02 | 0.15 | 4.5 | 100 | 2026-07-29 |
| 12 | Will the highest temperature in Shanghai be 35 | Weather | 171 | 6718 | 0.0222 | 0.01 | 0.09 | 4.5 | 100 | 2026-07-29 |
| 13 | US x Iran diplomatic meeting by August 31, 202 | Politics | 300 | 13678 | 0.0204 | 0.01 | 0.09 | 4.5 | 200 | 2026-08-31 |
| 14 | Will Shohei Ohtani win the 2026 National Leagu | Sports | 113 | 4616 | 0.0201 | 0.02 | 0.125 | 4.5 | 20 | 2026-11-13 |
| 15 | Will the highest temperature in Jeddah be 39°C | Weather | 105 | 4484 | 0.0191 | 0.02 | 0.15 | 4.5 | 100 | 2026-07-29 |
| 16 | Will the highest temperature in Los Angeles be | Weather | 38 | 1073 | 0.0183 | 0.01 | 0.14 | 4.5 | 20 | 2026-07-29 |
| 17 | Will the highest temperature in Tel Aviv be 32 | Weather | 61 | 2657 | 0.0167 | 0.02 | 0.135 | 4.5 | 100 | 2026-07-29 |
| 18 | Will the Fed Pause–Pause–Pause in the next thr | Fed | 51 | 2106 | 0.0164 | 0.003 | 0.099 | 4.5 | 50 | 2026-07-29 |
| 19 | Will Warsh say "AI" or "Artificial Intelligenc | Politics | 50 | 2154 | 0.0159 | 0.01 | 0.09 | 4.5 | 50 | 2026-07-29 |
| 20 | Will the highest temperature in Madrid be 38°C | Weather | 39 | 1749 | 0.0142 | 0.02 | 0.08 | 4.5 | 20 | 2026-07-29 |
| 21 | Will the highest temperature in Hong Kong be 2 | Weather | 32 | 1361 | 0.0136 | 0.01 | 0.125 | 4.5 | 100 | 2026-07-29 |
| 22 | Iran military action against a Gulf State on J | Iran | 60 | 3447 | 0.0135 | 0.02 | 0.075 | 4.5 | 200 | 2026-07-31 |
| 23 | Will the highest temperature in Sao Paulo be 2 | Weather | 26 | 979 | 0.0131 | 0.02 | 0.135 | 4.5 | 20 | 2026-07-29 |
| 24 | US announces end of Iranian blockade by July 3 | Politics | 200 | 14282 | 0.0131 | 0.02 | 0.1 | 4.5 | 200 | 2026-07-31 |
| 25 | Will the highest temperature in London be 33°C | Weather | 42 | 2281 | 0.0128 | 0.01 | 0.14 | 4.5 | 20 | 2026-07-29 |
| 26 | Iran full airspace closure by August 31? | Iran | 200 | 14626 | 0.0128 | 0.01 | 0.055 | 4.5 | 20 | 2026-08-31 |
| 27 | Will Alibaba have the best Chinese AI model at | China | 95 | 6499 | 0.0127 | 0.002 | 0.0365 | 4.5 | 20 | 2026-07-31 |
| 28 | Will the Fed decide differently in the next th | Fed | 49 | 3067 | 0.0120 | 0.035 | 0.0995 | 4.5 | 50 | 2026-07-29 |
| 29 | Will Trump endorse Likud in the 2026 Israeli E | Trump | 25 | 1093 | 0.0119 | 0.05 | 0.09 | 4.5 | 20 | 2026-10-28 |
| 30 | Will Mohamed Salah play in Saudi Pro League ne | Sports | 48 | 3140 | 0.0116 | 0.022 | 0.13 | 4.5 | 20 | 2026-09-01 |
| 31 | Will the Bank of Israel cut by 25 bps at the A | Economy | 22 | 919 | 0.0115 | 0.02 | 0.11 | 4.5 | 50 | 2026-08-31 |
| 32 | Will GPT-6 be released by August 31, 2026? | sam altman | 50 | 3400 | 0.0114 | 0.03 | 0.11 | 4.5 | 200 | 2026-08-31 |
| 33 | Will the highest temperature in London be 34°C | Weather | 28 | 1613 | 0.0107 | 0.02 | 0.1 | 4.5 | 20 | 2026-07-29 |
| 34 | Will the highest temperature in London be 32°C | Weather | 24 | 1252 | 0.0107 | 0.01 | 0.11 | 4.5 | 20 | 2026-07-29 |
| 35 | Will the highest temperature in Seoul be 32°C  | Weather | 27 | 1573 | 0.0105 | 0.01 | 0.14 | 4.5 | 100 | 2026-07-29 |
| 36 | Will Moonshot have the best Chinese AI model a | China | 105 | 9072 | 0.0104 | 0.001 | 0.031 | 4.5 | 20 | 2026-07-31 |
| 37 | Will Israeli forces withdraw from beyond the L | Politics | 30 | 1904 | 0.0103 | 0.01 | 0.055 | 4.5 | 200 | 2026-12-31 |
| 38 | Will NVIDIA be the largest company in the worl | Business | 108 | 9880 | 0.0099 | 0.01 | 0.1 | 4.5 | 200 | 2026-08-31 |
| 39 | Will the Fed decide differently in the next th | Fed | 103 | 9669 | 0.0097 | 0.01 | 0.115 | 4.5 | 100 | 2026-09-16 |
| 40 | Clarity Act (H.R.3633) signed into law in 2026 | Politics | 300 | 30486 | 0.0095 | 0.01 | 0.07 | 3.5 | 200 | 2027-01-01 |
| 41 | Will Apple be the largest company in the world | Business | 92 | 9244 | 0.0090 | 0.01 | 0.085 | 4.5 | 200 | 2026-08-31 |
| 42 | Will Anthropic IPO by October 31, 2026? | Finance | 100 | 10783 | 0.0085 | 0.01 | 0.1 | 5.5 | 50 | 2027-07-01 |
| 43 | Will Elon Musk post 760-799 tweets in July 202 | Politics | 35 | 3162 | 0.0084 | 0.008 | 0.1035 | 4.5 | 50 | 2026-08-01 |
| 44 | Will the Fed Pause–Pause–Pause in the next thr | Fed | 97 | 10965 | 0.0081 | 0.01 | 0.12 | 4.5 | 100 | 2026-09-16 |
| 45 | Iran full airspace closure by September 30? | Iran | 30 | 2751 | 0.0080 | 0.01 | 0.09 | 4.5 | 200 | 2026-09-30 |
| 46 | Will the Reserve Bank of India make no change  | interest r | 29 | 2871 | 0.0075 | 0.03 | 0.05 | 4.5 | 50 | 2026-08-05 |
| 47 | Will Warsh say "Good day" during July Press Co | Politics | 50 | 5700 | 0.0075 | 0.02 | 0.02 | 4.5 | 50 | 2026-07-29 |
| 48 | Will Apple be the largest company in the world | Business | 102 | 12673 | 0.0075 | 0.001 | 0.1435 | 4.5 | 200 | 2026-07-31 |
| 49 | Will the next Google Gemini Pro model be relea | AI | 70 | 8844 | 0.0071 | 0.01 | 0.075 | 4.5 | 50 | 2026-08-31 |
| 50 | Will Wesley Bell be the Democratic nominee for | Politics | 99 | 12962 | 0.0071 | 0.02 | 0.085 | 4.5 | 20 | 2026-08-04 |
| 51 | US x Iran diplomatic meeting by August 7, 2026 | Politics | 100 | 13809 | 0.0068 | 0.02 | 0.13 | 4.5 | 200 | 2026-08-07 |
| 52 | Will the Fed increase interest rates by 25 bps | Politics | 527 | 77986 | 0.0067 | 0.01 | 0.05 | 4.5 | 200 | 2026-09-16 |
| 53 | Will "Spider-Man: Brand New Day" score at leas | Movies | 20 | 2242 | 0.0062 | 0.037 | 0.1045 | 4.5 | 50 | 2026-08-03 |
| 54 | Will the highest temperature in Helsinki be 23 | Weather | 39 | 5979 | 0.0056 | 0.01 | 0.145 | 4.5 | 20 | 2026-07-30 |
| 55 | Will Anthropic IPO by December 31, 2026? | Finance | 100 | 17588 | 0.0054 | 0.01 | 0.0 | 5.5 | 200 | 2027-07-01 |
| 56 | No change in Reserve Bank of Australia's inter | Economy | 26 | 4213 | 0.0050 | 0.03 | 0.095 | 4.5 | 50 | 2026-08-11 |
| 57 | Will Apple be the second-largest company in th | Business | 24 | 3851 | 0.0049 | 0.03 | 0.15 | 4.5 | 50 | 2026-07-31 |
| 58 | Will there be no change in Fed interest rates  | Trump | 293 | 60640 | 0.0048 | 0.01 | 0.0 | 4.5 | 100 | 2026-10-28 |
| 59 | Will Alphabet be the third-largest company in  | Business | 32 | 5825 | 0.0047 | 0.02 | 0.075 | 4.5 | 50 | 2026-08-31 |
| 60 | Will the Fed decide differently in the next th | Fed | 110 | 22548 | 0.0047 | 0.01 | 0.105 | 4.5 | 100 | 2026-10-28 |
| 61 | US-Iran 60 day negotiation period extended? | Politics | 100 | 20749 | 0.0046 | 0.01 | 0.045 | 4.5 | 200 | 2026-08-20 |
| 62 | Israel x Iran ceasefire continues through July | Iran | 150 | 32016 | 0.0045 | 0.01 | 0.03 | 2.5 | 200 | 2026-07-31 |
| 63 | Will Apple be the largest company in the world | Business | 74 | 15441 | 0.0045 | 0.008 | 0.0425 | 4.5 | 200 | 2026-12-31 |
| 64 | Andrew Tate released from custody by December  | Politics | 50 | 10211 | 0.0045 | 0.02 | 0.1 | 4.5 | 100 | 2026-12-31 |
| 65 | NBA: LeBron James and Bronny James Jr. to Play | Sports | 50 | 10350 | 0.0044 | 0.01 | 0.02 | 4.5 | 100 | 2026-10-31 |
| 66 | Fed Rate Hike by October 2026 Meeting? | Finance | 150 | 36613 | 0.0040 | 0.01 | 0.055 | 4.5 | 200 | 2026-12-09 |
| 67 | Will there be no change in Fed interest rates  | Politics | 1284 | 322698 | 0.0040 | 0.003 | 0.106 | 4.5 | 200 | 2026-07-29 |
| 68 | Will Cori Bush be the Democratic nominee for M | Politics | 101 | 24660 | 0.0039 | 0.01 | 0.07 | 4.5 | 20 | 2026-08-04 |
| 69 | Will the Bank of Brazil make no change to the  | Brazil | 24 | 5391 | 0.0038 | 0.011 | 0.025 | 4.5 | 50 | 2026-08-04 |
| 70 | Israel x Iran ceasefire continues through Augu | Iran | 40 | 9726 | 0.0037 | 0.01 | 0.11 | 4.5 | 200 | 2026-08-09 |
| 71 | Israel closes its airspace by August 15? | Politics | 50 | 12620 | 0.0037 | 0.01 | 0.045 | 4.5 | 50 | 2026-08-15 |
| 72 | US announces end of Iranian blockade by Octobe | Politics | 30 | 7174 | 0.0037 | 0.01 | 0.1 | 4.5 | 200 | 2026-10-31 |
| 73 | Fed Rate Hike by September 2026 Meeting? | Finance | 150 | 40436 | 0.0036 | 0.01 | 0.065 | 4.5 | 200 | 2026-12-09 |
| 74 | Will there be no change in Fed interest rates  | Politics | 473 | 132320 | 0.0035 | 0.01 | 0.07 | 4.5 | 200 | 2026-09-16 |
| 75 | Will “Hacks” win Emmys 2026: Outstanding comed | Awards | 50 | 13395 | 0.0035 | 0.018 | 0.026 | 4.5 | 50 | 2026-09-14 |
| 76 | Will the Fed increase interest rates by 25 bps | Politics | 1216 | 353007 | 0.0034 | 0.001 | 0.1055 | 4.5 | 200 | 2026-07-29 |
| 77 | Will Sofia host Eurovision 2027? | Music | 50 | 13874 | 0.0034 | 0.01 | 0.035 | 4.5 | 50 | 2026-12-31 |
| 78 | Will the Fed Pause–Pause–Pause in the next thr | Fed | 90 | 26318 | 0.0033 | 0.01 | 0.145 | 4.5 | 100 | 2026-10-28 |
| 79 | Will Harrison Ford – “Shrinking” win Emmys 202 | Awards | 57 | 16311 | 0.0033 | 0.02 | 0.085 | 4.5 | 50 | 2026-09-14 |
| 80 | US announces end of Iranian blockade by Decemb | Politics | 30 | 8123 | 0.0033 | 0.01 | 0.095 | 4.5 | 200 | 2026-12-31 |
| 81 | Will the Bank of Israel decrease the Bank of I | Israel | 24 | 6518 | 0.0032 | 0.02 | 0.12 | 4.5 | 50 | 2026-09-01 |
| 82 | Will NVIDIA be the largest company in the worl | Business | 105 | 33654 | 0.0030 | 0.01 | 0.025 | 4.5 | 200 | 2026-12-31 |
| 83 | Will NVIDIA be the largest company in the worl | Business | 98 | 33703 | 0.0028 | 0.01 | 0.125 | 4.5 | 200 | 2026-07-31 |
| 84 | Will the Bank of Brazil decrease the target fo | Brazil | 23 | 7214 | 0.0028 | 0.01 | 0.06 | 4.5 | 50 | 2026-08-04 |
| 85 | GRVT FDV above $200M one day after launch? | Crypto | 50 | 17053 | 0.0028 | 0.01 | 0.045 | 4.5 | 100 | 2028-01-01 |
| 86 | US announces end of Iranian blockade by August | Politics | 30 | 10033 | 0.0027 | 0.01 | 0.065 | 4.5 | 200 | 2026-08-07 |
| 87 | Will Haley Stevens win the 2026 Michigan Democ | Politics | 106 | 39193 | 0.0026 | 0.01 | 0.129 | 4.5 | 20 | 2026-08-04 |
| 88 | Mojtaba Khamenei seen in public by December 31 | Iran | 100 | 37717 | 0.0026 | 0.01 | 0.01 | 4.5 | 200 | 2026-12-31 |
| 89 | Will Saudi Arabia join the Abraham Accords bef | Politics | 50 | 18486 | 0.0026 | 0.01 | 0.06 | 3.5 | 200 | 2026-12-31 |
| 90 | Israel closes its airspace by August 31? | Politics | 100 | 40755 | 0.0024 | 0.01 | 0.0 | 4.5 | 200 | 2026-07-15 |
| 91 | Will Russia capture all of Huliaipole by Septe | Politics | 50 | 20509 | 0.0023 | 0.01 | 0.09 | 6.5 | 100 | 2026-09-30 |
| 92 | Mitch McConnell steps down from Senate before  | Politics | 100 | 42051 | 0.0023 | 0.01 | 0.03 | 3.5 | 200 | 2027-01-03 |
| 93 | Will the Fed increase interest rates by 25 bps | Trump | 164 | 74252 | 0.0022 | 0.01 | 0.02 | 4.5 | 100 | 2026-10-28 |
| 94 | Will Elon Musk post 180-199 tweets from July 2 | Politics | 21 | 10484 | 0.0018 | 0.001 | 0.061 | 4.5 | 50 | 2026-07-31 |
| 95 | Will "Spider-Man: Brand New Day" Opening Weeke | box office | 35 | 18616 | 0.0018 | 0.008 | 0.0845 | 4.5 | 50 | 2026-08-02 |
| 96 | US strike on Cuba by December 31? | Venezuela | 100 | 58746 | 0.0017 | 0.01 | 0.01 | 4.5 | 100 | 2026-12-31 |
| 97 | Fed Rate Hike by July 2026 Meeting? | Finance | 150 | 95403 | 0.0016 | 0.015 | 0.0965 | 4.5 | 200 | 2026-12-09 |
| 98 | SAVE Act becomes law by December 31, 2026? | Politics | 150 | 97261 | 0.0015 | 0.01 | 0.0 | 4.5 | 200 | 2026-04-30 |
| 99 | Will Lamar Jackson win the 2026 NFL MVP? | football | 37 | 23537 | 0.0015 | 0.01 | 0.01 | 4.5 | 20 | 2027-02-15 |
| 100 | Strait of Hormuz traffic returns to normal by  | Politics | 150 | 100046 | 0.0015 | 0.01 | 0.015 | 4.5 | 200 | 2026-09-30 |
| 101 | Will Abdul El-Sayed win the 2026 Michigan Demo | Politics | 94 | 64086 | 0.0014 | 0.01 | 0.13 | 4.5 | 20 | 2026-08-04 |
| 102 | Tesla and SpaceX merger officially announced b | SpaceX | 40 | 27791 | 0.0014 | 0.01 | 0.015 | 4.5 | 50 | 2026-12-31 |
| 103 | Valorant: Gentle Mates vs Team Vitality (BO3)  | Sports | 47 | 32938 | 0.0014 | 0.01 | 0.015 | 2.5 | 500 | 2026-07-30 |
| 104 | Mojtaba Khamenei seen in public by September 3 | Iran | 30 | 21176 | 0.0014 | 0.01 | 0.015 | 4.5 | 200 | 2026-09-30 |
| 105 | Israel closes its airspace by July 31? | Politics | 100 | 83254 | 0.0012 | 0.001 | 0.016 | 2.5 | 300 | 2026-07-31 |
| 106 | Iran leadership change by September 30? | Politics | 100 | 88059 | 0.0011 | 0.01 | 0.01 | 4.5 | 200 | 2026-09-30 |
| 107 | Valorant: GIANTX vs Team Liquid (BO3) - VCT EM | Sports | 47 | 40937 | 0.0011 | 0.01 | 0.03 | 2.5 | 500 | 2026-07-29 |
| 108 | Will Denny Hamlin win the 2026 NASCAR Cup Seri | Sports | 100 | 90048 | 0.0011 | 0.01 | 0.095 | 4.5 | 20 | 2026-11-08 |
| 109 | Netanyahu out by end of 2026? | Politics | 30 | 28886 | 0.0010 | 0.01 | 0.075 | 3.5 | 200 | 2026-12-31 |
| 110 | Will Alphabet be the largest company in the wo | Business | 21 | 20553 | 0.0010 | 0.01 | 0.055 | 4.5 | 200 | 2026-12-31 |
| 111 | Strait of Hormuz traffic returns to normal by  | Politics | 200 | 206932 | 0.0010 | 0.01 | 0.02 | 4.5 | 200 | 2026-12-31 |
| 112 | Iran agrees to end enrichment of uranium by De | Politics | 30 | 30279 | 0.0010 | 0.03 | 0.025 | 3.5 | 200 | 2026-12-31 |
| 113 | LoL: Bilibili Gaming vs LGD Gaming (BO3) - LPL | Sports | 72 | 77221 | 0.0009 | 0.01 | 0.045 | 2.5 | 500 | 2026-07-29 |
| 114 | Will Count Binface get second place in the Cla | Politics | 40 | 43787 | 0.0009 | 0.01 | 0.01 | 4.5 | 100 | 2026-08-13 |
| 115 | Bab el-Mandeb Strait effectively closed by Aug | Politics | 150 | 175437 | 0.0009 | 0.01 | 0.02 | 4.5 | 200 | 2026-08-31 |
| 116 | Will Benjamin Netanyahu visit New York City by | Politics | 20 | 22863 | 0.0008 | 0.02 | 0.03 | 4.5 | 200 | 2026-09-30 |
| 117 | US-Iran Final Nuclear Deal by December 31, 202 | Iran | 150 | 194828 | 0.0008 | 0.01 | 0.01 | 4.5 | 200 | 2026-09-30 |
| 118 | Will Kimi Antonelli be the 2026 F1 Drivers' Ch | Sports | 154 | 200547 | 0.0008 | 0.001 | 0.0015 | 4.5 | 20 | 2026-12-06 |
| 119 | Will no Fed rate cuts happen in 2026? | Business | 116 | 166700 | 0.0007 | 0.002 | 0.004 | 4.5 | 50 | 2026-12-31 |
| 120 | LoL: Kiwoom DRX vs Nongshim Red Force (BO3) -  | Sports | 72 | 103564 | 0.0007 | 0.01 | 0.03 | 2.5 | 500 | 2026-07-29 |
| 121 | Will 30 ships transit the Strait of Hormuz on  | Iran | 100 | 150506 | 0.0007 | 0.011 | 0.049 | 4.5 | 200 | 2026-07-31 |
| 122 | Fed rate hike in 2026? | Fed | 100 | 157213 | 0.0006 | 0.01 | 0.06 | 3.5 | 200 | 2026-12-09 |
| 123 | Russia x Ukraine ceasefire by December 31, 202 | Ukraine | 30 | 48317 | 0.0006 | 0.01 | 0.015 | 4.5 | 200 | 2026-12-31 |
| 124 | Will Faker win a Finals MVP Award at an intern | Sports | 20 | 32193 | 0.0006 | 0.007 | 0.011 | 4.5 | 50 | 2026-12-31 |
| 125 | Will Spirit Win BLAST Bounty 2026 Season 2? | Sports | 33 | 54718 | 0.0006 | 0.01 | 0.07 | 4.5 | 50 |  |
| 126 | Will Russia capture all of Kostyantynivka by D | Politics | 20 | 33185 | 0.0006 | 0.01 | 0.03 | 6.5 | 50 | 2026-12-31 |
| 127 | LoL: T1 vs KT Rolster (BO3) - LCK Round 3-4 Le | Sports | 72 | 124932 | 0.0006 | 0.01 | 0.035 | 2.5 | 500 | 2026-07-29 |
| 128 | US obtains Iranian enriched uranium by Septemb | Politics | 30 | 57305 | 0.0005 | 0.01 | 0.005 | 4.5 | 200 | 2026-09-30 |
| 129 | LoL: Top Esports vs Anyone's Legend (BO3) - LP | Sports | 72 | 152794 | 0.0005 | 0.01 | 0.015 | 2.5 | 500 | 2026-07-29 |
| 130 | Kharg Island no longer under Iranian control b | Iran | 100 | 227651 | 0.0004 | 0.003 | 0.015 | 2.5 | 200 | 2026-06-30 |
| 131 | Will the U.S. invade Iran before 2027? | Politics | 300 | 688929 | 0.0004 | 0.01 | 0.02 | 3.5 | 200 | 2026-12-31 |
| 132 | Counter-Strike: SPARTA vs G2 Ares - Map 2 Winn | Sports | 759 | 1787565 | 0.0004 | 0.01 | 0.11 | 2.5 | 250 | 2026-07-28 |
| 133 | Will 1 Fed rate cut happen in 2026? | Business | 66 | 156704 | 0.0004 | 0.01 | 0.01 | 4.5 | 50 | 2026-12-31 |
| 134 | Will Iran announce withdrawal from MOU negotia | Politics | 30 | 79317 | 0.0004 | 0.02 | 0.025 | 4.5 | 200 | 2026-08-15 |
| 135 | Israel military action against Yemen by July 3 | Iran | 50 | 151946 | 0.0003 | 0.001 | 0.036 | 4.5 | 200 | 2026-07-31 |
| 136 | Will Lewis Hamilton be the 2026 F1 Drivers' Ch | Sports | 38 | 116449 | 0.0003 | 0.001 | 0.003 | 4.5 | 20 | 2026-12-06 |
| 137 | Zelenskyy out as Ukraine president by end of 2 | Politics | 30 | 102906 | 0.0003 | 0.01 | 0.0 | 3.5 | 200 | 2026-12-31 |
| 138 | Will 40 ships transit the Strait of Hormuz on  | Iran | 20 | 70758 | 0.0003 | 0.003 | 0.0345 | 4.5 | 50 | 2026-07-31 |
| 139 | Will Harry Kane win the 2026 Ballon d'Or? | Sports | 116 | 481364 | 0.0002 | 0.001 | 0.0035 | 4.5 | 20 | 2026-10-31 |
| 140 | Will Lamine Yamal win the 2026 Ballon d'Or? | Sports | 56 | 252955 | 0.0002 | 0.001 | 0.004 | 4.5 | 20 | 2026-10-31 |
| 141 | Strait of Hormuz traffic returns to normal by  | Politics | 500 | 2405193 | 0.0002 | 0.01 | 0.02 | 3.5 | 200 | 2026-08-31 |
| 142 | Will SpaceX have the highest IPO Market Cap 20 | SpaceX | 30 | 146094 | 0.0002 | 0.01 | 0.0 | 3.5 | 200 | 2026-12-31 |
| 143 | Will Russia capture Kostyantynivka by December | Politics | 50 | 248582 | 0.0002 | 0.001 | 0.036 | 6.5 | 100 | 2026-12-31 |
| 144 | US-Iran Final Nuclear Deal by August 18, 2026? | Iran | 100 | 500187 | 0.0002 | 0.002 | 0.002 | 3.5 | 200 | 2026-08-18 |
| 145 | Iran invades Kuwait by August 31? | Iran | 100 | 505015 | 0.0002 | 0.001 | 0.005 | 4.5 | 200 | 2026-08-31 |
| 146 | US x Iran diplomatic meeting by July 31, 2026? | Politics | 150 | 793550 | 0.0002 | 0.008 | 0.0315 | 3.5 | 200 | 2026-07-31 |
| 147 | Mojtaba Khamenei seen in public by August 31? | Iran | 30 | 163564 | 0.0002 | 0.01 | 0.015 | 4.5 | 200 | 2026-08-31 |
| 148 | Will J.D. Vance win the 2028 Republican presid | Politics | 63 | 352319 | 0.0002 | 0.001 | 0.0 | 5.5 | 50 | 2028-11-07 |
| 149 | US-Iran Final Nuclear Deal by September 30, 20 | Iran | 200 | 1147454 | 0.0002 | 0.01 | 0.02 | 4.5 | 200 | 2026-09-30 |
| 150 | US-Iran Final Nuclear Deal by August 31, 2026? | Iran | 40 | 256003 | 0.0002 | 0.01 | 0.0 | 3.5 | 200 | 2026-08-31 |
| 151 | Will Gavin Newsom win the 2028 Democratic pres | Politics | 40 | 263465 | 0.0002 | 0.001 | 0.001 | 5.5 | 50 | 2028-11-07 |
| 152 | 0 ships transit Hormuz on any date by July 31? | Iran | 20 | 141336 | 0.0001 | 0.015 | 0.0895 | 4.5 | 200 | 2026-07-31 |
| 153 | Will Marco Rubio win the 2028 Republican presi | Politics | 37 | 315634 | 0.0001 | 0.001 | 0.0 | 5.5 | 50 | 2028-11-07 |
| 154 | Will the Los Angeles Rams win the 2027 NFL lea | Sports | 110 | 1005711 | 0.0001 | 0.01 | 0.0 | 4.5 | 20 | 2027-03-31 |
| 155 | Will Philadelphia 76ers win the 2027 NBA Final | Sports | 40 | 422244 | 0.0001 | 0.001 | 0.008 | 4.5 | 20 | 2027-07-01 |
| 156 | Will Oklahoma City Thunder win the 2027 NBA Fi | Sports | 75 | 806364 | 0.0001 | 0.01 | 0.0 | 4.5 | 20 | 2027-07-01 |
| 157 | US charges Hormuz fees by August 31, 2026? | Politics | 30 | 327581 | 0.0001 | 0.003 | 0.006 | 4.5 | 200 | 2026-08-31 |
| 158 | Will Arsenal win the 2026-27 English Premier L | Sports | 84 | 1140471 | 0.0001 | 0.01 | 0.0 | 4.5 | 20 | 2027-05-30 |
| 159 | Will San Antonio Spurs win the 2027 NBA Finals | Sports | 67 | 916879 | 0.0001 | 0.01 | 0.0 | 4.5 | 20 | 2027-07-01 |
| 160 | Putin out as President of Russia by December 3 | Politics | 200 | 2961195 | 0.0001 | 0.01 | 0.0 | 3.5 | 200 | 2026-12-31 |
| 161 | Israel withdraws from Lebanon by August 31, 20 | Iran | 20 | 296435 | 0.0001 | 0.002 | 0.002 | 4.5 | 50 | 2026-08-31 |
| 162 | Will Alexandria Ocasio-Cortez win the 2028 Dem | Politics | 23 | 383837 | 0.0001 | 0.001 | 0.014 | 5.5 | 50 | 2028-11-07 |
| 163 | Will JD Vance win the 2028 US Presidential Ele | Politics | 40 | 700447 | 0.0001 | 0.001 | 0.002 | 5.5 | 50 | 2028-11-07 |
| 164 | Iran full airspace closure by July 31? | Iran | 30 | 528049 | 0.0001 | 0.002 | 0.027 | 4.5 | 200 | 2026-07-31 |
| 165 | Will Samuel Alito announce his retirement by S | Politics | 20 | 356751 | 0.0001 | 0.01 | 0.02 | 4.5 | 50 | 2026-12-31 |
| 166 | Will the Iranian regime fall before 2027? | Politics | 70 | 1324346 | 0.0001 | 0.01 | 0.0 | 3.5 | 200 | 2026-12-31 |
| 167 | US announces withdrawal from Al Udeid Air Base | Iran | 20 | 393706 | 0.0001 | 0.009 | 0.0025 | 4.5 | 200 | 2026-09-30 |
| 168 | Will the US confirm that aliens exist before 2 | Politics | 100 | 2125328 | 0.0000 | 0.01 | 0.0 | 3.5 | 200 | 2026-12-31 |
| 169 | Will Jon Ossoff win the 2028 Democratic presid | Politics | 23 | 536177 | 0.0000 | 0.001 | 0.011 | 5.5 | 50 | 2028-11-07 |
| 170 | Will Bayern Munich win the 2026-27 UEFA Champi | Sports | 36 | 1114088 | 0.0000 | 0.01 | 0.0 | 4.5 | 20 | 2027-05-30 |
| 171 | Will Manchester City win the 2026-27 English P | Sports | 66 | 2077343 | 0.0000 | 0.01 | 0.0 | 4.5 | 20 | 2027-05-30 |
| 172 | Will the Seattle Seahawks win the 2027 NFL lea | Sports | 20 | 664829 | 0.0000 | 0.01 | 0.0 | 4.5 | 20 | 2027-03-31 |
| 173 | Will Real Madrid win the 2026-27 UEFA Champion | Sports | 32 | 1333994 | 0.0000 | 0.02 | 0.01 | 4.5 | 20 | 2027-05-30 |
| 174 | Will China invade Taiwan by end of 2026? | Politics | 50 | 3502249 | 0.0000 | 0.001 | 0.002 | 3.5 | 200 | 2026-12-31 |
| 175 | Hantavirus pandemic in 2026? | Weather | 100 | 9122606 | 0.0000 | 0.001 | 0.001 | 5.5 | 200 | 2026-12-31 |
| 176 | Strait of Hormuz traffic returns to normal by  | Politics | 30 | 8710724 | 0.0000 | 0.001 | 0.0155 | 4.5 | 200 | 2026-08-15 |

