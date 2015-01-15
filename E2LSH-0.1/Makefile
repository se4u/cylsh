SOURCES_DIR:=sources
OBJ_DIR:=bin
OUT_DIR:=bin
TEST_DIR:=$(SOURCES_DIR)

#H_SOURCES:=`find $(SOURCES_DIR) -name "*.h"`
#CPP_SOURCES:=`find $(SOURCES_DIR) -name "*.cpp"`
#TEST_SOURCES:=`find $(TEST_DIR) -name "*.cpp"`
OBJ_SOURCES:=$(SOURCES_DIR)/BucketHashing.cpp \
	     $(SOURCES_DIR)/Geometry.cpp \
	     $(SOURCES_DIR)/LocalitySensitiveHashing.cpp \
	     $(SOURCES_DIR)/Random.cpp \
	     $(SOURCES_DIR)/Util.cpp \
	     $(SOURCES_DIR)/GlobalVars.cpp \
	     $(SOURCES_DIR)/SelfTuning.cpp \
	     $(SOURCES_DIR)/NearNeighbors.cpp

LSH_BUILD:=LSHMain

TEST_BUILDS:=exactNNs \
            genDS \
	    compareOutputs \
	    genPlantedDS

GCC:=g++ -O3
OPTIONS =  -DREAL_FLOAT $$MIPS
# -march=athlon -msse -mfpmath=sse
LIBRARIES:=-lm 
#-ldmalloc
MIPS_OPT_EXTRACTOR = if [ $* == mips ] ; then export MIPS=-DPERFORM_NEYSHABUR_MIPS; else export MIPS=-DNO_MIPS; fi; echo $$MIPS
binaries_%:
	$(MIPS_OPT_EXTRACTOR);\
	$(MAKE) c && $(MAKE) ct

c:
	@mkdir -p $(OUT_DIR)
	$(GCC) -o $(OUT_DIR)/$(LSH_BUILD) $(OPTIONS) $(OBJ_SOURCES) $(SOURCES_DIR)/$(LSH_BUILD).cpp $(LIBRARIES)
	chmod g+rwx $(OUT_DIR)/$(LSH_BUILD)

ct:
	@mkdir -p $(OUT_DIR)
	(for i in $(TEST_BUILDS); do \
	 $(GCC) -o $(OUT_DIR)/$$i $(OPTIONS) $(OBJ_SOURCES) $(TEST_DIR)/$${i}.cpp $(LIBRARIES); chmod g+rwx $(OUT_DIR)/$$i; done)

CC = $$MYCOMPILER $(OPTIONS)
CXX = $$MYCOMPILER $(OPTIONS)
# This create cylsh.so
cython_binding_%:
	if which icpc >	/dev/null; then\
          export MYCOMPILER='icpc -fast';\
        else\
          export MYCOMPILER=='g++ -O3';\
        fi; \
	$(MIPS_OPT_EXTRACTOR);\
	cd sources_py; \
	CC="$(CC)" CXX="$(CXX)" DOMIPS=$$MIPS python setup.py build_ext --inplace

test_cython_binding_%:
	time PYTHONPATH=$$PWD/sources_py python -c "import cylsh, numpy; db=cylsh.LSH(0.7, 0.9,numpy.asarray([[.1, .7],[.11, .69]]), numpy.asarray([[.1, .7]]), 1e6); print db.query(numpy.array([.1, .7]));"

clean:
	rm -rf sources_py/build sources_py/cylsh.cpp cylsh.so bin/LSHMain bin/compareOutputs bin/exactNNs
