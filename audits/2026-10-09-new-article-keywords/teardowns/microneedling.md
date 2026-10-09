# At-home microneedling: top-3 teardowns (2026-10-09)

Tags: VERIFIED (read in primary data), PLAUSIBLE (inferred), NOT ESTABLISHED. [SERP] `serp/serp.json`, `serp/raw/` (desktop, 2026-10-09;
"microneedling serum" from `../2026-10-08-competitor-gap-per-page/serp/`) · [PAA] `serp/paa-related.json` · [PG] `serp/pages.json` · [M]
`teardowns/measurements.jsonl` · [FETCH] competitor page read today (curl) · [VOL] `classified.json`, observed clickstream a month, Ads bucket in
brackets · [BL] `serp/authority.json`, referring domains, domain / page · [REG] `docs/claims/` · [OWN] our pages, curl today · [HG] Hairgenetix docs.

Scope: 12 SERPs. Reddit refused curl and WebFetch, so Reddit and Instagram slots are read from their SERP snippets.

## Findings

1. **Four terms belong to Hairgenetix.** "derma stamp", "how to use a derma stamp", "how to derma stamp" and "derma stamp vs derma roller" are
   hair-led, and Hairgenetix's plan of 2026-10-09 names a hero for each (`hairgenetix/docs/microneedling-number-one-plan-2026-10-09.md` §4) [HG]. It
   ranks #5 on the comparison today [SERP]. We build none; face variants become sections.
2. **One face article, not six.** "at home microneedling" absorbs how-to-at-home, how often at home, the face stamp how-to and aftercare. The serum terms wait behind a gate.
3. **The brief's context has moved.** Both stamp sets now show "Pre-order" (Malcolm, 2026-10-08, `docs/todo.md` line 106) with `InStock` schema, not
   `OutOfStock` [OWN]. Open: no `PreOrder` availability; and "1 stamp + 4 single-use vials = a one-month ritual" implies weekly sessions, where
   Dermstore and Google's Overview put 0.5 mm at every 2 to 4 weeks.
4. **Our 0.5 mm stamp is the top of any source's home range.** Vogue's facial plastic surgeon: "the safe limit … about 0.3 mm", beginners ≤ 0.5 mm; Dermstore and the Overview: ≤ 0.5 mm [FETCH] [SERP].
5. **Three register conflicts, not one.** Argireline: never with DIY microneedling. Copper: sells the stamp with GHK-Cu (claim 7, Li 2015, grade C)
   but bans "speeds recovery after … microneedling". PDRN: "not on broken skin" (`pdrn.md` line 217) while a PDRN stamp set is live [REG] [OWN].
   Outside them: the FDA "has not cleared any microneedling devices for use with another product", and JAMA Dermatology reported facial granulomas
   after a vitamin C serum used with microneedle therapy (Soltani-Arabshahi 2014, PMID 24258303, checked via E-utilities). Until Malcolm decides, no
   article may tell readers to put our serums on freshly needled skin.
6. **No top-3 page on the face terms cites a study** (FDA, Vogue, Dermstore, Dr Pen: 0) [M] [PG]. Ammuri, which sells a stamp plus peptide serum kit,
   is the only page with our registers' posture: its serum "is not being presented as a sterile microneedling solution for immediate application into
   freshly needled skin" [FETCH].

---

### 1. "at home microneedling" (US 1,510 [27,100]; GB 475; best at home microneedling 553 / 158; how to do microneedling at home 251 / 158; derma stamp for face 100 / 79; is at home microneedling safe 100 / –; how to use derma stamp on face 50 / –) [VOL]

