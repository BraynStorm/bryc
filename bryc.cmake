if("${BRYC}" STREQUAL "")
    message("bryc.cmake: Using default location for bryc.py")
    set(BRYC "${CMAKE_SOURCE_DIR}/bryc.py")
endif()

if("${BRYC_VERSION}" STREQUAL "")
    message("bryc.cmake: Using master version for bryc.py")
    set(BRYC_VERSION "master")
endif()

# NOTE:
# This makes bryc.py be auto-updated
if(NOT("${PROJECT_NAME}" STREQUAL "bryc2"))
    message("bryc.cmake: Downloading bryc.py (${BRYC_VERSION})")
    file(DOWNLOAD https://raw.githubusercontent.com/BraynStorm/bryc/${BRYC_VERSION}/bryc.py "${BRYC}")
endif()

function(bryc target)
    set(flags VERBOSE)
    cmake_parse_arguments(BRYC_F "${flags}" "" "" ${ARGN})

    get_target_property(SOURCES ${target} SOURCES)

    if(BRYC_F_VERBOSE)
        set(extra ${extra} -vvv)
    endif()

    add_custom_target(
        ${target}-bryc
        COMMAND py ${BRYC} ${extra} ${SOURCES}
        DEPENDS
        ${BRYC}
        ${SOURCES}
        USES_TERMINAL
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    add_dependencies(${target} ${target}-bryc)
endfunction()