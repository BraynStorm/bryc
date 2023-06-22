# bryc  [brik]

_BraynStorm's C-family code generator._


`bryc` allows you to write arbitrary python3 pre-processor code in C or C++ files.

Every pair of `/* bryc: start` and `/* bryc: end */` signifies a python code
block and the python part of the code is inside the `# bryc: start` comment.

The code between `/* bryc: start ... */` and `/* bryc: end */` will be populated
by all `bryc.emit(...)` calls, each on a separate line .

## Usage
```c
// inside my random C file

/* bryc: start
# -------------- Python3 goes here -----------------
*/
/* bryc: end */
```

To actually generate code


## Example

```c
#include <stdio.h>

char const* now = 
/* bryc: start
from datetime import datetime
bryc.emit(f'"Compilation timestamp: {datetime.now()}"')
*/
/* bryc: end */
;

int main(){
    puts(now);
    return 0;
}
```

After precompiling with bryc (`py bryc.py main.c`)

The file becomes:

```c
#include <stdio.h>

char const* now = 
/* bryc: start
from datetime import datetime
bryc.emit(f'"Compilation timestamp: {datetime.now()}"')
*/
"Compilation timestamp: 2023-06-22 15:25:20.932956"
/* bryc: end */
;

int main(){
    puts(now);
    return 0;
}
```

## Pre-requisites

`bryc` uses only standard Python 3.11 code, without any external dependencies.

## Security

_0/10 would not recomen[d]_

**DO NOT PREPROCESS ANY UNTRUSTED CODE!!!**

`bryc` allows you to execute arbitrary python3 code during the build process.
You should know exactly how dangerous this is.


## Getting started

curl -