**SERP (US):** Reddit r/30PlusSkinCare (UGC), FDA (government), Vogue (magazine), Dr Pen bundle (brand product), Dermstore (retailer guide), YouTube
(a creator's DIY do's and don'ts, 3,811 views), Banish, Qure, mdpen (brand guides). Overview, PAA, popular products. **Overview sources:** Vogue,
Dermstore, FDA, Banish, YouTube, Qure, Shopping card; it says 0.25 to 0.5 mm, "0.5 mm or shorter", stamps over rollers, a 70% alcohol soak, "once a
week to once a month". **GB:** no Overview; Dr Pen UK category, Dr Pen UK bundle, Vogue, Trinny London, Reddit, Amazon UK, Glamour, Dermapen World,
YouTube [SERP]. **PAA:** Does microneedling at home actually work? · Is 40 too old for microneedling? · What is the best at-home microneedling device?
· How often should you microneedle your face at home? [PAA].

| Factor                     | #1 Reddit                                                                              | #2 FDA                                                                                                             | #3 Vogue                                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Type, title                | thread "At-home microneedling - worth it?"                                             | Consumer Update "Microneedling Devices: Getting to the Point on Benefits, Risks and Safety"                        | round-up plus guide; H1 "Does At-Home Microneedling Really Work? Experts Weigh In"                             |
| Opening answers?           | snippet: "No, at home microneedling is NOT worth it. The needles don't go straight in" | no: "Being pricked by tiny needles may sound like a strange way…", then "choose a health care provider"            | partly, sentence 2: DIY gives "a fraction of the benefits"                                                     |
| Words, H2                  | –                                                                                      | 1,138: products · which are devices · benefits · risks · safety tips · RF, hair, combining                         | 2,116: five device picks · accordion on benefits, side effects, recovery, home vs office, choosing, how to use |
| Citations, author          | –                                                                                      | 0 studies; Office of the Commissioner                                                                              | 0 studies; contributor plus a facial plastic surgeon and a physician associate; no reviewer                    |
| Dates, schema              | –                                                                                      | current as of 15 Oct 2025; Article                                                                                 | 2020, modified 30 Nov 2025; NewsArticle                                                                        |
| Tables, FAQ, video, images | –                                                                                      | none; 1 image                                                                                                      | no table; accordion without FAQPage; no video; 23 images                                                       |
| Products                   | –                                                                                      | none                                                                                                               | 5 devices, $48 to $249                                                                                         |
| Needle length              | rollers enter at an angle                                                              | no numbers                                                                                                         | home limit "about 0.3 mm", beginners ≤ 0.5 mm; yet one pick is a 0.25 to 2.0 mm pen                            |
| Topicals vs procedures     | –                                                                                      | no device cleared "for use with another product"; after: avoid retinol, glycolic acid, menthol, capsaicin, alcohol | "You should not needle over skin-care products"; no AHA, BHA, retinol for 2 days                               |
| Referring domains [BL]     | 1.59M / 0                                                                              | 334,906 / **342**                                                                                                  | 206,604 / 10                                                                                                   |

GB #1 and #2: Dr Pen UK category (1,083-word FAQ, "every 4-6 weeks", "up to 97% product absorption"; 115 / 3) and bundle (511 words, £199; 42 / 0) [PG] [FETCH].

**Why they win:** FDA is the official answer on a YMYL safety query with 342 page domains (VERIFIED), held at #2 although it never answers "at home".
Reddit's "worth it?" is the first PAA in the searcher's words (PLAUSIBLE). Vogue serves buying and how-to at once, names experts, updated Nov 2025
(VERIFIED). GB's top two sit on 115- and 42-domain sites, so authority is not the wall there (VERIFIED).

**The gap:** the sources disagree on needle length (0.3 vs 0.5 mm) and Dr Pen's US stamp page advises 1.5 mm for "deep wrinkles" on a home tool
[FETCH]; nobody shows the disagreement. Nobody cites the granuloma case series. "Is 40 too old?" goes unanswered; the FDA text answers it (clearances
cover adults 22 and older, no upper age). "How often at home?" gets no number from the top 3. The Overview leans on brand guides with 1 to 3 page
domains, and its "strictly cosmetic and meant for surface exfoliation" overstates the FDA (PLAUSIBLE).

**Our edge:** Dr Bodde as reviewer; the Yogya appraisal and the register's reading of Li 2015, which no competitor has (neither tested a home stamp,
so the edge is honesty, not proof); the real 0.5 mm tool to photograph. **Not an edge:** authority (2 referring domains [BL]), no reviews on the sets,
no video.

**Recommended article**

