"""This cython file wraps the following two functions
PRNearNeighborStructT initSelfTunedRNearNeighborWithDataSet(
    RealT thresholdR,
    RealT successProbability,
    Int32T nPoints,
    IntT dimension,
    PPointT *dataSet,
    IntT nSampleQueries,
    PPointT *sampleQueries)
Int32T getRNearNeighbors(PRNearNeighborStructT nnStruct,
                         PPointT queryPoint,
                         PPointT *(&result), IntT &resultSize)
To do that I need to cdef/ctypedef the following functions and types
IntT                   | #define intT int    | BasicDefinitions
Int32T                 | #define int32T int  | BasicDefinitions
RealT                  | #define RealT float | BasicDefinitions
PPointT                | typedef struct _PointT *PPointT | Geometry
PRNearNeighborStructT  | tydef struct RNe. *P..| LocalitySensitiveHashing
initSelfTunedRNearNeighborWithDataSet |      | NearNeighbors
getRNearNeighbors      |                     | NearNeighbors
"""
__author__="pushpendre"

cdef extern from "../sources/BasicDefinitions.h":
    ctypedef int IntT
    ctypedef int Int32T
    ctypedef float RealT
    ctypedef long long int MemVarT

cdef extern from "../sources/Geometry.h":
    struct _PointT:
        IntT index
        RealT* coordinates
        RealT sqrLength
    ctypedef _PointT PointT
    ctypedef PointT* PPointT
    
cdef extern from "../sources/LocalitySensitiveHashing.h":
    ctypedef struct RNearNeighborStructT:
        pass
    ctypedef RNearNeighborStructT* PRNearNeighborStructT

cdef extern from "../sources/NearNeighbors.h":
    PRNearNeighborStructT initSelfTunedRNearNeighborWithDataSet(
        RealT thresholdR,
        RealT successProbability,
        Int32T nPoints,
        IntT dimension,
        PPointT *dataSet,
        IntT nSampleQueries,
        PPointT *sampleQueries,
        MemVarT memoryUpperBound
        )
    
    Int32T getRNearNeighbors(
        PRNearNeighborStructT nnStruct,
        PPointT queryPoint,
        PPointT* (&result),
        Int32T &resultSize
        )


    
