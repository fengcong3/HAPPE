# HAPPE

A tool to visualize the haplotype pattern and various information in excel.
Please cite this paper when using HAPPE for your publications
> Cong Feng, Xingwei Wang, Shishi Wu, Weidong Ning, Bo Song, Jianbin Yan, and Shifeng Cheng. 2022. “HAPPE: A Tool for Population Haplotype Analysis and Visualization in Editable Excel Tables.” Frontiers in Plant Science 13 (July): 927407. https://doi.org/10.3389/fpls.2022.927407.


![avatar](./Figure_S2.jpg)


## Installing HAPPE

There easiest way to install `HAPPE` is to use pip3. 

```sh
pip3 install HAPPE
```

or you can clone the project to your local directory and installing it with:

```sh
python3 setup.py install --record log.txt
#if u want to uninstall the package:
#cat log.txt | xargs rm -rf
```

then you should have the  `HAPPE` command available.
```sh
$ HAPPE -h

usage: HAPPE [-h] -g CONFIG -v GZVCF [-k KEEP] [-r REGION]
                          [-s SNPLIST] -i INF -c COLOR [-I SNPINF] [-R REF]
                          [-F FUNCANN] [-f | -x | -n] [-D DEPTH] [-d DEPTHBIN]
                          -o OUTPUT

show haplotype patterns in excel file./fengcong@caas.cn

optional arguments:
  -h, --help            show this help message and exit
  -g CONFIG, --config CONFIG
                        config file.[required]
  -v GZVCF, --gzvcf GZVCF
                        gzvcf, bcftools indexed.use to annotation and get
                        ref/alt basepair.[required]
  -k KEEP, --keep KEEP  keep sample, if u wana plot a subset of
                        --gzvcf.[optional]
  -r REGION, --region REGION
                        if u wana plot a subset of --gzvcf, u can use this
                        option. if u use this option , ucant use -s
                        option[optional]
  -s SNPLIST, --snplist SNPLIST
                        snp id list(format:chr_pos). if u use this option , u
                        cant use -r option.[optional]
  -w TREEWIDTH, --treewidth TREEWIDTH
                        How many columns do you want to occupy for this tree
                        topology.(default=1000)[optional]
  -i INF, --inf INF     the information of each sample.[required]
  -c COLOR, --color COLOR
                        the color of each sample.[required]
  -I SNPINF, --snpinf SNPINF
                        more information about SNP.[optional]
  -R REF, --Ref REF     change Reference and color system.[optional]
  -F FUNCANN, --FuncAnn FUNCANN
                        functional annotation file.[optional]
  -f, --functional      only functional SNP
  -x, --coding          only coding region SNP
  -n, --noncoding       only noncoding region SNP
  -D DEPTH, --Depth DEPTH
                        depth dir for each sample.[optional]
  -d DEPTHBIN, --Depthbin DEPTHBIN
                        Depth bin size.[optional,default:50]
  -o OUTPUT, --output OUTPUT
                        output prefix
```
## Preparing config file
```ini
[software]
bgzip=
bcftools=
tabix=
partlen=
```
Because some software cant deal with chromosome bigger than 512Mbp, so we need to split the chromosome into several parts.`partlen` is the file that contains the length of each part. Mainly used for the depth information extraction.
## Preparing the vcf file

1. The SNP/INDEL ID must be in the format :`Chromosome_position`.
2. Only bi-allelic remains in vcf file.
2. Compress `vcf` to `vcf.gz` using bgzip
3. Use `bcftools index` to create an index for the `vcf.gz` file.

## Preparing the depth information
if you want to integrate the depth information, you need to prepare the depth file as follows:

1. Create a directory for each sample with the name of the sample.
2. using `mosdepth` to calc the depth of each position for each sample.
```sh
#example
mosdepth -f ref.fa -Q 0 sample1/sample1.Q0  path/to/sample1.bam
```

## Usage
```sh
"-g  CONFIG", required parameter, give the paths to bcftools, bgzip and tabix in the CONFIG file. 

"-v GZVCF", required parameter, input vcf file.

"-k SAMPLELIST", required parameter, list of samples to be retained, one sample per line.

"-r REGION", optional parameter, the genomic region to be displayed, format: chromosome: start-end.

"-s VARIANTLIST", optional parameter, the list of variant IDs you need to keep, using this parameter you cannot use the -r parameter.

"-w TREEWIDTH", optional parameter, the width of the tree topology.

"-i INFORMATION", optional parameter, additional sample information, the first column must be the sample ID.

"-c COLOR", optional parameter, Specify the color of each sample, the first column is the sample id and the second column is the color hex code.

"-I VARINFORMATION", optional parameter, Additional variant annotation information, such as GWAS p-value. the first colum is the variant id and each column is the annotation information with header.

"-f", optional parameter, Only the variant that changes the amino acid is retained.( Requires that the input vcf file has been annotated with SnpEff.)

"-x", optional parameter, Only the variant in the CDS region is retained.( Requires that the input vcf file has been annotated with SnpEff.)

"-n"， optional parameter, Only the variant in the non-coding region is retained.( Requires that the input vcf file has been annotated with SnpEff.)

"-D DIRECTORY"， optional parameter, This directory contains the depth information for each sample calculated using mosdepth, one directory per sample.

"-d WINDOWSIZE", optional parameter, window size for calculate normalized depth.

"-o PREFIX"， required parameter, output prefix.

```
## example
The example data covered in the publication is in the `example/` folder.

```sh
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


## each file of the prameter
## -g config.ini
# [software]
# bgzip=path_to/bgzip
# bcftools=path_to/bcftools
# tabix=path_to/tabix

## -i ./data/02.sample_information//sample_inf.tsv
## Just make sure the first column is the sample name.
# Sample_ID	... ...
# sample1   ... ...

## -c ./data/02.sample_information//sample.color
## Just make sure the first column is the sample name and the second column is color code.
# Sample_ID	color
# sample1	FF0000
# ...       ...

## -F FunctionalAnnotation_v1__HCgenes_v1.0.TAB
## just make sure the first column is the gene name , and the forth column is the functional annotation.
# Gene_name	XXX XXX function ... ...
# gene1     XXX XXX func1    ... ...

## -D ./data/01.depth
##Make sure that the files *mosdepth.summary.txt and *per-base.bed.gz are in the directory for each sample in this directory.
```
