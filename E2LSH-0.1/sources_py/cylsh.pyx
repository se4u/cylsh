#clib library_with_useful_functions
#cython: nonecheck=True
"""This cython file provides a single class, the LSH class, that can be
initialized and then queried.
"""
import time
import cython
cimport lsh
from lsh cimport PRNearNeighborStructT, PointT, PPointT, IntT, Int32T, RealT, initSelfTunedRNearNeighborWithDataSet, getRNearNeighbors
from libc.stdlib cimport calloc, free

cdef RealT* create_coordinates_ptr(list coordinate_vector,
                                   int dimension):
    c = <RealT*>calloc(dimension, sizeof(RealT))
    for j in xrange(dimension):
        c[j]=coordinate_vector[j]
    return c

cdef PPointT* create_dataset_ptr(list dataset,
                                 int len_dataset,
                                 int dimension):
    dataset_ptr=<PPointT*>calloc(len_dataset, sizeof(PPointT))
    for i in xrange(len_dataset):
        p = <PPointT>calloc(1, sizeof(PointT))
        p.index=dataset[i][0]
        p.coordinates=create_coordinates_ptr(dataset[i][1],
                                             dimension)
        p.sqrLength=dataset[i][2]
        dataset_ptr[i]=p
    return dataset_ptr

cdef class LSH:
    # Create a pointer to index
    cdef PRNearNeighborStructT _nnStruct
    cdef PPointT* _p_dataset
    cdef PPointT* _p_sampleQueries
    cdef int dimension
    def __cinit__(self,
                  float thresholdR,
                  float successProbability,
                  list dataset,
                  list sampleQueries,
                  int memoryUpperBound):
        """ The dataset is a list of tuples
        Each tuple has (index, [coordinates], sqrLength)
        The coordinates contains vectors  downscaled by
        a maximum scalar and then 1 number = sqrt(1-norm(x)^2)
        that has been appended.
        """
        self.dimension = len(dataset[0][1])
        cdef int len_dataset = len(dataset)
        cdef int len_sampleQueries = len(sampleQueries)
        _p_dataset = create_dataset_ptr(dataset,
                                        len_dataset,
                                        self.dimension)
        _p_sampleQueries = create_dataset_ptr(
            sampleQueries, len_sampleQueries, self.dimension)
        self._nnStruct = initSelfTunedRNearNeighborWithDataSet(
            thresholdR,
            successProbability,
            len_dataset,
            self.dimension,
            _p_dataset,
            len_sampleQueries,
            _p_sampleQueries,
            memoryUpperBound
            )
        return
    
    def query(self, queryvector):
        """ We must ensure in python code that the query vectors
        have a zero appended to them and that there magnitude are 1
        They can be anything that support dereferencing.

        The queryvector is just a single vector. (could be list or ndarr)
        """
        cdef PointT queryPoint
        queryPoint.index = 0
        queryPoint.sqrLength = 1
        queryPoint.coordinates = create_coordinates_ptr(
            queryvector, self.dimension)
        cdef PPointT* result = create_dataset_ptr(
            [(0, [0, 0, 0], 1)],
            1,
            self.dimension)
        cdef Int32T resultSize = 0
        st = time.clock()
        num_neighbor = getRNearNeighbors(
            self._nnStruct,
            &queryPoint,
            result,
            resultSize
            )
        et = time.clock() - st
        ret_list = [result[i].index
                    for i
                    in xrange(num_neighbor)]
        return dict(neighbors=ret_list,
                    time_taken=et)
