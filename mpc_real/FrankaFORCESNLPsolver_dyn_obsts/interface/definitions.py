import numpy
import ctypes

name = "FrankaFORCESNLPsolver_dyn_obsts"
requires_callback = True
lib = "lib/libFrankaFORCESNLPsolver_dyn_obsts.so"
lib_static = "lib/libFrankaFORCESNLPsolver_dyn_obsts.a"
c_header = "include/FrankaFORCESNLPsolver_dyn_obsts.h"
nstages = 10

# Parameter             | Type    | Scalar type      | Ctypes type    | Numpy type   | Shape     | Len
params = \
[("x0"                  , "dense" , ""               , ctypes.c_double, numpy.float64, ( 70,   1),   70),
 ("xinit"               , "dense" , ""               , ctypes.c_double, numpy.float64, (  3,   1),    3),
 ("all_parameters"      , "dense" , ""               , ctypes.c_double, numpy.float64, (180,   1),  180)]

# Output                | Type    | Scalar type      | Ctypes type    | Numpy type   | Shape     | Len
outputs = \
[("x01"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x02"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x03"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x04"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x05"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x06"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x07"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x08"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x09"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7),
 ("x10"                 , ""      , ""               , ctypes.c_double, numpy.float64,     (  7,),    7)]

# Info Struct Fields
info = \
[('it', ctypes.c_int),
 ('it2opt', ctypes.c_int),
 ('res_eq', ctypes.c_double),
 ('res_ineq', ctypes.c_double),
 ('rsnorm', ctypes.c_double),
 ('rcompnorm', ctypes.c_double),
 ('pobj', ctypes.c_double),
 ('dobj', ctypes.c_double),
 ('dgap', ctypes.c_double),
 ('rdgap', ctypes.c_double),
 ('mu', ctypes.c_double),
 ('mu_aff', ctypes.c_double),
 ('sigma', ctypes.c_double),
 ('lsit_aff', ctypes.c_int),
 ('lsit_cc', ctypes.c_int),
 ('step_aff', ctypes.c_double),
 ('step_cc', ctypes.c_double),
 ('solvetime', ctypes.c_double),
 ('fevalstime', ctypes.c_double),
 ('solver_id', ctypes.c_int * 8)
]

# Dynamics dimensions
#   nvar    |   neq   |   dimh    |   dimp    |   diml    |   dimu    |   dimhl   |   dimhu    
dynamics_dims = [
	(7, 3, 2, 18, 4, 3, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 3, 2, 18, 5, 4, 2, 0), 
	(7, 0, 2, 18, 5, 4, 2, 0)
]