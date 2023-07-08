static int a;

/* bryc: start
from pathlib import Path

csv = (Path("t0.csv")).read_text(encoding='utf-8')
lines = csv.split('\n')
cols = lines[0].count(',')+1
fmt_csv = '\n'.join(map(lambda l: f"    {{{l}}},",lines))
bryc().emit(f"static int x [{len(lines)}][{cols}] = {{\n{fmt_csv}\n}};")
bryc().emit(f"#define X_ROWS {len(lines)}")
bryc().emit(f"#define X_COLS {cols}")
*/
static int x [2][3] = {
    {0, 1, -2},
    {-1, 0, 2},
};
#define X_ROWS 2
#define X_COLS 3
/* bryc: end */

static int b;

int main() { 
  int sum = 0;
  for (int i = 0; i < X_ROWS; ++i) {
    for (int j = 0; j < X_COLS; ++j) {
      sum += x[i][j];
    }
  }
  return a + b + sum;
}
