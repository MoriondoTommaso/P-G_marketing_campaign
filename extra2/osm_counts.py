"""Extra 2: count OpenStreetMap places within 1 km of each store.

Usage (needs the `osmium` package, see README.md):
    python -I extra2/osm_counts.py <italy-260101.osm.pbf> <FRM_FARMA_5_*.csv>

Reads only store_id, Latitude and Longitude from outputs/store-universe.csv.
It never reads the outcome columns. All choices (snapshot, radius, tags,
regions, "too thin" rule) were fixed in README.md before this script ran.
"""
import csv
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import osmium

ROOT = Path(__file__).resolve().parents[1]
STORES = ROOT / "outputs" / "store-universe.csv"
OUT_DIR = ROOT / "extra2"
SNAPSHOT = "2026-01-01"
SNAPSHOT_DAY = date(2026, 1, 1)
RADIUS_KM = 1.0
TYPES = ("dentists", "pharmacies", "schools", "supermarkets", "drugstores")
THIN_RATIO = 0.80  # OSM must find at least 80% of official pharmacies


def kind(tags):
    """Map OSM tags to one of our five place types, or None."""
    amenity, health, shop = tags.get("amenity"), tags.get("healthcare"), tags.get("shop")
    if amenity == "dentist" or health == "dentist":
        return "dentists"
    if amenity == "pharmacy" or health == "pharmacy":
        return "pharmacies"
    if amenity == "school":
        return "schools"
    if shop == "supermarket":
        return "supermarkets"
    if shop == "chemist":
        return "drugstores"
    return None


def band(lat):
    """Primary latitude bands from docs/evaluation.md."""
    return "South" if lat < 41.5 else "Centre" if lat < 44.5 else "North"


def read_osm(pbf):
    """Return {type: [(lat, lon), ...]} for points, buildings and areas.

    Three passes keep memory small: relations, then ways, then nodes.
    Buildings and areas are placed at the mean of their node locations.
    """
    rel_type, rel_ways = {}, {}
    for r in osmium.FileProcessor(pbf, osmium.osm.RELATION):
        k = kind(r.tags)
        if k and r.tags.get("type") == "multipolygon":
            rel_type[r.id] = k
            rel_ways[r.id] = [m.ref for m in r.members if m.type == "w" and m.role != "inner"]
    member_ways = {w for ws in rel_ways.values() for w in ws}

    way_type, way_nodes = {}, {}
    for w in osmium.FileProcessor(pbf, osmium.osm.WAY):
        k = kind(w.tags)
        if k or w.id in member_ways:
            if k:
                way_type[w.id] = k
            way_nodes[w.id] = [n.ref for n in w.nodes]
    needed = {n for ns in way_nodes.values() for n in ns}

    points = defaultdict(list)
    coords = {}
    for n in osmium.FileProcessor(pbf, osmium.osm.NODE):
        if n.id in needed:
            coords[n.id] = (n.location.lat, n.location.lon)
        k = kind(n.tags)
        if k:
            points[k].append((n.location.lat, n.location.lon))

    def centre(node_ids):
        pts = [coords[i] for i in dict.fromkeys(node_ids) if i in coords]
        if not pts:
            return None
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

    for wid, k in way_type.items():
        c = centre(way_nodes[wid])
        if c:
            points[k].append(c)
    for rid, k in rel_type.items():
        c = centre([n for w in rel_ways[rid] for n in way_nodes.get(w, [])])
        if c:
            points[k].append(c)
    return points


