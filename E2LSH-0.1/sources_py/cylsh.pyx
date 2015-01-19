#clib library_with_useful_functions
#cython: nonecheck=True
#cython: boundscheck=True
"""This cython file provides a single class, the LSH class, that can be
initialized and then queried.
"""
import time, cython
import numpy as np
cimport numpy as np
np.import_array()
cimport lsh
from lsh cimport PRNearNeighborStructT, PointT, PPointT, IntT, Int32T, RealT, initSelfTunedRNearNeighborWithDataSet, getRNearNeighbors, computeOptimalParameters, initLSH_WithDataSet, RNNParametersT
#from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.stdlib cimport malloc, free
DTYPE=np.float
ctypedef np.float_t DTYPE_t
cdef RealT* create_coordinates_ptr(
    np.ndarray[DTYPE_t, ndim=1] coordinate_vector,
    int dimension):
    """ Simply copy over the data from numpy array
    to a RealT array
    """
    c = <RealT*>malloc(dimension*sizeof(RealT))
    for j in xrange(dimension):
        c[j]=coordinate_vector[j]
    return c

cdef PPointT* create_dataset_ptr(
    np.ndarray[DTYPE_t, ndim=2] dataset,
    int len_dataset,
    int dimension,
    ):
    dataset_ptr=<PPointT*>malloc(len_dataset*sizeof(PPointT))
    for i in xrange(len_dataset):
        p = <PPointT>malloc(sizeof(PointT))
        p.index=i
        p.coordinates=create_coordinates_ptr(dataset[i],
                                             dimension)
        p.sqrLength=1.0
        dataset_ptr[i]=p
    return dataset_ptr

cdef class LSH:
    """ This class auto-tunes the parameters of the LSH index
    and prints them out to stderr. It provides only one method
    for querying.
    >>> import cylsh;
    >>> import numpy as np
    >>> db=cylsh.LSH(0.9,
                    0.9,
                    np.asarray([[.1, .7, .7],
                                [.11, .69, .7]]),
                    np.asarray([[.1, .7, .7]]),
                    1e6);
    >>> print db.query(np.asarray([.1, .7, 0]))
    """
    cdef PRNearNeighborStructT _nnStruct
    cdef int dimension
    def __cinit__(self):
        return

    @staticmethod
    def optimize_and_initialize(
                  float thresholdR,
                  float successProbability,
                  np.ndarray[DTYPE_t, ndim=2] dataset,
                  np.ndarray[DTYPE_t, ndim=2] sampleQueries,
                  int memoryUpperBound,
                  bint debug
                  ):
        """ The dataset is a numpy ndarray with datapoint x dimension
        size. Every datapoint only has unit norm.
        """
        self=LSH()
        cdef int len_dataset = dataset.shape[0] 
        cdef int len_sampleQueries = sampleQueries.shape[0]
        # Preprocessor Hack to simplify the API and pass compile
        # time information.
        IF DOMIPS == "yes":
            norm_dataset=np.sqrt(np.sum(np.square(dataset), axis=1))
            max_norm=np.max(norm_dataset)
            slack = np.expand_dims(np.sqrt(1 - np.square(norm_dataset/max_norm)),
                                  axis=1)
            if debug:
                print dataset.shape[0], dataset.shape[1], slack.shape[0], \
                    slack.shape[1]
            dataset = np.concatenate((dataset/max_norm, slack), axis=1)
            norm_query = np.sqrt(np.sum(np.square(sampleQueries),
                                        axis=1))
            sampleQueries = np.concatenate(
                (sampleQueries, np.zeros([len_sampleQueries, 1], DTYPE)),
                axis=1)
        ELSE:
            pass
        ## The Above code would simply be excluded if DOMIPS
        ## is not supplied at compile time
        
        self.dimension = dataset.shape[1]
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
        return self
    
    def query(self, np.ndarray[DTYPE_t, ndim=1] queryvector):
        """ We must ensure in python code that the query vectors
        have a zero appended to them and that there magnitude are 1
        for doing a MIPS query. This function only does vanilla lsh.
        They can be anything that support dereferencing.

        The queryvector is just a single vector. (could be list or ndarr)
        The output is a dictionary with two keys referencing the time taken
        and the indices of neighbors.
        """
        cdef PointT queryPoint
        queryPoint.index = 0
        IF DOMIPS == "yes":
            queryvector = np.concatenate(
                (queryvector/np.linalg.norm(queryvector),
                 np.zeros(1)))
            queryPoint.sqrLength = 1
        ELSE:
            queryPoint.sqrLength = np.sum(np.square(queryvector))
        queryPoint.coordinates = create_coordinates_ptr(
            queryvector, self.dimension)
        cdef Int32T resultSize = 100
        cdef PPointT* result = create_dataset_ptr(
            np.zeros([resultSize, self.dimension], DTYPE),
            resultSize,
            self.dimension)
        
        st = time.time()
        num_neighbor = getRNearNeighbors(
            self._nnStruct,
            &queryPoint,
            result,
            resultSize
            )
        et = time.time() - st
        ret_list = np.zeros(num_neighbor, np.int)
        for i in xrange(num_neighbor):
            ret_list[i] = result[i].index
        return dict(neighbors=ret_list,
                    time_taken=et)

    @staticmethod
    def compute_optimal_parameters(
        float R,
        float successProbability, 
        np.ndarray[DTYPE_t, ndim=2] dataset,
        np.ndarray[DTYPE_t, ndim=2] sampleQueries,
        int memoryUpperBound,
        ):
        cdef int nPoints = dataset.shape[0]
        cdef int dimension = dataset.shape[1]
        cdef int nSampleQueries = sampleQueries.shape[0]
        return computeOptimalParameters(
            R,
            successProbability, 
            nPoints,
            dimension,
            create_dataset_ptr(dataset, nPoints, dimension),
            nSampleQueries,
            create_dataset_ptr(sampleQueries, nSampleQueries, dimension),
            memoryUpperBound)

    @staticmethod
    def init_manually(dict params,
                      np.ndarray[DTYPE_t, ndim=2] dataset):
        self=LSH()
        cdef int nPoints = dataset.shape[0]
        cdef int dimension = dataset.shape[1]
        self.dimension = dimension
        self._nnStruct = initLSH_WithDataSet(
            RNNParametersT(
                parameterR=params['parameterR'],
                successProbability=params['successProbability'],
                dimension=params['dimension'],
                parameterR2=params['parameterR2'],
                useUfunctions=params['useUfunctions'],
                parameterK=params['parameterK'],
                parameterM=params['parameterM'],
                parameterL=params['parameterL'],
                parameterW=params['parameterW'],
                parameterT=params['parameterT'],
                typeHT=params['typeHT']),
            nPoints,
            create_dataset_ptr(dataset,
                               nPoints,
                               dimension)
            )
        return self
    
    def __dealloc__(self):
        """ Implement me
        """ 
        pass
