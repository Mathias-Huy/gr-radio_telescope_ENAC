# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT radio_telescope_ENAC_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT radio_telescope_ENAC_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND radio_telescope_ENAC_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(radio_telescope_ENAC
   ../../..
   gr::radio_telescope_ENAC
   "${radio_telescope_ENAC_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/radio_telescope_ENAC/
  DEPENDS radio_telescope_ENAC_python)

install(TARGETS radio_telescope_ENAC_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/radio_telescope_ENAC COMPONENT pythonapi)
