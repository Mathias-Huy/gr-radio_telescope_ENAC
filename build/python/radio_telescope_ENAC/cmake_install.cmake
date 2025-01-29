# Install script for directory: /home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.10/dist-packages/gnuradio/radio_telescope_ENAC" TYPE FILE FILES
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/__init__.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/PFB.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/Calibration.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/Integration.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/Save.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/Gaussian_fit.py"
    "/home/mathuy/gr-radio_telescope_ENAC/python/radio_telescope_ENAC/Gausian_Signal.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.10/dist-packages/gnuradio/radio_telescope_ENAC" TYPE FILE FILES
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/__init__.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/PFB.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Calibration.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Integration.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Save.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Gaussian_fit.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Gausian_Signal.pyc"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/__init__.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/PFB.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Calibration.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Integration.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Save.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Gaussian_fit.pyo"
    "/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/Gausian_Signal.pyo"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/mathuy/gr-radio_telescope_ENAC/build/python/radio_telescope_ENAC/bindings/cmake_install.cmake")

endif()

