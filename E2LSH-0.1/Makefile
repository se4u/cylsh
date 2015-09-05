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
OPTIONS =  -DREAL_FLOAT $$MIPS # -DDEBUG
# -march=athlon -msse -mfpmath=sse
LIBRARIES:=-lm
#-ldmalloc
MIPS_OPT_EXTRACTOR = if [ $* == mips ] ; then export MIPS=-DPERFORM_NEYSHABUR_MIPS; else export MIPS=-DNO_MIPS; fi; echo $$MIPS
CC = $$MYCOMPILER $(OPTIONS)
CXX = $$MYCOMPILER $(OPTIONS)
## CYTHON BINDING CREATION CODE
default: cython_binding_mips # Change this to cython_binding_e2lsh for normal lsh.
cython_binding_%:
	if which icpc >	/dev/null; then\
          export MYCOMPILER='icpc -fast';\
        else\
          export MYCOMPILER='g++ -O3';\
        fi; \
	$(MIPS_OPT_EXTRACTOR);\
	cd sources_py; \
	CC="$(CC)" CXX="$(CXX)" DOMIPS=$$MIPS python setup.py build_ext --inplace


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


## EXAMPLE
example:
	time PYTHONPATH=$$PWD/sources_py python -c "import cylsh, numpy; db=cylsh.LSH(0.7, 0.9,numpy.asarray([[.1, .7],[.11, .69]]), numpy.asarray([[.1, .7]]), 1e6); print db.query(numpy.array([.1, .7]));"

## TESTING CODE
test: test_mnist1k_cython_mips # test_gauss_cython_mips
TEST_OPT_EXTRACTOR = $(word $1,$(subst ~, ,$*))
# TEST_CMD = PYTHONPATH=$$PWD/sources_py python sources_py/test_api.py $(call TEST_OPT_EXTRACTOR,1) $+ $(call TEST_OPT_EXTRACTOR,2) $(call TEST_OPT_EXTRACTOR,3) $(call TEST_OPT_EXTRACTOR,4) > $@
TEST_CMD = PYTHONPATH=$$PWD/sources_py python sources_py/test_api.py
QSUB1 := qsub -b y -q all.q -V -j y -r yes -cwd submit_grid_stub.sh
test_mnist1k_cython_%: sample_data/mnist1k.dts sample_data/mnist1k.q
	$(TEST_CMD)
process_logs:
	python sources_py/process_logs.py "17 17.5 18 18.5 19 19.5 20" "2 4 6 8" "0.9 0.92 0.94 0.96 0.98"

qsub_gauss_cython:
	for R in 17 17.5 18 18.5 19 19.5 20; do \
	   for K in 2 4 6 8; do \
		for p in 0.9 0.92 0.94 0.96 0.98; do\
		  $(QSUB1) log/test_gauss_cython_mips~"$$R"~"$$K"~"$$p";\
		done; done; done
log/test_gauss_cython_%: sample_data/gauss.dts sample_data/gauss.q
	$(TEST_CMD)

R := 0.7
BINARY_DEP = sample_data/%.dts.mips sample_data/%.q.mips
test_with_binaries_%: $(BINARY_DEP)
	bin/lsh $(R) $+ | tee $@
how_good_are_binaries_%: $(BINARY_DEP)
	python src/how_good_are_binaries_at_mips.py $+ test_with_binaries_$*

## CLEANUP AND UTILITIES
clean:
	rm -rf sources_py/build sources_py/cylsh.cpp cylsh.so bin/LSHMain bin/compareOutputs bin/exactNNs

create_appended_data_file_for_use_with_binaries_%: sample_data/%.dts sample_data/%.q
	python sources_py/convert_mnist_data_to_bounded_data_by_dividing_by_norm_and_appending_diff.py $(word 1,$+) train > $(word 1,$+).mips
	python sources_py/convert_mnist_data_to_bounded_data_by_dividing_by_norm_and_appending_diff.py $(word 2,$+) query > $(word 2,$+).mips
