// Body of the single-row native Java Snippet; the input is bounded release evidence.
java.util.Set<String> stores = new java.util.HashSet<>(), links = new java.util.HashSet<>(),
    history = new java.util.HashSet<>(), scores = new java.util.HashSet<>(), raw = new java.util.HashSet<>();
java.util.Map<String,String> folds = new java.util.HashMap<>(), sources = new java.util.HashMap<>();
java.util.Set<String> oof = new java.util.HashSet<>();
java.util.Map<String,String[]> national = new java.util.HashMap<>(), activation = new java.util.HashMap<>(),
    sensitivity = new java.util.HashMap<>(), finance = new java.util.HashMap<>();
int successes = 0;
for (String row : $Concatenate(evidence)$.split("\\|", -1)) {
    String[] v = row.split(":", -1);
    String id = v[1];
    boolean ok = !id.equals("null") && !id.isEmpty();
    switch (v[0]) {
        case "start": break;
        case "store": ok &= stores.add(id); break;
        case "raw": ok &= raw.add(id); break;
        case "national": ok &= national.put(id,v) == null; break;
        case "activation": ok &= activation.put(id,v) == null; break;
        case "sensitivity": ok &= sensitivity.put(id+":"+v[6],v) == null; break;
        case "finance": ok &= finance.put(id,v) == null; break;
        case "link": if ("1".equals(v[3])) successes++;
            ok &= links.add(id) && history.add(v[2]) &&
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
// Reconstruct from national probabilities and observed outcomes, not from the
// forecast or scenario formulas being checked. Money comparisons allow only
// floating-point summation noise, well below one cent.
class Compare {
    boolean number(String s, double expected) {
        return !"null".equals(s) && Math.abs(Double.parseDouble(s)-expected) < 0.000001;
    }
    boolean delta(String s, boolean used, double expected) {
        return used ? number(s,expected) : "null".equals(s);
    }
}
Compare cmp = new Compare();
if (!national.keySet().equals(stores) || sensitivity.size()!=3*stores.size())
    throw new Abort("Release guard: final national/sensitivity coverage");
java.util.TreeMap<Double,java.util.TreeSet<String>> rank = new java.util.TreeMap<>();
java.util.Set<String> funded = new java.util.HashSet<>();
for (String id : stores) {
    String[] n = national.get(id);
    double p = Double.parseDouble(n[2]);
    double net = 2500*p-1500;
    boolean eligible = p>0.60;
    if (!(p>=0 && p<=1) || !sources.get(id).equals(n[3]) || !cmp.number(n[4],net) || !cmp.number(n[5],eligible?1:0))
        throw new Abort("Release guard: final national decision "+id);
    if (!rank.containsKey(p)) rank.put(p,new java.util.TreeSet<String>());
    rank.get(p).add(id);
    if (eligible) {
        funded.add(id);
        String[] a = activation.get(id);
        if (a==null || !java.util.Arrays.equals(java.util.Arrays.copyOfRange(a,1,a.length),java.util.Arrays.copyOfRange(n,1,n.length)))
            throw new Abort("Release guard: activation mismatch "+id);
    }
    for (String scenario : new String[]{"lower","base","upper"}) {
        String[] s = sensitivity.get(id+":"+scenario);
        java.math.BigDecimal adj = new java.math.BigDecimal(n[2]);
        if (p>=0.55 && p<=0.65) adj=adj.add(new java.math.BigDecimal(
            scenario.equals("lower")?"-0.05":scenario.equals("upper")?"0.05":"0"));
        boolean after = adj.compareTo(new java.math.BigDecimal("0.60"))>0;
        String change = after ? (eligible?"retained":"added") : (eligible?"dropped":"not_selected");
        if (s==null || !n[2].equals(s[2]) || !n[3].equals(s[3]) || !cmp.number(s[4],net)
            || !cmp.number(s[5],eligible?1:0) || adj.compareTo(new java.math.BigDecimal(s[7]))!=0
            || !cmp.number(s[8],adj.doubleValue()*2500-1500) || !cmp.number(s[9],after?1:0) || !change.equals(s[10]))
            throw new Abort("Release guard: sensitivity mismatch "+id+" "+scenario);
    }
}
if (!funded.equals(activation.keySet())) throw new Abort("Release guard: activation membership");
int k = Math.min(funded.size(),history.size());
boolean matched = funded.size()<history.size() || funded.size()-history.size()>=17;
java.util.Map<String,double[]> policies = new java.util.HashMap<>();
String[] names={"optimized_forecast","repeat_forecast","matched_optimized","matched_repeat"};
for(int i=0;i<(matched?4:2);i++) {
    double sales=0; int count=0;
    for(double p : rank.descendingKeySet()) for(String id : rank.get(p)) {
        if ((i%2==0?funded:history).contains(id) && (i<2 || count<k)) {count++; sales+=2500*p;}
    }
    policies.put(names[i],new double[]{count,sales,1500.*count,sales-1500.*count});
}
double actualSales=2500.*successes, actualSpend=1500.*history.size();
policies.put("actual_2026",new double[]{history.size(),actualSales,actualSpend,actualSales-actualSpend});
if (!finance.keySet().equals(policies.keySet())) throw new Abort("Release guard: finance policy coverage");
for(String name : policies.keySet()) {
    String[] f=finance.get(name); double[] e=policies.get(name);
    for(int i=0;i<4;i++) if(!cmp.number(f[2+i],e[i])) throw new Abort("Release guard: finance mismatch "+name);
    boolean opt=name.equals(names[0]), same=name.equals(names[2]) && k>0;
    if (!cmp.delta(f[6],opt,e[3]-policies.get("actual_2026")[3]) ||
        !cmp.delta(f[7],opt,e[3]-policies.get(names[1])[3]) ||
        !cmp.delta(f[8],same,same?e[3]-policies.get(names[3])[3]:0))
        throw new Abort("Release guard: finance difference "+name);
}
return "Release checks passed";
