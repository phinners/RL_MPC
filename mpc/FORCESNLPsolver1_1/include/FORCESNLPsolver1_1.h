/*
FORCESNLPsolver1_1 : A fast customized optimization solver.

Copyright (C) 2013-2023 EMBOTECH AG [info@embotech.com]. All rights reserved.


This software is intended for simulation and testing purposes only. 
Use of this software for any commercial purpose is prohibited.

This program is distributed in the hope that it will be useful.
EMBOTECH makes NO WARRANTIES with respect to the use of the software 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. 

EMBOTECH shall not have any liability for any damage arising from the use
of the software.

This Agreement shall exclusively be governed by and interpreted in 
accordance with the laws of Switzerland, excluding its principles
of conflict of laws. The Courts of Zurich-City shall have exclusive 
jurisdiction in case of any dispute.

*/

/* Generated by FORCESPRO v6.2.0 on Thursday, August 3, 2023 at 10:44:49 AM */
#ifndef FORCESNLPsolver1_1_H
#define FORCESNLPsolver1_1_H

#ifndef SOLVER_STDIO_H
#define SOLVER_STDIO_H
#include <stdio.h>
#endif
#ifndef SOLVER_STRING_H
#define SOLVER_STRING_H
#include <string.h>
#endif


#ifndef SOLVER_STANDARD_TYPES
#define SOLVER_STANDARD_TYPES

typedef signed char solver_int8_signed;
typedef unsigned char solver_int8_unsigned;
typedef char solver_int8_default;
typedef signed short int solver_int16_signed;
typedef unsigned short int solver_int16_unsigned;
typedef short int solver_int16_default;
typedef signed int solver_int32_signed;
typedef unsigned int solver_int32_unsigned;
typedef int solver_int32_default;
typedef signed long long int solver_int64_signed;
typedef unsigned long long int solver_int64_unsigned;
typedef long long int solver_int64_default;

#endif


/* DATA TYPE ------------------------------------------------------------*/
typedef double FORCESNLPsolver1_1_float;
typedef double FORCESNLPsolver1_1_ldl_s_float;
typedef double FORCESNLPsolver1_1_ldl_r_float;
typedef double FORCESNLPsolver1_1_callback_float;

typedef double FORCESNLPsolver1_1interface_float;

/* SOLVER SETTINGS ------------------------------------------------------*/

/* MISRA-C compliance */
#ifndef MISRA_C_FORCESNLPsolver1_1
#define MISRA_C_FORCESNLPsolver1_1 (0)
#endif

/* restrict code */
#ifndef RESTRICT_CODE_FORCESNLPsolver1_1
#define RESTRICT_CODE_FORCESNLPsolver1_1 (0)
#endif

/* print level */
#ifndef SET_PRINTLEVEL_FORCESNLPsolver1_1
#define SET_PRINTLEVEL_FORCESNLPsolver1_1    (0)
#endif

/* timing */
#ifndef SET_TIMING_FORCESNLPsolver1_1
#define SET_TIMING_FORCESNLPsolver1_1    (1)
#endif

/* Numeric Warnings */
/* #define PRINTNUMERICALWARNINGS */

/* maximum number of iterations  */
#define SET_MAXIT_FORCESNLPsolver1_1			(200)	

/* scaling factor of line search (FTB rule) */
#define SET_FLS_SCALE_FORCESNLPsolver1_1		(FORCESNLPsolver1_1_float)(0.99)      

/* maximum number of supported elements in the filter */
#define MAX_FILTER_SIZE_FORCESNLPsolver1_1	(200) 

/* whether callback return values should be checked */
#define EXTFUNC_RETURN_FORCESNLPsolver1_1 (0)

/* SOLVER RETURN CODES----------------------------------------------------------*/
/* solver has converged within desired accuracy */
#define OPTIMAL_FORCESNLPsolver1_1      (1)

/* maximum number of iterations has been reached */
#define MAXITREACHED_FORCESNLPsolver1_1 (0)

/* solver has stopped due to a timeout */
#define TIMEOUT_FORCESNLPsolver1_1   (2)

/* solver stopped externally */
#define EXIT_EXTERNAL_FORCESNLPsolver1_1 (3)

/* wrong number of inequalities error */
#define INVALID_NUM_INEQ_ERROR_FORCESNLPsolver1_1  (-4)

