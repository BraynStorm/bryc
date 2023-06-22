include(CTest)
enable_testing()

function(bryc_test target ...)
    add_executable(${ARGV})
    bryc(${target})
    add_test(${target} ${target})
endfunction()

bryc_test(t0 t0.c)
bryc_test(t1 t1.c)
bryc_test(t2 t2-main.c)
bryc_test(t3 t3-vec.c)
