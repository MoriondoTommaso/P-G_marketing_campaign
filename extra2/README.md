# Extra 2 test input: OpenStreetMap counts near each store

> **STATUS: done, 26 Nov 2026.** The counts were tested on the final workflow
> (`workflows/oral-b-italy-final.knwf`, bottom row, nodes #107–#118): the tree earns
> €88,000 with and without the 3 usable OSM counts, with the same confusion matrix,
> so OSM is dropped. Result and keep rule in
> [`docs/additional-data.md`](../docs/additional-data.md#osm-test-result-26-nov-2026).

Team 2 · Ele · prepared 24 Nov 2026 · issue #4 / Extra 2

This folder holds one **free** data source for the Extra 2 test in
[`docs/additional-data.md`](../docs/additional-data.md#how-we-would-test-it):
how many dentists, pharmacies, schools, supermarkets and drugstores sit near
each of our 480 stores, according to OpenStreetMap (OSM).

It is a candidate **input**, like a purchased file. It is not a result. Any
number for the deck must come from the KNIME rerun described below.

## Decisions fixed before any count was computed

These choices were written down **before** the counting script was run, so no
result could influence them.

| Decision | Choice | Why |
|---|---|---|
| OSM snapshot | Geofabrik `italy-260101.osm.pbf` (OSM data as of 1 Jan 2026) | The 2026 campaign dates are not in our files. A 1 January 2026 snapshot was available before any 2026 activation, so it passes the "measurement date before the campaign" rule in the test plan. Today's OSM would include shops added during and after the campaign. |
| Radius | **1 km straight-line** around the store's latitude/longitude | About a 12–15 minute walk: the neighbourhood a shopper can reach on foot. One fixed value only, never tuned; trying several radii and keeping the best would be a hidden search on the 170 labelled stores. Rural stores will often score 0; that is information, not an error. |
| Store location | `Latitude` and `Longitude` from `outputs/store-universe.csv` (national store file) | Never the activation file's coordinates: their missingness depends on the outcome. The script does not read `success` or `target`. |
| What counts as each type | dentists: `amenity=dentist` or `healthcare=dentist`; pharmacies: `amenity=pharmacy` or `healthcare=pharmacy`; schools: `amenity=school`; supermarkets: `shop=supermarket`; drugstores: `shop=chemist` (OSM's tag for *drogheria / profumeria*) | Standard OSM tags. Points, buildings and areas are all counted; buildings and areas are placed at the average of their corner points. |
| Regions | South: latitude < 41.5; Centre: 41.5–44.5; North: ≥ 44.5 | The same primary bands as [`docs/evaluation.md`](../docs/evaluation.md). |
| "Too thin" rule | In a region, if OSM finds **fewer than 80%** of the official pharmacies within 1 km of our stores, OSM is too thin there | Pharmacies are the only type with an official national list (Ministry of Health, IODL 2.0), so they are our completeness yardstick. We use only register pharmacies open on 1 Jan 2026 and with coordinates. We also report the share of stores with zero of each type. |

**Assumption:** the 2026 campaign dates are not in our files. We assume no
activation started before 1 January 2026.

## Coverage result (run 24 Nov 2026, before any model test)

OSM file `italy-260101.osm.pbf`, MD5 `b1058774150ace61a7bd3c0a301e6af0` (matches Geofabrik).
Italy-wide OSM places found: 2,451 dentists, 16,110 pharmacies, 23,891 schools,
18,651 supermarkets, 1,868 drugstores. Register: 20,734 pharmacies open on
1 Jan 2026, 18,950 of them with coordinates.

| Stores with ≥ 1 place within 1 km | North | Centre | South | Italy |
|---|---:|---:|---:|---:|
| All 480: any of the five types | 95% | 89% | 89% | 91% (436) |
| Labelled 170: any of the five types | 94% | 94% | 92% | 94% (159) |
| All 480: dentists | 30% | 28% | 20% | 26% |
| All 480: drugstores | 31% | 33% | 18% | 28% |
| All 480: pharmacies / schools / supermarkets | 79 / 74 / 87% | 75 / 73 / 80% | 75 / 78 / 74% | 76 / 75 / 81% |

- **The pre-set "too thin" rule passes everywhere, but the yardstick is not clean.**
  Near our stores OSM finds *more* pharmacies than the register (ratio 1.14–1.32).
  Likely causes: a pharmacy mapped twice (point and building), *parafarmacie*
  tagged as pharmacies, and 8.6% of register pharmacies without coordinates.
  Across each whole region OSM finds 94% (North), 84% (Centre) and **75% (South)**
  of official pharmacies, so OSM is probably thinner in the South.
- **Dentists are very thin in OSM everywhere.** 2,451 places for all of Italy is
  a small fraction of the country's dental practices, and 74% of stores have
  none within 1 km. A zero mostly means "not mapped", not "no dentist". This
  weakens OSM for gap G1, the main reason it was shortlisted. Drugstores are
  similarly thin (72% zero).
- Pharmacies, schools and supermarkets are usable inputs for the test.

## Files

| File | What it is |
|---|---|
| `osm_counts.py` | The script that reads the OSM snapshot and writes both CSVs. Reads only `store_id`, `Latitude`, `Longitude`. |
| `osm-counts-2026-01-01.csv` | One row per store (480), sorted by `store_id`: five counts within 1 km, plus the snapshot date and radius. |
| `osm-coverage-2026-01-01.csv` | Coverage check by region: stores, average count and share of stores with zero, per type; OSM vs. official pharmacies. |

Only the counts and the script are kept here. The 2.1 GB OSM file and the
pharmacy register are downloaded to a scratch folder and not committed.

## Privacy

The store coordinates never leave this computer. The OSM file is a whole-Italy
download, and all counting happens locally. No store location is sent to any
web service.

## Licences and credit

- OpenStreetMap data © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright). Extract by [Geofabrik](https://download.geofabrik.de/europe/italy.html).
- Pharmacy register: Ministero della Salute, [Farmacie](https://www.dati.salute.gov.it/it/dataset/farmacie/), [IODL 2.0](http://www.dati.gov.it/iodl/2.0/). Used only for the coverage check, never as a predictor.

## How it was tested in KNIME

In the final workflow, not in RC3. The test sits in its own row at the bottom
of `oral-b-italy-final.knwf`, so the main model and its outputs are untouched.

1. **CSV Reader (#107)** reads `osm-counts-2026-01-01.csv`, which travels inside
   the workflow (`data/inputs`).
2. **Joiner (#108)** adds the counts to the 170 stores with a known result, on
   `Pdv Code` = `store_id`, matching rows only, row order *Input order* so every
   store keeps its fold.
3. **Column Filter (#109)** keeps the same 5 store traits, `target` and the 3
   usable counts: pharmacies, schools and supermarkets.
4. **#110–#118** are a copy of the tree row (X-Partitioner seed 2026, Learner,
   Predictor, X-Aggregator, 60% rule, Scorer, € per store, total), unchanged.

Result: €88,000, confusion matrix 100 / 8 / 8 / 54 and AUC 0.864, all identical to the tree without OSM.

## Reproduce

```sh
python3 -m venv /tmp/osm-venv && /tmp/osm-venv/bin/pip install osmium
curl -O https://download.geofabrik.de/europe/italy/italy-260101.osm.pbf
curl -O https://www.dati.salute.gov.it/sites/default/files/opendata/FRM_FARMA_5_20261124.csv
/tmp/osm-venv/bin/python -I extra2/osm_counts.py italy-260101.osm.pbf FRM_FARMA_5_20261124.csv
```