/* factorization error */
#define FACTORIZATION_ERROR_FORCESNLPsolver1_1   (-5)

/* NaN encountered in function evaluations */
#define BADFUNCEVAL_FORCESNLPsolver1_1  (-6)

/* invalid value (<= -100) returned by external function */
#define INVALIDFUNCEXIT_FORCESNLPsolver1_1 (-200)

/* bad value returned by external function */
#define BADFUNCEXIT_FORCESNLPsolver1_1(status) (status > -100? status - 200 : INVALIDFUNCEXIT_FORCESNLPsolver1_1)

/* no progress in method possible */
#define NOPROGRESS_FORCESNLPsolver1_1   (-7)

/* regularization error */
#define REGULARIZATION_ERROR_FORCESNLPsolver1_1   (-9)

/* invalid values in parameters */
#define PARAM_VALUE_ERROR_FORCESNLPsolver1_1   (-11)

/* too small timeout given */
#define INVALID_TIMEOUT_FORCESNLPsolver1_1   (-12)

/* thread error */
#define THREAD_FAILURE_FORCESNLPsolver1_1  (-98)

/* locking mechanism error */
#define LOCK_FAILURE_FORCESNLPsolver1_1  (-99)

/* licensing error - solver not valid on this machine */
#define LICENSE_ERROR_FORCESNLPsolver1_1  (-100)

/* Insufficient number of internal memory instances.
 * Increase codeoptions.max_num_mem. */
#define MEMORY_INVALID_FORCESNLPsolver1_1 (-101)
/* Number of threads larger than specified.
 * Increase codeoptions.nlp.max_num_threads. */
#define NUMTHREADS_INVALID_FORCESNLPsolver1_1 (-102)


/* INTEGRATORS RETURN CODE ------------*/
/* Integrator ran successfully */
#define INTEGRATOR_SUCCESS (11)
/* Number of steps set by user exceeds maximum number of steps allowed */
#define INTEGRATOR_MAXSTEPS_EXCEEDED (12)


/* MEMORY STRUCT --------------------------------------------------------*/
typedef struct FORCESNLPsolver1_1_mem FORCESNLPsolver1_1_mem;
#ifdef __cplusplus
extern "C" {
#endif
/* MEMORY STRUCT --------------------------------------------------------*/
extern FORCESNLPsolver1_1_mem * FORCESNLPsolver1_1_external_mem(void * mem_ptr, solver_int32_unsigned i_mem, size_t mem_size);
extern size_t FORCESNLPsolver1_1_get_mem_size( void );
extern size_t FORCESNLPsolver1_1_get_const_size( void );
#ifdef __cplusplus
}
#endif

/* PARAMETERS -----------------------------------------------------------*/
/* fill this with data before calling the solver! */
typedef struct
{
    /* vector of size 6 */
    FORCESNLPsolver1_1_float xinit[6];

    /* vector of size 80 */
    FORCESNLPsolver1_1_float x0[80];

    /* vector of size 144 */
    FORCESNLPsolver1_1_float all_parameters[144];


} FORCESNLPsolver1_1_params;


