/* bryc: start
from t1 import *

create_variable('foo', 'int', value=10, static=True, const=True)
*/
static int const foo = 10;
/* bryc: end */ 

int main() { return !(foo == 10); }