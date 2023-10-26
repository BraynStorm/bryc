// clang-format off
/* bryc: start
global G

G = 0
*/
/* bryc: end */
// clang-format on

// clang-format off
/* bryc: start
global G

bryc().emit(f"int x = {G};")
*/
int x = 0;
/* bryc: end */
// clang-format on

int main() { return x; }