/* OUTPUTS --------------------------------------------------------------*/
/* the desired variables are put here by the solver */
typedef struct
{
    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x1[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x2[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x3[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x4[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x5[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x6[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x7[10];

    /* column vector of length 10 */
    FORCESNLPsolver1_1_float x8[10];


} FORCESNLPsolver1_1_output;


/* SOLVER INFO ----------------------------------------------------------*/
/* diagnostic data from last interior point step */
typedef struct
{
    /* scalar: iteration number */
    solver_int32_default it;

    /* scalar: number of iterations needed to optimality (branch-and-bound) */
    solver_int32_default it2opt;

    /* scalar: inf-norm of equality constraint residuals */
    FORCESNLPsolver1_1_float res_eq;

    /* scalar: inf-norm of inequality constraint residuals */
    FORCESNLPsolver1_1_float res_ineq;

    /* scalar: norm of stationarity condition */
    FORCESNLPsolver1_1_float rsnorm;

    /* scalar: max of all complementarity violations */
    FORCESNLPsolver1_1_float rcompnorm;

    /* scalar: primal objective */
    FORCESNLPsolver1_1_float pobj;

    /* scalar: dual objective */
    FORCESNLPsolver1_1_float dobj;

    /* scalar: duality gap := pobj - dobj */
    FORCESNLPsolver1_1_float dgap;

    /* scalar: relative duality gap := |dgap / pobj | */
    FORCESNLPsolver1_1_float rdgap;

    /* scalar: duality measure */
    FORCESNLPsolver1_1_float mu;

    /* scalar: duality measure (after affine step) */
    FORCESNLPsolver1_1_float mu_aff;

    /* scalar: centering parameter */
    FORCESNLPsolver1_1_float sigma;

    /* scalar: number of backtracking line search steps (affine direction) */
    solver_int32_default lsit_aff;

    /* scalar: number of backtracking line search steps (combined direction) */
    solver_int32_default lsit_cc;

    /* scalar: step size (affine direction) */
    FORCESNLPsolver1_1_float step_aff;

    /* scalar: step size (combined direction) */
    FORCESNLPsolver1_1_float step_cc;

    /* scalar: total solve time */
    FORCESNLPsolver1_1_float solvetime;

    /* scalar: time spent in function evaluations */
    FORCESNLPsolver1_1_float fevalstime;

    /* column vector of length 8: solver ID of FORCESPRO solver */
    solver_int32_default solver_id[8];




} FORCESNLPsolver1_1_info;







/* SOLVER FUNCTION DEFINITION -------------------------------------------*/
/* Time of Solver Generation: (UTC) Thursday, August 3, 2023 10:44:50 AM */
/* User License expires on: (UTC) Monday, January 29, 2024 10:00:00 PM (approx.) (at the time of code generation) */
/* Solver Static License expires on: (UTC) Monday, January 29, 2024 10:00:00 PM (approx.) */
/* Solver Id: 865922cd-97f9-4bbe-b573-c6018ae936b4 */
/* Host Compiler Version: d76500f0 */
/* Target Compiler Version: unused */
/* examine exitflag before using the result! */
#ifdef __cplusplus
extern "C" {
#endif		

typedef solver_int32_default (*FORCESNLPsolver1_1_extfunc)(FORCESNLPsolver1_1_float* x, FORCESNLPsolver1_1_float* y, FORCESNLPsolver1_1_float* lambda, FORCESNLPsolver1_1_float* params, FORCESNLPsolver1_1_float* pobj, FORCESNLPsolver1_1_float* g, FORCESNLPsolver1_1_float* c, FORCESNLPsolver1_1_float* Jeq, FORCESNLPsolver1_1_float* h, FORCESNLPsolver1_1_float* Jineq, FORCESNLPsolver1_1_float* H, solver_int32_default stage, solver_int32_default iterations, solver_int32_default threadID);

extern solver_int32_default FORCESNLPsolver1_1_solve(FORCESNLPsolver1_1_params *params, FORCESNLPsolver1_1_output *output, FORCESNLPsolver1_1_info *info, FORCESNLPsolver1_1_mem *mem, FILE *fs, FORCESNLPsolver1_1_extfunc evalextfunctions_FORCESNLPsolver1_1);



/*Integrator declarations */
typedef const solver_int32_default* (*cDynJacXsparsity)( solver_int32_default i );
typedef const solver_int32_default* (*cDynJacUsparsity)( solver_int32_default i );
typedef solver_int32_default (*fConDynamics)( const FORCESNLPsolver1_1_callback_float** arg, FORCESNLPsolver1_1_callback_float** res, solver_int32_default* iw, FORCESNLPsolver1_1_callback_float* w, solver_int32_default mem );
typedef solver_int32_default (*fConJacStateDynamics)( const FORCESNLPsolver1_1_callback_float** arg, FORCESNLPsolver1_1_callback_float** res, solver_int32_default* iw, FORCESNLPsolver1_1_callback_float* w, solver_int32_default mem );
typedef solver_int32_default (*fConJacInputDynamics)( const FORCESNLPsolver1_1_callback_float** arg, FORCESNLPsolver1_1_callback_float** res, solver_int32_default* iw, FORCESNLPsolver1_1_callback_float* w, solver_int32_default mem );

void FORCESNLPsolver1_1_rkfour_0(const FORCESNLPsolver1_1_callback_float * const z, const FORCESNLPsolver1_1_callback_float * const p, FORCESNLPsolver1_1_float * const c, FORCESNLPsolver1_1_float * const jacc,
            fConDynamics cDyn0rd, fConDynamics cDyn, const solver_int32_default threadID);









#ifdef __cplusplus
}
#endif

#endif
