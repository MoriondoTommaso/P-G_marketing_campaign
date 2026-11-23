// Body of the single-row native Java Snippet; the input is bounded release evidence.
java.util.Set<String> stores = new java.util.HashSet<>(), links = new java.util.HashSet<>(),
    history = new java.util.HashSet<>(), scores = new java.util.HashSet<>(), raw = new java.util.HashSet<>();
java.util.Map<String,String> folds = new java.util.HashMap<>(), sources = new java.util.HashMap<>();
java.util.Set<String> oof = new java.util.HashSet<>();
for (String row : $Concatenate(evidence)$.split("\\|", -1)) {
    String[] v = row.split(":", -1);
    String id = v[1];
    boolean ok = !id.equals("null") && !id.isEmpty();
    switch (v[0]) {
        case "start": break;
        case "store": ok &= stores.add(id); break;
        case "raw": ok &= raw.add(id); break;
        case "link": ok &= links.add(id) && history.add(v[2]) &&
            !v[2].equals("null") && (v[3].equals("0") || v[3].equals("1")); break;
        case "conflict": ok = false; break;
        case "fold": ok &= folds.put(id, v[2]) == null && v[2].matches("[1-5]"); break;
        case "oof": ok &= oof.add(id+":"+v[2]+":"+v[3]) && v[4].equals("true"); break;
        case "score": ok &= scores.add(id) && sources.put(id, v[2]) == null && v[3].equals("true"); break;
        default: ok = false;
    }
    if (!ok) throw new Abort("Release guard: invalid or repeated " + row);
}
if (stores.size() != 480 || history.size() != 170 || raw.size() != 170 ||
    !raw.equals(links) || !history.equals(folds.keySet()) || !stores.containsAll(history) ||
    !scores.equals(stores) || oof.size() != 510)
    throw new Abort("Release guard: population, activation links, folds, OOF or national scores incomplete");
for (String id : stores) {
    boolean h = history.contains(id);
    if (!(h ? "held_out_2026" : "refit_unseen").equals(sources.get(id)))
        throw new Abort("Release guard: wrong score source for " + id);
    if (h) for (String model : new String[]{"baseline", "logistic", "tree"})
        if (!oof.contains(id+":"+folds.get(id)+":"+model))
            throw new Abort("Release guard: missing or wrong-fold OOF for " + id + "/" + model);
}
return "Release checks passed";
