#! /bin/tcsh

rm out_new/*
rm err_new/*
#
###### this is only for testing on HPC, don't fit gridsearch after tuning
#foreach goal (precision f1 auc)
#  foreach r (true false)
#    bsub -W 1200 -o ./out_new/${goal}_${r}.out.%J -e ./err_new/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
#  end
#end


###### this is only for testing on HPC, exhuastive grid search
#foreach goal (precision f1 auc)
#  foreach r (false)
#    bsub -W 1200 -o ./out/${goal}_${r}.out.%J -e ./err/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
#  end
#end


##### this is only for testing on HPC, testing cluster data idea
foreach goal (prec f)
  foreach VAR ( ant camel ivy jedit log4j lucene poi synapse velocity xerces )
    bsub -W 1200 -o ./out/${goal}_${VAR}.out.%J -e ./err/${goal}_${VAR}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py start /share3/wfu/data/$VAR $goal
  end
end

###### this is only for testing locally, testing cluster data idea
#foreach goal (f)
#  foreach VAR ( ant  )
#    python run.py start ./data/$VAR $goal
#  end
#end
