#=============================================================================
# CMake configuration file for the Chrono Robosimian module
# 
# Cannot be used stand-alone (it's loaded by CMake config. file in parent dir.)
#=============================================================================

option(ENABLE_MODULE_ROBOSIMIAN "Enable the Chrono Robosimian module" OFF)

# Return now if this module is not enabled
IF(NOT ENABLE_MODULE_ROBOSIMIAN)
	RETURN()
ENDIF()

MESSAGE(STATUS "==== Chrono Robosimian module ====")

#-----------------------------------------------------------------------------
# LIST THE FILES THAT MAKE THE ROBOSIMIAN LIBRARY

SET(ChronoEngine_ROBOSIMIAN_SOURCES 
    robosimian.cpp
)

SET(ChronoEngine_ROBOSIMIAN_HEADERS
    ChApiRoboSimian.h
	robosimian.h 
	driver_cb.h
)

SOURCE_GROUP("" FILES 
            ${ChronoEngine_ROBOSIMIAN_SOURCES} 
            ${ChronoEngine_ROBOSIMIAN_HEADERS})

#-----------------------------------------------------------------------------	
# In most cases, you do not need to edit the lines below.

# The ROBOSIMIAN library is added to the project,
# and some custom properties of this target are set.

ADD_LIBRARY(ChronoEngine_robosimian SHARED 
			${ChronoEngine_ROBOSIMIAN_SOURCES}
			${ChronoEngine_ROBOSIMIAN_HEADERS})

SET_TARGET_PROPERTIES(ChronoEngine_robosimian PROPERTIES
                      COMPILE_FLAGS "${CH_CXX_FLAGS}"
                      LINK_FLAGS "${CH_LINKERFLAG_SHARED}"
					  COMPILE_DEFINITIONS "CH_API_COMPILE_ROBOSIMIAN")
                          
TARGET_LINK_LIBRARIES(ChronoEngine_robosimian 
	                  ChronoEngine)
	
ADD_DEPENDENCIES(ChronoEngine_robosimian ChronoEngine)
	
INSTALL(TARGETS ChronoEngine_robosimian
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)		

INSTALL(FILES ${ChronoEngine_robosimian_HEADERS}
        DESTINATION include/chrono_robosimian)


