HAPPE \
-g config.ini \
-v ./data/00.annotated_vcf/SEVIR.592.SNP.ann.allele2.part.vcf.gz \
-r 5:6847970-6850236 \
-w 100 \
-d 20 \
-i ./data/02.sample_information//sample_inf.tsv \
-c ./data/02.sample_information//sample.color \
-D ./data/01.depth \
-k ./data/02.sample_information//small_example.list \
-o SEVIR_5G085400v2

