#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
# script: multiRun_healthy.sh
# author: Lincoln Harris
# date: 8.15.18
# 
# Can I run this on more than one cell at a time? 
# 		ohhh shit i think this is workin!!
#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
#!/bin/bash

driver () {
	docker run -v `pwd`:/data --rm trinityctat/ctatfusion /usr/local/src/STAR-Fusion/STAR-Fusion --left_fq /data/${dir}/*_R1_001.fastq --right_fq /data/${dir}/*_R2_001.fastq --genome_lib_dir /data/ctat_genome_lib_build_dir/ -O /data/StarFusionOut/${dir}/ --FusionInspector inspect --CPU 30 --STAR_use_shared_memory --no_filter
}

root_dir=/home/ubuntu/sandbox_expansion1/07-STARfus/02-TH238/02-healthyCells

i=0

for dir in *; 
do 
	driver "$dir"
	#driver "$dir" &

	# limit to X number of procs
	#if (( $i % 10 == 0 )); 
	#then 
	#	wait; 
	#fi
	#i=$((i+1))
done

wait

#/////////////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////////////
