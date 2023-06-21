set(BRYC ${CMAKE_SOURCE_DIR}/bryc.py)

function(bryc target)
    get_target_property(SOURCES ${target} SOURCES)
    add_custom_target(
        ${target}-bryc
        COMMAND py ${BRYC} ${SOURCES}
        DEPENDS
        ${BRYC}
        ${SOURCES}
        USES_TERMINAL
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    add_dependencies(${target} ${target}-bryc)
endfunction()