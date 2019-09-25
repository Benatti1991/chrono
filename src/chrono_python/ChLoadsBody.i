%{

/* Includes the header in the wrapper code */
#include "chrono/physics/ChLoad.h"
#include "chrono/physics/ChLoadsBody.h"

%}

%shared_ptr(chrono::ChLoadBodyForce)
%shared_ptr(chrono::ChLoadBodyTorque)
%shared_ptr(chrono::ChLoadBodyBody)
%shared_ptr(chrono::ChLoadBodyBodyTorque)
%shared_ptr(chrono::ChLoadBodyBodyBushingSpherical)
%shared_ptr(chrono::ChLoadBodyBodyBushingPlastic)
%shared_ptr(chrono::ChLoadBodyBodyBushingMate)
%shared_ptr(chrono::ChLoadBodyBodyBushingPlastic)
%shared_ptr(chrono::ChLoadBodyBodyBushingGeneric)

// Tell SWIG about parent class in Python
%import "ChLoad.i"

/* Parse the header file to generate wrappers */
%include "../chrono/physics/ChLoadsBody.h"




