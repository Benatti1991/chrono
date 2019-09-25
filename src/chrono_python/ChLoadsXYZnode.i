%{

/* Includes the header in the wrapper code */
#include "chrono/physics/ChLoad.h"
#include "chrono/physics/ChLoadsXYZnode.h"

%}

%shared_ptr(chrono::ChLoadXYZnodeForce)
%shared_ptr(chrono::ChLoadXYZnodeForceAbsolute)
%shared_ptr(chrono::ChLoadXYZnodeXYZnode)
%shared_ptr(chrono::ChLoadXYZnodeXYZnodeSpring)
%shared_ptr(chrono::ChLoadXYZnodeXYZnodeBushing)
%shared_ptr(chrono::ChLoadXYZnodeBody)
%shared_ptr(chrono::ChLoadXYZnodeBodySpring)
%shared_ptr(chrono::ChLoadXYZnodeBodyBushing)

// Tell SWIG about parent class in Python
%import "ChLoad.i"

/* Parse the header file to generate wrappers */

%include "../chrono/physics/ChLoadsXYZnode.h"




