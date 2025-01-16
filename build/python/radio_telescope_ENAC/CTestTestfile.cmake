# CMake generated Testfile for 
# Source directory: /home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC
# Build directory: /home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(qa_PFB "/usr/bin/sh" "qa_PFB_test.sh")
set_tests_properties(qa_PFB PROPERTIES  _BACKTRACE_TRIPLES "/usr/lib/x86_64-linux-gnu/cmake/gnuradio/GrTest.cmake;116;add_test;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;45;GR_ADD_TEST;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;0;")
add_test(qa_Calibration "/usr/bin/sh" "qa_Calibration_test.sh")
set_tests_properties(qa_Calibration PROPERTIES  _BACKTRACE_TRIPLES "/usr/lib/x86_64-linux-gnu/cmake/gnuradio/GrTest.cmake;116;add_test;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;46;GR_ADD_TEST;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;0;")
add_test(qa_Integration "/usr/bin/sh" "qa_Integration_test.sh")
set_tests_properties(qa_Integration PROPERTIES  _BACKTRACE_TRIPLES "/usr/lib/x86_64-linux-gnu/cmake/gnuradio/GrTest.cmake;116;add_test;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;47;GR_ADD_TEST;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;0;")
add_test(qa_Save "/usr/bin/sh" "qa_Save_test.sh")
set_tests_properties(qa_Save PROPERTIES  _BACKTRACE_TRIPLES "/usr/lib/x86_64-linux-gnu/cmake/gnuradio/GrTest.cmake;116;add_test;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;48;GR_ADD_TEST;/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/CMakeLists.txt;0;")
subdirs("bindings")
