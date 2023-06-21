cmake_minimum_required(VERSION 3.20)
project(bryc2)

function(bryc target)
    get_target_property(SOURCES ${target} SOURCES)
    add_custom_target(
        ${target}-bryc
        COMMAND py bryc.py ${SOURCES}
        DEPENDS
        bryc.py
        ${SOURCES}
        USES_TERMINAL
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    )
    add_dependencies(${target} ${target}-bryc)
endfunction()

add_executable(test src/test.c src/bryc-base.h)
bryc(test)