for i in D_sta*; do cd $i; for j in pos-5 pos-6; do cd $j ; qsub run.sh; cd ..; done ; cd ..; done
