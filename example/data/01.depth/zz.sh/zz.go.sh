bam_path="path_to_bam"
ref_path="path_to_ref"
for sample in `cat vcf.sample.list`
do
    mkdir ../$sample
    echo "
    mosdepth -t 2  -f$ref_path/Setaria_viridis.fa  -Q 0  ../$sample/${sample}.Q0  $path_to_bam/$sample.sorted.markdup.bam
    " > $sample.depth.sh ## then, run all the shell script
done
