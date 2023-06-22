# bryc  /brik/

_BraynStorm's C-family in-place code generator._


`bryc` allows you to write arbitrary python3 pre-processor code in C or C++ files.

Every pair of `/* bryc: start` and `/* bryc: end */` signifies a python code
block and the python part of the code is inside the `# bryc: start` comment.

The code between `/* bryc: start ... */` and `/* bryc: end */` will be populated
by all `bryc.emit(...)` calls, each on a separate line .

## Usage
```c
// file.c

/* bryc: start
# -------------- Python3 goes here -----------------
*/
/* bryc: end */
```

Building is as easy as
```sh
#!/bin/bash
python3 bryc.py file.c
gcc file.c
```

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

int main()
{
    puts(now);
    return 0;
}
```

After preprocessing with bryc (`py bryc.py main.c`) the file becomes:

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

int main()
{
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

### CMake

```cmake
# Setup the project
cmake_minimum_required(VERSION 3.16)
project(my_project)

# Define targets
add_executable(
    my_executable
    exec-main.c
    exec-util.c
    exec-util.h
)
add_library(
    my_library
    mylib.c
    mylib.h
)

# Ensures it auto-updates on Configure
file(DOWNLOAD https://raw.githubusercontent.com/BraynStorm/bryc/master/bryc.cmake bryc.cmake)

# Pre-process all targets you want.
include(bryc.cmake)
bryc(my_executable)
bryc(my_library)

```

## Open questions

`bryc` is in it's infancy. There are open questions about using it effectively.

- How do you debug complex code?
  - Launching PDB might be inconvenient, especially if you've written all the important code _inside_ the c/cpp file.
- "I don't wanna use python, I wanna use language X"
- Specifying python dependencies.
  - For example, your codegen needs to use a lot of matrix math and you want to use NumPY.
- Poor IDE support
  - `VSCode` + `clangd` don't support language injections (AFAIK) so the python code in the comment is treated as just a comment - no highlighting.