def read_register(path):
    """Official pharmacies open on the snapshot day, with coordinates."""
    def day(s):
        d, m, y = s.split("/")
        return date(int(y), int(m), int(d))

    open_ids, with_xy = set(), {}
    with open(path, encoding="latin-1", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            start = row["data_inizio_validita"]
            end = row["data_fine_validita"]
            if start in ("", "-") or day(start) > SNAPSHOT_DAY:
                continue
            if end not in ("", "-") and day(end) < SNAPSHOT_DAY:
                continue
            open_ids.add(row["cod_farmacia"])
            lat, lon = row["latitudine"], row["longitudine"]
            if lat not in ("", "-") and lon not in ("", "-"):
                with_xy[row["cod_farmacia"]] = (float(lat.replace(",", ".")), float(lon.replace(",", ".")))
    return len(open_ids), list(with_xy.values())


def km(a, b):
    """Great-circle distance in km."""
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


class Grid:
    """Bucket points in 0.02° cells so each store checks only nearby cells."""
    SIZE = 0.02  # larger than 1 km in both directions everywhere in Italy

    def __init__(self, pts):
        self.cells = defaultdict(list)
        for p in pts:
            self.cells[(int(p[0] // self.SIZE), int(p[1] // self.SIZE))].append(p)

    def count(self, at):
        ci, cj = int(at[0] // self.SIZE), int(at[1] // self.SIZE)
        return sum(1 for di in (-1, 0, 1) for dj in (-1, 0, 1)
                   for p in self.cells.get((ci + di, cj + dj), ()) if km(at, p) <= RADIUS_KM)


def main(pbf, register):
    with open(STORES, encoding="utf-8", newline="") as f:
        stores = [(r["store_id"], float(r["Latitude"]), float(r["Longitude"])) for r in csv.DictReader(f)]
    assert len(stores) == 480 and len({s[0] for s in stores}) == 480, "expected 480 unique stores"

    points = read_osm(pbf)
    grids = {t: Grid(points[t]) for t in TYPES}
    reg_open, reg_xy = read_register(register)
    reg_grid = Grid(reg_xy)

    rows = []
    for sid, lat, lon in sorted(stores, key=lambda s: int(s[0])):
        counts = {t: grids[t].count((lat, lon)) for t in TYPES}
        rows.append({"store_id": sid, "osm_snapshot_date": SNAPSHOT, "radius_km": RADIUS_KM,
                     **{f"osm_{t}_1km": counts[t] for t in TYPES},
                     "_band": band(lat), "_reg_pharm": reg_grid.count((lat, lon))})

    cols = ["store_id", "osm_snapshot_date", "radius_km"] + [f"osm_{t}_1km" for t in TYPES]
    with open(OUT_DIR / f"osm-counts-{SNAPSHOT}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    cov = []
    for name in ("North", "Centre", "South", "Italy"):
        sub = [r for r in rows if name == "Italy" or r["_band"] == name]
        osm_ph = sum(r["osm_pharmacies_1km"] for r in sub)
        reg_ph = sum(r["_reg_pharm"] for r in sub)
        band_osm = sum(1 for p in points["pharmacies"] if name == "Italy" or band(p[0]) == name)
        band_reg = sum(1 for p in reg_xy if name == "Italy" or band(p[0]) == name)
        row = {"region": name, "stores": len(sub)}
        for t in TYPES:
            vals = [r[f"osm_{t}_1km"] for r in sub]
            row[f"{t}_mean_1km"] = round(sum(vals) / len(vals), 2)
            row[f"{t}_share_zero"] = round(sum(v == 0 for v in vals) / len(vals), 3)
        ratio = osm_ph / reg_ph if reg_ph else None
        row.update({
            "pharmacies_osm_near_stores": osm_ph,
            "pharmacies_register_near_stores": reg_ph,
            "pharmacy_completeness_near_stores": round(ratio, 3) if ratio is not None else "",
            "pharmacies_osm_whole_region": band_osm,
            "pharmacies_register_whole_region": band_reg,
            "pharmacy_completeness_whole_region": round(band_osm / band_reg, 3) if band_reg else "",
            "too_thin": "" if ratio is None else ("yes" if ratio < THIN_RATIO else "no"),
        })
        cov.append(row)
    with open(OUT_DIR / f"osm-coverage-{SNAPSHOT}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cov[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(cov)

    print({t: len(points[t]) for t in TYPES})
    print(f"register: {reg_open} pharmacies open on {SNAPSHOT}, {len(reg_xy)} with coordinates")


if __name__ == "__main__":
    main(*sys.argv[1:3])
