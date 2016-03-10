#! /bin/tcsh

rm out_new/*
rm err_new/*

##### this is only for testing on HPC, don't fit gridsearch after tuning
foreach goal (precision f1 auc)
  foreach r (true false)
    bsub -W 1200 -o ./out_new/${goal}_${r}.out.%J -e ./err_new/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
  end
end


###### this is only for testing on HPC, exhuastive grid search
#foreach goal (precision f1 auc)
#  foreach r (false)
#    bsub -W 1200 -o ./out/${goal}_${r}.out.%J -e ./err/${goal}_${r}.err.%J /share3/wfu/miniconda/bin/python2.7 run.py run $goal $r
#  end
#end