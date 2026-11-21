# Extra 2 — Additional data

Team 2 · Ele (lead) and Deniz

**Status:** longlist and test plan drafted by Deniz on 21 Nov. Ele narrows the list to the 3–4 best sources and writes the recommendation on 22 Nov.

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

| # | Source | Gap filled | Free / paid (cost) | Italy coverage | How it links to our stores | Effort | Usefulness (hypothesis) |
|---|---|---|---|---|---|---|---|
| 1 | **ISTAT permanent census** (population, education, employment, households) — [istat.it](https://www.istat.it) | G2, G5 | Free | National, municipality and census-section level | Store lat/lon → municipality using the ISTAT boundary file (source 10) | Low–medium | Medium. It overlaps the census traits we already have, so the main gain would be finer detail. |
| 2 | **ISTAT commuting matrix** (home-to-work and home-to-school flows) — [istat.it](https://www.istat.it) | G2, G4 (traffic proxy) | Free | National, municipality to municipality | Same municipality join; inflow per municipality | Medium | Medium. A proxy for daytime traffic past a store. Latest full matrix is census-based, so check how recent it is. |
| 3 | **MEF taxable income by municipality** (IRPEF statistics) — [finanze.gov.it](https://www1.finanze.gov.it/finanze/analisi_stat/) | G5 | Free | National, every municipality, published yearly | Municipality join | Low | Medium. Tests whether income matters once geography is controlled for. |
| 4 | **OpenStreetMap** points of interest: dentists, pharmacies, supermarkets, competing stores, schools — [openstreetmap.org](https://www.openstreetmap.org), Italy extract from [Geofabrik](https://download.geofabrik.de/europe/italy.html) | G1, G2, G4 (competition) | Free (ODbL licence; credit OSM) | National. Completeness varies by area. | Count points within a radius of the store lat/lon | Medium | High for G1: an independent dentist count could explain the middle range. Check completeness first. |
| 5 | **Ministry of Health pharmacy register** (pharmacy list with addresses) — [dati.salute.gov.it](https://www.dati.salute.gov.it) | G1, G4 | Free | National | Count pharmacies within a radius; geocode where coordinates are missing | Medium | Medium. Pharmacies are another channel for oral care advice. |
| 6 | **Agenzia delle Entrate OMI property values** (house prices by area) — [agenziaentrate.gov.it](https://www.agenziaentrate.gov.it) | G5 | Free | National, OMI micro-zones | Store lat/lon → OMI zone | Medium | Low–medium. An affluence proxy finer than the municipality. |
| 7 | **Store-level retail sales panel** (e.g. NielsenIQ, Circana) | G4, G3 | Paid. Price on quote; not public. | Panel stores only. Coverage of our 480 is unknown. | Store code mapping from the provider | High | High, if it covers our stores: past oral care sales per store is the most direct signal. |
| 8 | **Footfall / mobility data** (mobile-network or app-based panels) | G4, G2 | Paid. Price on quote. | National, depending on the provider | Visits within a radius of the store lat/lon | Medium–high | Medium–high. Measures shopper traffic directly. |
| 9 | **Retailer loyalty-card data** (via a retailer partnership) | G4 | Paid or partnership. Cost depends on the deal. | One retailer's stores only | Retailer store code | High | High for that retailer: basket and category data. Limited coverage. |
| 10 | **P&G store audits / retail execution data** (shelf share, display, out-of-stock, store format) | G4, G6 | Internal. Cost is staff time and access. | Stores P&G's field team visits | P&G store code (likely the same as `store_id`) | Low–medium | High. Probably the cheapest store-level data. |
| — | **ISTAT administrative boundaries** (municipality and census-section shapes) — [istat.it](https://www.istat.it) | Enabler for 1, 2, 3, 6 | Free | National | Point-in-polygon on store lat/lon | Low | Needed to link any area data. Not a predictor. |

**Not in scope:** a 2027 pilot that deliberately includes under-covered stores (G1–G3) is not a data purchase, but it may fill G3 faster than any of the sources above. Hand it to Team 4 for the uncertainty slide.

### For Ele: shortlist and recommendation (22 Nov)

- [ ] Pick the 3–4 best sources, mixing free and paid. Plan suggestion: ISTAT, MEF and OSM as free sources; store sales panel, footfall, loyalty data and P&G audits as paid.
- [ ] Link each source to a gap (G1–G6) above.
- [ ] Recommend **one source to buy first** and say why.
- [ ] Draft one slide with an action title (storyboard slide 9).
- [ ] Confirm every link and licence before delivery. The URLs above point to the publishers' main sites and need checking for the exact dataset page.

## How we would test it

The test is the same for any new source. We compare the **expected net €** with and without the new data, using the **same 5 folds** as the main model, so the only thing that changes is the data.

1. **Freeze the reference.** Take Team 3's chosen model and settings exactly as in [`docs/evaluation.md`](evaluation.md): seed `20261120`, the same `outputs/folds.csv` (5 folds, 34 stores each) and the same learner settings. Record its pooled held-out net € and the net in each fold. This is the **without** result.
2. **Add the new data.** Join the new variables to `store-universe.csv` by `store_id`, using the link method in the longlist. Do not use anything from the activation file. Decide which new columns to add **before** looking at any results, and write them down.
3. **Prepare inside the folds.** Fill missing values and scale the new columns inside each training fold only, exactly as for the existing traits (Team 3's fold-local preparation). Stores the new source does not cover stay missing and are filled inside the fold. Record how many stores are missing per fold.
4. **Rerun the same 5 folds.** Fit the same model type with the old and new columns. Score each held-out fold, and fund a store when its expected net, €2,500 × p − €1,500, is greater than €0.
5. **Compare.** For each fold and pooled, report: funded stores, funded successes and failures, realised net €, and the Brier score. Report the difference in net € (with − without) per fold.
6. **Decide.** **Keep the new data only if the pooled held-out net € improves** and the improvement holds in at least 3 of 5 folds, the same stability rule as in `docs/evaluation.md`. Also check the 43° north/south split, so that the gain does not come from one band only. If the net does not improve, report that honestly and drop the source.
7. **Report the limits.** Even a held-out improvement describes the 170 stores activated in 2026. It does not prove the gain for never-activated stores, especially in the gaps G1–G3. For a paid source, compare the measured net € gain with the source's price before buying at scale.

**Before buying:** ask the provider for a free sample covering our 480 stores, and check coverage first. If a source covers fewer than about half of the labelled stores, the 5-fold test has too little data to show a difference.
