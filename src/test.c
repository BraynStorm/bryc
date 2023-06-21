static int a() { return 0; }

/* bryc: start */
/*
csv = (Path("dump") / "csv").read_text(encoding='utf-8')
lines = csv.split('\n')
cols = lines[0].count(',')+1
fmt_csv = '\n'.join(map(lambda l: f"    {{{l}}},",lines))
bryc.emit(f"static int x [{len(lines)}][{cols}] = {{\n{fmt_csv}\n}};")
*/
static int x [2][2] = {
    {0,1},
    {2,23},
};
/* bryc: end */

static int b() { return 0; }

int main(){
    return x[0][0];
}
