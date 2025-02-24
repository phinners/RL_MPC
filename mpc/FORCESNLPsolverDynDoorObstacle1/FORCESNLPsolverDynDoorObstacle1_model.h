

#ifndef FORCESNLPSOLVERDYNDOOROBSTACLE1_MODEL_H
#include "include/FORCESNLPsolverDynDoorObstacle1.h"
#define FORCESNLPSOLVERDYNDOOROBSTACLE1_MODEL_H
/* This file was automatically generated by CasADi.
   The CasADi copyright holders make no ownership claim of its contents. */
#ifdef __cplusplus
extern "C" {
#endif

#ifndef casadi_real
#define casadi_real FORCESNLPsolverDynDoorObstacle1_float
#endif

#ifndef casadi_int
#define casadi_int solver_int32_default
#endif

int FORCESNLPsolverDynDoorObstacle1_objective_0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_objective_0_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_objective_0_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int FORCESNLPsolverDynDoorObstacle1_inequalities_0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_inequalities_0_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_inequalities_0_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int FORCESNLPsolverDynDoorObstacle1_cdyn_0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_cdyn_0_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_cdyn_0_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int FORCESNLPsolverDynDoorObstacle1_cdyn_0rd_0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_cdyn_0rd_0_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_cdyn_0rd_0_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int FORCESNLPsolverDynDoorObstacle1_objective_1(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_objective_1_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_objective_1_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int FORCESNLPsolverDynDoorObstacle1_inequalities_1(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
const casadi_int* FORCESNLPsolverDynDoorObstacle1_inequalities_1_sparsity_out(casadi_int i);
int FORCESNLPsolverDynDoorObstacle1_inequalities_1_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#ifdef __cplusplus
} /* extern "C" */
#endif
#endif