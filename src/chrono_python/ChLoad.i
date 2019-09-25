%{

/* Includes the header in the wrapper code */
#include "chrono/physics/ChLoad.h"
#include "chrono/physics/ChLoadsBody.h"
#include "chrono/physics/ChLoadsXYZnode.h"

%}

//TODO: remove ignore once ref is wrapped 
%shared_ptr(chrono::ChLoad)
%shared_ptr(chrono::ChLoadBase)
%shared_ptr(chrono::ChLoadCustom)
%shared_ptr(chrono::ChLoadCustomMultiple)

// Tell SWIG about parent class in Python
%import "ChPhysicsItem.i"
%import "ChObject.i"

/* Parse the header file to generate wrappers */
%ignore chrono::ChLoad::ComputeJacobian;
%ignore chrono::ChLoadBase::ComputeJacobian;
%ignore chrono::ChLoadCustom::ComputeJacobian;
%ignore chrono::ChLoadCustomMultiple::ComputeJacobian;
%include "../chrono/physics/ChLoad.h"





