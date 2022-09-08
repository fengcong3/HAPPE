1. HAPPE supports SnpEff annotated vcf (containing ANN field), if your vcf is not annotated then the annotation information will not be displayed in the results. 
2. HAPPE supports only bi-allelic variants, including SNP/INDEL.
3. If you want to use the -r parameter, your input files must be vcf compressed using `bgzip`, not `gzip`, and have been indexed using `bcftools index`, and no other requirements. Cuz HAPPE will call the third-party command bcftools view -r chr22:22026076-22896111 input.vcf.gz, you need to ensure that this command can run normally.

