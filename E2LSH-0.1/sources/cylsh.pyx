###cython: nonecheck=True
"""This cython file provides a single class, the LSH class, that can be
initialized and then queried.
"""
import time
import cython
cimport lsh
from lsh cimport initSelfTunedRNearNeighborWithDataSet, getRNearNeighbors, PRNearNeighborStructT, PointT, PPointT, IntT, Int32T, RealT
from libc.stdlib cimport calloc, free

cdef RealT* create_coordinates_ptr(coordinate_vector, dimension):
    c = <RealT*>calloc(dimension, sizeof(RealT))
    for j in xrange(dimension):
        c[j]=coordinate_vector[j]
    return c

cdef PPointT* create_dataset_ptr(dataset, len_dataset, dimension):
    dataset_ptr=<PPointT*>calloc(len_dataset, sizeof(PPointT))
    for i, data in enumerate(dataset):
        p = <PPointT>calloc(1, sizeof(PointT))
        p.index=data[i][0]
        c = create_coordinates_ptr(data[i][1], dimension)
        p.coordinates=c
        p.sqrLength=data[i][2]
        dataset_ptr[i]=p
    return dataset_ptr

cdef class LSH:
    # Create a pointer to index
    cdef PRNearNeighborStructT nnStruct
    cdef PPointT* _p_dataset
    cdef PPointT* _p_sampleQueries
    def __cinit__(self,
                  float thresholdR,
                  float successProbability,
                  list dataset,
                  list sampleQueries,
                  int memoryUpperBound):
        """ The dataset contains vectors that have been downscaled by
        a maximum scalar and then a single number that is sqrt(1-norm(x)^2)
        has been appended.
        But the dataset is a list of tuples
        Each tuple has (index, [coordinates], sqrLength)
        """
        cdef int len_dataset = len(dataset)
        cdef int dimension = len(dataset[0][1])
        #self._p_dataset = create_dataset_ptr(dataset,
        # len_dataset,
        # dimension)
        cdef int len_sampleQueries = len(sampleQueries)
        self._p_sampleQueries = create_dataset_ptr(
            sampleQueries, len_sampleQueries, dimension)
        self.nnStruct = initSelfTunedRNearNeighborWithDataSet(
            thresholdR,
            successProbability,
            len_dataset,
            dimension,
            create_dataset_ptr(dataset,
                               len_dataset,
                               dimension),
            len_sampleQueries,
            self._p_sampleQueries,
            memoryUpperBound
            )
        return
    
    def query(self,
              queryvector,
              len_queryvector):
        """ We must ensure in python code that the query vectors
        have a zero appended to them and that there magnitude are 1
        They can be anything that support dereferencing.

        The queryvector is just a single vector. (could be list or ndarr)
        """
        cdef PointT queryPoint
        queryPoint.index = -1
        queryPoint.sqrLength = 1
        queryPoint.coordinates = create_coordinates_ptr(
            queryvector, len_queryvector)
        cdef PPointT* result
        cdef Int32T resultSize = 0
        st = time.clock()
        cdef Int32T num_neighbor = getRNearNeighbors(
            self.nnStruct,
            &queryPoint,
            result,
            resultSize
            )
        et = time.clock() - st
        ret_list = []
        for i in xrange(num_neighbor):
            ret_list[i] = result[i].index
        return ret_list
