"""Extend RC2 gate #1029 using the exact data ports feeding its four final writers."""
from pathlib import Path
import sys
from build import Archive, key, value, put, entry


def extend(source, target):
    a = Archive(source)
    a.serial = max(a.path)
    group = a.parent[1029]
    edges = a.edges(group)

    def input_of(i):
        wire, = [c for c in edges if value(c, "destID") == str(i) and value(c, "destPort") == "1"]
        return wire, (int(value(wire, "sourceID")), int(value(wire, "sourcePort")))

    agg_input, collected = input_of(1028)
    store = "store_id p_success score_source expected_net_eur recommend_activate"
    tables = [(339, "national", store), (341, "activation", store),
              (353, "sensitivity", "store_id p_success score_source base_net_eur base_recommend_activate scenario scenario_p_success expected_net_eur recommend_activate change"),
              (556, "finance", "policy store_count sales_eur spend_eur net_eur vs_2026_actual_eur vs_repeat_forecast_eur matched_net_difference_eur")]
    for ix, (writer, tag, fields) in enumerate(tables):
        _, source_port = input_of(writer)
        row = a.clone(41, group, "Read final " + tag + " rows before export", 220, 860 + ix*135)
        m = a.model(row)
        entry(m, "insert_missing_as_null", "true", "xboolean")
        put(m, "replaced_column", "evidence")
        put(m, "expression", f'return "{tag}:" + ' + ' + ":" + '.join(f"${c}$" for c in fields.split()) + ";")
        a.wire(group, source_port, (row, 1))
        # Reuse a release evidence-only column filter (its schema is already configured).
        select = a.clone(1007, group, "Keep " + tag + " evidence", 420, 860 + ix*135)
        a.wire(group, (row, 1), (select, 1))
        merge = a.clone(48, group, "Append " + tag + " evidence", 650+ix*190, 850)
        a.wire(group, collected, (merge, 1))
        a.wire(group, (select, 1), (merge, 2))
        collected = merge, 1
    put(agg_input, "sourceID", collected[0])
    put(agg_input, "sourcePort", collected[1])
    put(a.model(1029), "expression", Path(__file__).with_name("guard.java").read_text())
    put(key(a.edit(1029), "nodeAnnotation"), "text", "Require exact cohorts, activation membership, three scenarios per store and reconciled policy economics before publication.")
    a.save(target)


if __name__ == "__main__":
    extend(*map(Path, sys.argv[1:]))
