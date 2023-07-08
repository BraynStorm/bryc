include(CTest)
enable_testing()

function(bryc_test target ...)
    add_executable(${ARGV})
    bryc(${target})
    add_test(${target} ${target})
endfunction()

bryc_test(t0 t0.c t0.csv)
bryc_test(t1 t1.c t1.py)
bryc_test(t2 t2-main.c t2.h)
bryc_test(t3 t3-vec.c t3.py)