- **SEO title:** "At-Home Microneedling: Needle Length, How Often, Aftercare" (58). **Primary:** at home microneedling. **Secondaries:** how to do microneedling at home; how often to do microneedling at home; derma stamp for face.
- **Job:** decide whether to try it, pick a needle length, do it without marking the skin, know what to apply after.
- **H2s:** Does microneedling at home work? · Which needle length is sensible at home? · How to use a derma stamp on your face · How often can you
  microneedle your face at home? · What to put on skin after microneedling, and what never to · Aftercare day by day · Who should not microneedle at
  home, and is 40 too old? · Stamp, roller or pen for the face? · When to see a professional instead.
- **Opening direction:** at-home microneedling presses short needles, usually 0.5 mm or less, into the top of the skin; it is a shallower cousin of
  the clinic procedure, and the FDA has authorised no microneedling medical device for over-the-counter sale. With a clean tool, light vertical
  presses and weeks between sessions it mainly affects texture, and what you apply afterwards matters more than the tool.
- **Table no competitor has:** "What the sources say on home needle length and frequency" (FDA, Vogue's two experts, Dermstore, the Overview, a 0.5 to 3 mm stamp seller, our fixed 0.5 mm stamp), plus the "tested on needled skin" box from section 4.
- **Links:** first 150 words up to `/collections/microneedling` and `/pages/copper-peptide-research`; sideways to the Yogya article; down to the copper stamp set. **Length:** 1,300 to 1,500 words. **Safety block:** below.

**Guardrails:** shared list below; no "best device" list (it needs competitor brands); answer that PAA with criteria (fixed short needle, vertical stamp, sealed head, replacement schedule, no deep settings).
**Cannibalisation:** the copper set owns "microneedling stamp" (anchor "copper peptide microneedling stamp set" instead); Yogya owns "pdrn
microneedling" (link only); the collection is not rebuilt (plan 1.3); Hairgenetix: face wording only, no "derma stamp", "how to use a derma stamp" or
"vs roller" in title or headings.
**Winnable? Target:** GB page one in 6 to 12 months; US page one in 12, top 3 unrealistic. **Decides it:** whether Google trusts a 2-domain shop on "needles on your face": reviewer, primary sources, 5 to 10 genuine referring domains.

---

### 2. "how often to do microneedling" (US 402; GB 79; how often can you do microneedling 251 / 79; how often should you do microneedling 50 / 158; how often to use derma stamp 100 / –) [VOL]

**SERP:** clinics at #1, #3, #5, #6, #8, a dental practice at #7, Reddit #2, mdpen #4. **Overview:** clinic sessions every 4 to 6 weeks, 3 to 6
sessions, maintenance every 3 to 6 months; at home "0.25 mm … every 1 to 2 weeks", "0.5 mm … 2 to 4 weeks", too shallow for "major collagen
remodeling"; eight clinic and brand sources [SERP]. **PAA:** Is 40 too old? · Can you do too much microneedling? · Is once a year worth it? · Can I
microneedle my spider veins? [PAA].

| Factor                 | #1 Three Rivers Dermatology                         | #2 Reddit                              | #3 Texas Dermatology                                                                           |
| ---------------------- | --------------------------------------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Opening                | snippet: "every four to six weeks" (page 403 to us) | snippet: 4 to 6 weeks, 3 to 6 sessions | "3–6 treatments spaced 4–6 weeks apart"                                                        |
| Shape                  | clinic blog, 1 Oct 2025                             | thread                                 | 1,036 words; frequency, factors, signs, FAQ; author Tanya Gaines; modified 2 Sep 2026; FAQPage |
| Home use covered?      | no                                                  | no                                     | no                                                                                             |
| Referring domains [BL] | 757 / 1                                             | 1.59M / 1                              | 1,227 / 4                                                                                      |

**Why they win:** Google reads the query as "how often should I book", rewarding clinics with FAQ markup and fresh dates (PLAUSIBLE). **Gap:** all
three answer for the clinic; the Overview takes its home numbers from mdpen (#4, 0 page domains). **Edge:** only on the home variant. **Verdict:**
section of article 1 ("every 2 to 4 weeks at 0.5 mm, longer while the skin is still pink"; "can you do too much?"). No collagen claim for home
needling. No cannibalisation. Head term not winnable. **Blocker:** the set's weekly cadence (decision 4).

---

### 3. "after microneedling care" (US 151; microneedling after care 251 / 79; aftercare for microneedling 50 / 79) and "best products to use after microneedling" (GB 237; US 50) [VOL]

Volume note: the brief's 251 / 79 is "microneedling after care"; the exact phrase is 151 / 0.

**SERP (US):** clinic handouts and clinic blogs hold the top 3 and #6 to #8; Qure #4; YouTube #5. Overview: Virginia Facial Plastic Surgery, Byrdie,
Reddit, Park Derm and four more; "avoid … Vitamin C … for at least 5 to 7 days". PAA: best thing to put on skin after? · when do results show? · are 2
sessions enough? · all skin types? **SERP (GB):** Harley Street Skin Clinic, SkinCeuticals UK, Sublime Beauty, Byrdie, Green People, Banish, a
Skinstation collection, Yorkshire Skin Centre, Dr Pen UK; the Overview names a branded B5 serum and balm. PAA: best product after? · which serum? ·
what do I need? · fastest way to heal? [SERP] [PAA].

| Factor       | US #1 Derrington PDF                            | US #2 BH Skin         | US #3 Gold Coast clinic     | GB #1 Harley Street                         | GB #2 SkinCeuticals                    | GB #3 Sublime Beauty                                |
| ------------ | ----------------------------------------------- | --------------------- | --------------------------- | ------------------------------------------- | -------------------------------------- | --------------------------------------------------- |
| Shape        | 1-page handout, ~370 words, day 1 to 3 timeline | 1,568 words, 13 H2    | 1,417 words, day-by-day H3s | 1,506 words, 7 named moisturisers, 3 tables | snippet: HA, vitamin C, peptides (403) | 2,135 words, ingredient H3s, "what NOT to use", FAQ |
| Author, date | none; 2020                                      | Don Mehrabi; Aug 2025 | site admin; Dec 2025        | reviewed by Dr Aamer Khan; Mar 2026         | Mar 2025                               | Sara-Jayne Slack; May 2025                          |
| Domains [BL] | 835 / 2                                         | 1,569 / 17            | 329 / 3                     | 2,424 / 0                                   | 959 / 0                                | 73 / 0                                              |

**Why they win:** the searcher has just had a clinic procedure, and a clinic handout is the exact format (VERIFIED: a 370-word PDF is #1). GB wants named products; Sublime holds #3 on 73 domains, so intent beats authority (VERIFIED).
**Gap:** everyone assumes a clinic procedure; nobody covers a 0.5 mm home stamp. Vitamin C advice conflicts (SkinCeuticals for it; Sublime and the Overview against). Harley Street says wait "about 24 hours … before applying any products", against brands selling serums for immediate use.
**Edge:** none for products. Copper bans "speeds recovery after … microneedling", PDRN says "not on broken skin", Argireline never with needles [REG]; a list would also need competitor brands.
**Verdict:** two sections of article 1: a product-neutral timeline (hour 0, day 1, days 2 to 3, days 4 to 7) and the "never" list (retinoids, acids,
vitamin C, fragrance, heat, sweat, make-up), each sourced. A standalone home-aftercare spoke only once article 1 is on page one. "best products to use
after microneedling": do not build. No "soothes", "calms", "repairs", "heals" for any product of ours.

---

### 4. "microneedling serum" (US 402 [5,400]; GB 237) and "best microneedling serum" (US 151; GB 237; serum for microneedling 151 / 79; what serum to use with microneedling 100 / 79) [VOL]

**SERP "microneedling serum" (US, 2026-10-08):** no Overview; Reddit r/45PlusSkincare, Melanin Laser Clinic (231 words, 752 / 0), Reddit
r/Microneedling, RealSelf (47 words), answers.skin-beauty (59), Wellaholic (2,396, FAQPage), gopicky, acne.org [SERP] [PG]. PAA: What serum do I use
when microneedling? · best serum? · Do microneedle serums really work? · best professional serum?
**SERP "best microneedling serum" (US):** Dr Pen Australia, YouTube (Ms Longevity, 5,335 views, Mar 2025), Reddit, mdpen (7,134 words), drderme,
Timeless, Reddit, Amazon. The **Overview names hyaluronic acid, peptides and PDRN (salmon DNA)** and warns against L-ascorbic acid during needling
("granulomas"). PAA: What to use for microneedling glide? · Do microneedling serums work? · Can I use Alastin after? · Where to buy sterile hyaluronic
acid? [SERP] [PAA].

| Factor       | #1 Dr Pen Australia                                                                        | #2 YouTube                                                                                             | #3 Reddit                                                              |
| ------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| Opening      | "pairing your treatments with a serum … can considerably improve the benefits" (no answer) | "which serums are safe for microneedling at home and which ones can actually damage your skin barrier" | "the most basic, safe option … is hyaluronic acid … PDRN and exosomes" |
| Shape        | 815 words, no real H2s, 120 product links, Article; 2020, modified Sep 2026                | creator video                                                                                          | thread                                                                 |
| Advice       | EGF serum "during and after"; no vitamin C, retinoids or acids; patch test                 | –                                                                                                      | HA first                                                               |
| Domains [BL] | 296 / 7                                                                                    | –                                                                                                      | 1.59M / 0                                                              |

**Why they win:** a thin, forum-led SERP; the head term's top 5 are threads and 47 to 231-word pages (VERIFIED). **Gap:** nobody defines "sterile", shows what was tested on needled skin, or cites the FDA or the case series; the Overview's PDRN line has no evidence page behind it.

| Tested on needled skin                                   | Setting                                          | Result                                                                                                           | Transfers to a home stamp? |
| -------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Yogya 2022: 0.3% polynucleotide + HA vs saline, 29 women | clinic, after RF microneedling, 3 sessions       | wrinkle indentation around the eyes improved significantly by 2 months, where saline took 6; similar by 6 months | no (Malcolm, 2026-10-01)   |
| Li 2015: GHK-Cu, polymeric microneedle array             | excised human skin                               | 134 nmol passed in 9 h, almost none through intact skin; amount, not depth                                       | no                         |
| Soltani-Arabshahi 2014: 3 women                          | clinic, vitamin C serum with microneedle therapy | facial foreign-body granulomas                                                                                   | the warning                |
| FDA                                                      | regulator                                        | no device cleared for use with another product                                                                   | applies to all             |

**Edge:** this table and products matching the Overview's list; both gated. **Recommended article (build later):** "What Serum to Use With
Microneedling: What Was Tested" (53). Primary "microneedling serum"; secondaries best microneedling serum, serum for microneedling, what serum to use
with microneedling. H2s: what a serum for needled skin must be · why hyaluronic acid is the usual choice · what has been tested (table) ·
polynucleotides after clinic microneedling (Yogya) · copper peptide through microneedled skin (Li, amount not depth) · what never to put on needled
skin · what is in our vials (after decision 2) · when a clinic is better. Links up to `/collections/microneedling` and `/pages/pdrn-research`,
sideways to Yogya, down to the stamp set. 1,000 to 1,300 words.
**Gate:** decisions 1 and 2, and PDRN's "not on broken skin" squared with the PDRN set; until then write nothing (as decided 2026-10-08). **Guardrails:** "polynucleotide" for Yogya; Li in claim 7's wording; no brand ranking.
**Cannibalisation:** remove "microneedling serum" from the collection's secondaries when this ships; keep product pages off it (the DE copper serum drew "ghk cu microneedling serum", 2 impressions, 90 days).
**Winnable? Target:** "microneedling serum" US page one 6 months after publication, top 3 in 9 to 12; "best" page one in 6 to 9. **Decides it:** the gate, not the competition.

---

### 5. Hair-led stamp terms: "derma stamp" (US 8,154 [18,100]; GB 3,088), "how to use a derma stamp" (US 151; GB 79), "how to derma stamp" (GB 237; US 50), "derma stamp vs derma roller" (US 251; GB 158) [VOL]

**SERP shape:** "derma stamp" is transactional (popular products; a video block of three hair videos from one creator): Dr Pen product (face, hair and
beard, adjustable 0.5 to 3 mm, $29, 4.8 stars from 90), Amazon, Zenagen (scalp), Rhute (hair), Target; GB adds Pure Derma (0.25 to 3.0 mm, £18.95, 4.8
from 133). How-to: US top 8 is 4 hair, 3 face, 1 mixed; GB top 8 is 6 hair. Comparison: 2 hair-led (Rhute, Hairgenetix), 3 face-led or mixed, 1
Instagram post. All five Overviews cite Rhute among their first three sources; the comparison Overview cites Hairgenetix fifth [SERP] [FETCH].
**PAA:** Does the derma stamp actually work? · Will derma stamp regrow hair? · How hard should you press a derma stamp? · Do dermatologists recommend
derma stamps? [PAA].

| Keyword                          | #1                                      | #2                                                                                                 | #3                                                |
| -------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| derma stamp (US)                 | Dr Pen product, 885 words, 108 / 2      | Amazon search                                                                                      | Zenagen scalp product, 141 words, 1,137 / 1       |
| how to use a derma stamp (US)    | Instagram reel, hair                    | Dr Pen AU 2020 launch post, 848 words, no steps or needle length, "Amazing for Hair Loss", 296 / 2 | Instagram reel, scar-roller ad                    |
| how to derma stamp (GB)          | Rhute hair how-to, 2,189 words, 929 / 0 | YouTube short, hair                                                                                | Watermans hair guide, 2,911 words, 1,538 / 0      |
| derma stamp vs derma roller (US) | Reddit r/SkincareAddiction, 2019        | Rhute hair comparison, 2,231 words                                                                 | Dr Pen UK "3 Tools", 1,961 words, a table, 42 / 0 |

Hairgenetix's comparison (#5): 3,393 words, 4 tables, 30 citations, video, modified 2 Oct 2026 [PG].

**Why they win:** exact-title brand how-tos and product pages on 100 to 1,500-domain sites, plus video (VERIFIED). On the comparison a 2019 thread and
Rhute beat a deeper Hairgenetix page, so freshness and forum trust beat depth (PLAUSIBLE). **Gap (face):** no face stamp how-to in either top 3 except
Dr Pen AU, which has no steps. **Edge:** none that would not take traffic from the sister brand.
**Verdict: do not build any of the four.** Face variants become H2s of article 1 ("How to use a derma stamp on your face"; "Stamp, roller or pen for
the face?", no "vs" in the heading). Our product pages may say "facial derma stamp", never the bare term in a title. **Cannibalisation:**
Hairgenetix's heroes: stamp set for "derma stamp", stamp guide for "how to use a derma stamp", comparison page for "stamp vs roller" [HG]; a
Skingenetix page would split one owner's signals across two domains.

---

## What can and cannot be said (all microneedling articles)

**Can say, source named:** the FDA's position (no microneedling medical device authorised for over-the-counter sale; cleared devices are mostly
motorised pens for adults 22 and older, used by trained providers; short-needle products claiming only appearance are not devices; none cleared for
use with another product; its risk list: bleeding, bruising, redness, peeling, stinging from skincare, dark or light spots, cold-sore flare-ups,
infection). Needle length: sources disagree (0.3 vs 0.5 mm) and ours is 0.5 mm. Frequency: every 2 to 4 weeks at 0.5 mm. Technique: press straight
down, lift, never drag; pinpoint bleeding means the needles are too long for home use (Vogue). Hygiene: disinfect as the maker instructs (sources cite
a 70% isopropyl alcohol soak), dry fully, never share, replace the head. Clinic microneedling as context, never equated with the home stamp. Yogya, Li
and Soltani-Arabshahi exactly as in section 4.

**Cannot say:** "absorb deeper", "delivers serums through micro-channels", "penetrates", "reaches the dermis", any "× more absorption" (live on both
stamp pages and the collection [OWN]: decision 5). "Stimulates collagen" for the home stamp; "heals", "repairs", "soothes", "speeds recovery". Acne
scars, stretch marks, hyperpigmentation, melasma. "Safe", "gentle", "suitable for sensitive skin", "clinically proven". Any suggestion to use the
Argireline, Matrixyl or glutathione serum, a cream, or anything but the set's own vials on needled skin; PDRN on needled skin waits for decision 1.
Botox or "clinic at home" equivalence; hair growth; before/after images; competitor brand names.

**Safety block:** do not microneedle at home with active acne, open wounds, infected or irritated skin, active eczema, keloid tendency, slow healing,
diabetes, a weakened immune system, a bleeding disorder or blood thinners (FDA; Ammuri); ask first if prone to cold sores (the FDA lists flare-ups).
Not tested in pregnancy: ask a doctor or pharmacist. Patch-test the serum on intact skin, never on needled skin. PDRN: not with a fish allergy.
Copper: no pure L-ascorbic acid, strong acids or high-strength retinol around a session. See a professional for scars or deep wrinkles, and at once
for spreading redness, heat, swelling, discharge or fever. **Register conflict, flagged in every article:** Argireline forbids DIY microneedling;
copper sells the stamp on grade-C ex vivo evidence; PDRN says "not on broken skin"; no register covers microneedling safety.

## Ranked summary

| Keyword                                                        | Demand (US / GB)          | Winnable                               | Edge                                               | Verdict                                                  |
| -------------------------------------------------------------- | ------------------------- | -------------------------------------- | -------------------------------------------------- | -------------------------------------------------------- |
| at home microneedling (+ how to at home, derma stamp for face) | 1,510 / 475 (+ 401 / 237) | GB page one 6 to 12 mo; US page one 12 | reviewer, sourced honesty, real tool; no authority | **build** (after decisions 1, 3, 4)                      |
| microneedling serum + best microneedling serum                 | 553 / 474                 | page one 6 mo after publication        | evidence table, matching products                  | **build later** (gate: decisions 1, 2)                   |
| how often to do microneedling                                  | 402 / 79                  | head term no                           | home answer only                                   | **section on article 1**                                 |
| after microneedling care / microneedling after care            | 402 / 79                  | not alone yet                          | none for products                                  | **section on article 1**; spoke later                    |
| best products to use after microneedling                       | 50 / 237                  | needs brand names                      | none                                               | **do not build**                                         |
| best at home microneedling                                     | 553 / 158                 | publisher round-ups                    | none                                               | **do not build** (PAA answered with criteria)            |
| derma stamp vs derma roller                                    | 251 / 158                 | Hairgenetix #5                         | none                                               | **do not build** (face H2 only)                          |
| how to use a derma stamp / how to derma stamp                  | 201 / 316                 | hair-led                               | none                                               | **do not build** (face H2 only)                          |
| derma stamp                                                    | 8,154 / 3,088             | product SERP, hair-led                 | none                                               | **do not build** ("facial derma stamp" on product pages) |

## Decisions for Malcolm

1. **Register conflict:** (a) the set's own vials only, applied after needling, if decision 2 confirms they suit needled skin; or (b) Ammuri's
   posture: needle bare skin, serums only on settled intact skin (changes both products' concept). PDRN's "not on broken skin" must give way or the
   PDRN set must change.
2. **Formulator:** are the vials sterile, fragrance-free, free of ascorbic acid or derivatives (copper gap 5 mentions 3-O-ethyl ascorbic acid in a copper formula) and made for needled skin? Is the stamp head sterile and replaceable, on what schedule?
3. **Needle length:** keep 0.5 mm and say it is the top of the home range, or add a 0.25 to 0.3 mm head for beginners.
4. **Frequency:** four single-use vials as "a one-month ritual" means weekly sessions at 0.5 mm, against every 2 to 4 weeks in two sources; relabel as a two-to-four-month set or change the count.
5. **Live wording and schema:** "absorb deeper" (stamp pages) and "deliver … through fine, sterile micro-channels" (collection) against claim 7's conditions; set `PreOrder` with a date (today `InStock`).
6. **Cross-brand link:** one contextual link from article 1 to Hairgenetix's stamp guide for scalp readers: yes or no.
