# Extra 2: Additional data

Team 2 · Ele (lead) and Deniz

**Status:** longlist and test plan drafted by Deniz on 21 Nov. Shortlist, buy-first recommendation, dataset links, licences and the PR #32 test-plan update added by Ele on 24 Nov. Slide 9 draft is below and in the [storyboard](../presentation/storyboard.md).

**Rule:** we claim no improvement we have not tested. Every benefit below is a **hypothesis** until the test in the last section has been run.

## Gaps we want to fill (from T07)

The gaps come from [`docs/store-insights.md`](store-insights.md#3-data-gaps-sent-to-ele-for-extra-2):

- **G1:** Distance from a Dentist, 25–100: 190 never-activated stores, only 13 activated. In the south, 35 never-activated stores are further from a dentist than any activated southern store.
- **G2:** Stores with no schools nearby: 157 never-activated stores, 27 activated (25 failed).
- **G3:** Few labelled failures in the centre and south (9 failures in total, against 227 never-activated stores).
- **G4:** No store-level data: sales, footfall, size or format, retailer, shelf space, competitors.
- **G5:** Income only separates success from failure through the north/south split.
- **G6:** Water hardness separates success from failure strongly, but we cannot explain why.

## Longlist (about 10 sources)

**How each source links to our stores:** our stores have latitude and longitude. Area data (by municipality or census section) joins by locating each store inside an ISTAT boundary file. Point data (shops, dentists) joins by counting points within a fixed radius of the store. Store-level data joins on a store code, which needs a mapping from the retailer or data provider to our `store_id`.

Licences were checked on 24 Nov 2026 on the publisher pages linked below. Recheck them before any commercial use.

| # | Source | Gap filled | Free / paid (cost) and licence | Italy coverage | How it links to our stores | Effort | Usefulness (hypothesis) |
|---|---|---|---|---|---|---|---|
| 1 | **ISTAT permanent census** (population, education, employment, households), data in [IstatData](https://esploradati.istat.it) | G2, G5 | Free. [CC BY 4.0](https://www.istat.it/note-legali/) (credit "Istat") | National, municipality and census-section level | Store lat/lon → municipality using the ISTAT boundary file (source 11) | Low–medium | Medium. It overlaps the census traits we already have, so the main gain would be finer detail. |
| 2 | **ISTAT commuting matrix** (home-to-work and home-to-school flows), [contiguity, distance and commuting matrices](https://www.istat.it/notizia/matrici-di-contiguita-distanza-e-pendolarismo/) | G2, G4 (traffic proxy) | Free. [CC BY 4.0](https://www.istat.it/note-legali/) (credit "Istat") | National, municipality to municipality | Same municipality join; inflow per municipality | Medium | Medium. A proxy for daytime traffic past a store. The 2021 work matrix is estimated from census and administrative data, not counted directly; check how recent each edition is. |
| 3 | **MEF taxable income by municipality** (main IRPEF variables), [municipal open data](https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?search_class%5B0%5D=cCOMUNE&opendata=yes) | G5 | Free. [CC BY 3.0 IT](http://creativecommons.org/licenses/by/3.0/it/), as stated on the [declarations page](https://www1.finanze.gov.it/finanze/pagina_dichiarazioni/public/dichiarazioni.php) (credit "MEF - Dipartimento delle Finanze") | National, every municipality, published yearly (latest: tax year 2024) | Municipality join | Low | Medium. Tests whether income matters once geography is controlled for. |
| 4 | **OpenStreetMap** points of interest: dentists, pharmacies, supermarkets, competing stores, schools, Italy extract from [Geofabrik](https://download.geofabrik.de/europe/italy.html) | G1, G2, G4 (competition) | Free. [ODbL](https://www.openstreetmap.org/copyright) (credit "© OpenStreetMap contributors") | National. Completeness varies by area. | Count points within a radius of the store lat/lon | Medium | High for G1: an independent dentist count could explain the middle range. Check completeness first. |
| 5 | **Ministry of Health pharmacy register** (pharmacy list with addresses, updated daily), [Farmacie dataset](https://www.dati.salute.gov.it/it/dataset/farmacie/) | G1, G4 | Free. [IODL 2.0](http://www.dati.gov.it/iodl/2.0/) | National | Count pharmacies within a radius; geocode where coordinates are missing | Medium | Medium. Pharmacies are another channel for oral care advice. |
| 6 | **Agenzia delle Entrate OMI property values** (house prices by area), OMI data downloads in the Agenzia's online services area, [agenziaentrate.gov.it](https://www.agenziaentrate.gov.it) | G5 | Free, but needs a Fisconline/Entratel login. **No open licence found:** reuse follows the Agenzia's own terms of use (credit "Agenzia Entrate - OMI"); commercial use unconfirmed. | National, OMI micro-zones | Store lat/lon → OMI zone | Medium | Low–medium. An affluence proxy finer than the municipality. |
| 7 | **Store-level retail sales panel** (e.g. NielsenIQ, Circana) | G4 (G3 only indirectly: it describes centre and south stores but adds no outcomes) | Paid. Price on quote; not public. Commercial licence set by contract. | Panel stores only. Coverage of our 480 is unknown. | Store code mapping from the provider | High | High, if it covers our stores: past oral care sales per store is the most direct signal. |
| 8 | **Footfall / mobility data** (mobile-network or app-based panels) | G4, G2 | Paid. Price on quote. | National, depending on the provider | Visits within a radius of the store lat/lon | Medium–high | Medium–high. Measures shopper traffic directly. |
| 9 | **Retailer loyalty-card data** (via a retailer partnership) | G4 | Paid or partnership. Cost depends on the deal. | One retailer's stores only | Retailer store code | High | High for that retailer: basket and category data. Limited coverage. |
| 10 | **P&G store audits / retail execution data** (shelf share, display, out-of-stock, store format) | G4, G6 | Internal. Cost is staff time and access. | Stores P&G's field team visits | P&G store code (likely the same as `store_id`) | Low–medium | High. Probably the cheapest store-level data. |
| 11 | **ISTAT administrative boundaries** (municipality and census-section shapes, yearly at 1 January), [boundaries for statistical purposes](https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici/) | Enabler for 1, 2, 3, 6 | Free. [CC BY 4.0](https://www.istat.it/note-legali/) under ISTAT's site-wide terms; no file-specific licence found on the download page. | National | Point-in-polygon on store lat/lon | Low | Needed to link any area data. Not a predictor. |

**Not in scope:** a 2027 pilot that deliberately includes under-covered stores (G1–G3) is not a data purchase, but it may fill G3 faster than any of the sources above. Hand it to Team 4 for the uncertainty slide.

### For Ele: shortlist and recommendation (24 Nov)

- [x] Pick the 3–4 best sources, mixing free and paid.
- [x] Link each source to a gap (G1–G6) above.
- [x] Recommend **one source to buy first** and say why.
- [x] Draft one slide with an action title (storyboard slide 9).
- [x] Replace homepage links with the dataset pages and note each licence (24 Nov). OMI has no open licence; its download page sits behind a login.

| Priority | Source (longlist #) | Type and cost | Gaps | Why it is on the shortlist (hypothesis until tested) |
|---|---|---|---|---|
| 1 | **P&G store audits / retail execution data** (#10) | Internal. Staff time and access. | G4, G6 | Store format, shelf share, displays and out-of-stocks per store. It may explain why water hardness separates stores. Probably the cheapest store-level data. |
| 2 | **OpenStreetMap dentists, pharmacies and schools** (#4) | Free, ODbL | G1, G2 | An independent count of dentists and schools near each store, where our 2026 evidence is thinnest. Check completeness by region first. |
| 3 | **MEF income by municipality** (#3) | Free, CC BY 3.0 IT | G5 | Yearly, dated municipality income. Tests whether income matters once north/south is accounted for. Needs the ISTAT boundaries (#11) to link. |
| 4 | **NielsenIQ / Circana store sales panel** (#7) | Paid, price on quote | G4 (G3 only indirectly) | Past oral care sales per store, the most direct store-level signal. **Buy first** (below). |

**Buy first: the store sales panel (NielsenIQ or Circana).** It is the only shortlisted source with **dated** store sales before and after the 2026 campaign. Because every value has a date, we can keep only weeks before the 2026 activation as predictors. That protects the new data against the leakage question raised in PR #32. It does **not** date the five workbook fields we already use: Team 2's request to the data provider still stands. Before signing, get a free sample for our 480 stores and check coverage (see "Before buying"). The P&G audits and the two free sources should be requested in parallel, because they cost little.

**No data source fills G3.** G3 is a shortage of labelled failures in the centre and south. New predictors cannot create outcomes. Only the bounded pilot in [`model-review/pilot.md`](model-review/pilot.md) can, by activating stores there and recording what happens.

### Slide 9 draft

**Action title:** Buy store-level sales history first, after a free coverage check on our 480 stores

| Source | Fills | Cost |
|---|---|---|
| Store sales panel (NielsenIQ / Circana): **buy first** | No sales or store data today | Paid, on quote |
| P&G store audits | Store format, shelf, displays | Internal |
| OpenStreetMap dentists and schools | Areas with little 2026 evidence | Free |
| MEF income by municipality | Whether income matters beyond north/south | Free |

- **Why this one:** only dated store sales let us use pre-2026 weeks and avoid leakage.
- **How we test it:** same 5 folds, same model; keep it only if held-out net € improves in at least 3 of 5 folds. The result is **retrospective**; the pilot confirms it.
- **What data cannot fix:** too few failed stores in the centre and south. Only the pilot adds those outcomes.
- **Footnote:** no improvement is claimed until tested; licences in `docs/additional-data.md`.

## How we would test it

The test is the same for any new source. We compare the **expected net €** with and without the new data, using the **same 5 folds** as the main model, so the only thing that changes is the data.

**Every fold result is retrospective.** The same 5 folds already compared and selected the tree ([`model-review/pilot.md`](model-review/pilot.md)), so a gain on them may overstate the gain on new stores. Label every number from this test "retrospective (2026 activated stores)". Only fresh stores, such as the bounded pilot, give a prospective answer.

1. **Freeze the reference.** Take Team 3's chosen model and settings exactly as in [`docs/evaluation.md`](evaluation.md): seed `20261120`, the same `outputs/folds.csv` (5 folds, 34 stores each) and the same learner settings. Record its pooled held-out net € and the net in each fold. This is the **without** result.
2. **Add the new data.** Join the new variables to `store-universe.csv` by `store_id`, using the link method in the longlist. Do not use anything from the activation file. Decide which new columns to add **before** looking at any results, and write them down.
   **Measurement dates are required.** For every new column, record its measurement or reference date and confirm it was available before the 2026 activation. Drop any column without a date, or measured during or after the campaign: it could leak the outcome (see PR #32).
3. **Prepare inside the folds.** Fill missing values and scale the new columns inside each training fold only, exactly as for the existing traits (Team 3's fold-local preparation). Stores the new source does not cover stay missing and are filled inside the fold. Record how many stores are missing per fold.
4. **Rerun the same 5 folds.** Fit the same model type with the old and new columns. Score each held-out fold, and fund a store when its expected net, €2,500 × p − €1,500, is greater than €0.
5. **Compare.** For each fold and pooled, report: funded stores, funded successes and failures, realised net €, and the Brier score. Report the difference in net € (with − without) per fold.
6. **Decide.** **Keep the new data only if the pooled held-out net € improves** and the improvement holds in at least 3 of 5 folds, the same stability rule as in `docs/evaluation.md`. If the net does not improve, report that honestly and drop the source. We do not use a north/south split here: both geographic splits failed the minimum-data rule in [`model-choice.md`](model-choice.md), so they cannot show whether a gain transfers between regions.
7. **Report the limits.** Label the result **retrospective**. Even a held-out improvement describes the 170 stores activated in 2026. It does not prove the gain for never-activated stores, especially in the gaps G1–G3, or across regions. Confirm it in the bounded pilot before relying on it. For a paid source, compare the measured net € gain with the source's price before buying at scale.

**Before buying:** ask the provider for a free sample covering our 480 stores, and check coverage first. If a source covers fewer than about half of the labelled stores, the 5-fold test has too little data to show a difference.
