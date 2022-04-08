#coding:utf-8
# fengcong@caas.cn
# created by fengcong on 2021-8-30 14:50:23
# pipeline of excel haplotype 

import sys
import os
import argparse
import logging
import configparser

logging.basicConfig(level = logging.DEBUG,format = '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',stream = sys.stderr)
logger = logging.getLogger("HAPPE")
# logger.info("Start print log")
# logger.debug("Do something")
# logger.warning("Something maybe fail.")
# logger.info("Finish")


#sample file path
script_dir = os.path.split(os.path.realpath(__file__))[0]
cluster_py = script_dir + "/hierarchy_clustering.py"
pheat_py = script_dir + "/pheat2excel_V5.py"
sampleinf_py=script_dir + "/sampleinf2excel_V2.py"
tree_py = script_dir + "/tree2excel_v3.py"
vcf2heat= script_dir + "/vcf2heatmatrix.py"
filter_func_py= script_dir +  "/filter_functional_SNP.py"
filter_cod_py= script_dir + "/filter_codingregion_SNP.py"
filter_noncod_py = script_dir + "/filter_noncodingregion_SNP.py"
depth2excel = script_dir + "/depth2excel.py"

# color_file = "/vol3/agis/chengshifeng_group/fengcong/wheat_pop_analysis/40.89mapping_and_merge/14.final_SNP_filter2/0x.some_required_file/pca_1059.pop.color"
# sampleinf = "/vol3/agis/chengshifeng_group/fengcong/wheat_pop_analysis/40.89mapping_and_merge/14.final_SNP_filter2/0x.some_required_file/1059_Inf.txt"
# funcann = "/vol1/agis/chengshifeng_group/fengcong/30sample_popTest/04.snp_anno/iwgsc_refseqv1.0_FunctionalAnnotation_v1__HCgenes_v1.0.TAB"
# svfile = "/vol3/agis/chengshifeng_group/zhangchaofan/03.pansv/08.merge/06.total/02.sample_merge_vcf_v3/02.diff_type_SV/05.merge/delly_lumpy.merge.filter.sorted.rename.vcf.gz"
# depthdir="/vol3/agis/chengshifeng_group/fengcong/zz.wheat_data.zz/02.1059_depth_data"

bcftools = "bcftools"
#
python3 = sys.executable
bgzip = "bgzip"
tabix= "tabix"
#

def check_ret(ret,step):
    if  ret:
        logger.error("%s -- retrun code:%d\n"%(step,ret))
        exit(-1)

def main1():
    cmdparser = argparse.ArgumentParser(description="show haplotype patterns in excel file./fengcong@caas.cn" )
    #general options
    cmdparser.add_argument("-g","--config", dest="config",type=str, required=True,
                            help="config file.[required]")
    cmdparser.add_argument("-v","--gzvcf", dest="gzvcf",type=str, required=True,
                            help="gzvcf, bcftools indexed.use to annotation and get ref/alt basepair.[required]")
    cmdparser.add_argument("-k","--keep", dest="keep",type=str, required=False,
                            help="keep sample, if u wana plot a subset of --gzvcf.[optional]")
    cmdparser.add_argument("-r","--region", dest="region",type=str, required=False,
                            help="if u wana plot a subset of --gzvcf, u can use this option. if u use this option , ucant use -s option[optional]")
    cmdparser.add_argument("-s","--snplist", dest="snplist",type=str,required=False,
                            help="snp id list(format:chr_pos). if u use this option , u cant use -r option.[optional]")
    cmdparser.add_argument("-i","--inf", dest="inf",type=str, required=True, 
                            help="the information  of each sample.[required]")
    cmdparser.add_argument("-c","--color", dest="color",type=str, required=True,
                            help="the color  of each sample.[required]")
    # u can give more information about SNP to plot, such as:
    cmdparser.add_argument("-I","--snpinf", dest="snpinf",type=str, required=False,
                            help="more information about SNP.[optional]")
    cmdparser.add_argument("-R","--Ref", dest="Ref",type=str, required=False,
                            help="change Reference and color system.[optional]")
    cmdparser.add_argument("-F","--FuncAnn", dest="FuncAnn",type=str, required=False,
                            help="functional annotation file.[optional]")

    group = cmdparser.add_mutually_exclusive_group()
    group.add_argument("-f","--functional", dest="functional",action="store_true" ,
                            help="only functional SNP")
    group.add_argument("-x","--coding", dest="coding",action="store_true" ,
                            help="only coding region SNP")
    group.add_argument("-n","--noncoding", dest="noncoding",action="store_true" ,
                            help="only noncoding region SNP")
    
    # #SV and depth
    # cmdparser.add_argument("-S","--SV", dest="SV",type=str, required=False,nargs='?', const=svfile,
    #                         help="plot SV.\033[31m[use -S directly if is wheat,else u must specify SV file,optional]\033[0m")
    cmdparser.add_argument("-D","--Depth", dest="Depth",type=str, required=False,
                            help="depth dir for each sample.[optional]")
    cmdparser.add_argument("-d","--Depthbin", dest="Depthbin",type=str, required=False,default=50,
                            help="Depth bin size.[optional,default:50]")

    #output prefix , u must give this option    
    cmdparser.add_argument("-o","--output", dest="output",type=str, required=True,
                            help="output prefix")
    
    
    # deal args
    args = cmdparser.parse_args()
    # logger.debug("Presenting the most raw data in the dumbest way possible can lead to amazing discoveries.")
    logger.info("deal args.")

    #args.config
    if os.path.exists(args.config) :
        configf = os.getcwd()+"/"+args.config if not args.config.startswith("/") else args.config
    else:
        logger.error("%s  not exist"%(args.config))
        exit(-1)
    
    ##read config
    config = configparser.ConfigParser()
    config.read(configf)
    bgzip = config.get("software","bgzip")
    bcftools = config.get("software","bcftools")
    tabix = config.get("software","tabix")


    #args.gzvcf
    if os.path.exists(args.gzvcf) :
        gzvcf = os.getcwd()+"/"+args.gzvcf if not args.gzvcf.startswith("/") else args.gzvcf
    else:
        logger.error("%s  not exist"%(args.gzvcf))
        exit(-1)
    
    #args.keep
    if args.keep and os.path.exists(args.keep):
        keep = args.keep
    else:
        keep = None
    
    #args.region
    if args.region:
        region = args.region
    else:
        region = None

    if args.snplist:
        snplist = args.snplist
    else:
        snplist = None
    
    #args.inf
    if os.path.exists(args.inf) :
        inf = args.inf
    else:
        logger.error("%s not exist"%(args.inf))
    
    #args.color
    if os.path.exists(args.color) :
        color = args.color
    else:
        logger.error("%s not exist"%(args.color))

    #args.snpinf
    if args.snpinf and os.path.exists(args.snpinf):
        snpinf = args.snpinf
    else:
        snpinf = None

    if args.Ref :
        Ref  = args.Ref
    else:
        Ref = None

    #args.output
    if args.output :
        output_prefix = args.output
        output_dir = os.path.dirname(args.output)
        #create output dir
        if not os.path.exists(output_dir) and output_dir:
            os.makedirs(output_dir)

    #args.FuncAnn
    funcannf = None
    if args.FuncAnn:
        if os.path.exists(args.FuncAnn) :
            funcannf =  args.FuncAnn
        else:
            logger.error("%s not exist"%(args.FuncAnn))

    #args.functional
    functional = args.functional
    coding = args.coding
    noncoding = args.noncoding
    
    ###########################################################################################
    # keep and filter snp
    logger.info("Filter samples and variants.")
    if region:
        ret = os.system("""
        #eg. bcftools view -r chr1A:1-100 -S sample.list test.vcf.gz | bgzip -c > out.vcf.gz
        %s view %s %s %s | %s -c > %s.vcf.gz
        %s
        %s
        %s
        """%( bcftools , "-r %s"%(region) if region else "", "-S %s"%(keep) if keep else "" , gzvcf ,
            bgzip, output_prefix,
            "%s %s %s.vcf.gz | %s -c > %s.vcf.gz.bak && mv %s.vcf.gz.bak %s.vcf.gz" % (
                python3 ,filter_func_py , output_prefix , bgzip , output_prefix , output_prefix , output_prefix 
                ) if functional else "",

            "%s %s %s.vcf.gz | %s -c > %s.vcf.gz.bak && mv %s.vcf.gz.bak %s.vcf.gz" % (
                python3 ,filter_cod_py , output_prefix , bgzip , output_prefix , output_prefix , output_prefix 
                ) if coding else "",
            
            "%s %s %s.vcf.gz | %s -c > %s.vcf.gz.bak && mv %s.vcf.gz.bak %s.vcf.gz" % (
                python3 ,filter_noncod_py , output_prefix , bgzip , output_prefix , output_prefix , output_prefix 
                ) if noncoding else "",
            ) 
        )

    elif snplist:
        ret = os.system("""
        for i in `cat %s`;
        do
            chr=`echo $i | cut -f 1 -d "_"`
            pos=`echo $i | cut -f 2 -d "_"`
            %s view -r $chr:$pos-$pos  %s %s | tail -n 1 >> %s.vcf.tmp2
        done
        %s view -r $chr:$pos-$pos %s %s | head -n -1 > %s.vcf.tmp
        cat %s.vcf.tmp %s.vcf.tmp2 | %s -c > %s.vcf.gz && rm %s.vcf.tmp %s.vcf.tmp2
        """%( snplist ,
            bcftools, "-S %s"%(keep) if keep else "" ,gzvcf ,output_prefix,
            bcftools ,"-S %s"%(keep) if keep else "" , gzvcf , output_prefix,
            output_prefix, output_prefix,bgzip , output_prefix , output_prefix , output_prefix
            ) 
        )
    else:
        ret = os.system("""
        cd %s;
        ln -s %s %s.vcf.gz
        """%(output_dir, gzvcf , output_prefix)
        )

    check_ret(ret,"Filter samples and variants.")
    ###########################################################################################
    # vcf to heat format
    logger.info("convert file format.")
    ret = os.system("""
    # eg. python3 vcf2heatmatrix.py -v out.vcf.gz  > out.heat
    %s %s -v %s.vcf.gz > %s.heat 
    """%(python3 , vcf2heat , output_prefix ,
        output_prefix)
    )

    check_ret(ret,"convert file format.")

    ###########################################################################################
    # clustering using pheat file
    logger.info("hierarchy clustering.")
    ret = os.system("""
    #eg. python3 hierarchy_clustering.py  out.heat out.cluster.newick
    %s %s %s.heat %s.newick %s.cluster 1>/dev/null
    """%(python3 , cluster_py , output_prefix , output_prefix , output_prefix)
    )
    check_ret(ret,"hierarchy clustering")

    ###########################################################################################
    # read snp information file
    logger.info("read snp information file.")
    info_num = 0
    if snpinf:
        snp_info = {} # {snpid:{p-value: 1e-5 , addi: -5, ...}}
        snp_info_field = []
        with open(snpinf) as f:
            #read header
            header_list = f.readline().strip().split()
            snp_info_field = header_list[1:]
            for line in f:
                ls = line.strip().split()
                snp_info[ls[0]] = {}
                for index , info in enumerate( header_list[1:] ):
                    snp_info[ ls[0] ][ info ] = ls[index + 1]

                if info_num == 0:
                    info_num = len(ls) - 1
                else:
                    if info_num == len(ls) - 1:
                        pass
                    else:
                        logger.error("different col num of snp information file.")
                        exit(-1)

    ###########################################################################################
    # calc SNP info row num
    # stable rows: SNP_id , CS , alt , feature id , annotation ,protein change    and    information header line
    # variable rows: more snp information 

    snp_info_row_num = 8 + info_num if funcannf else 7 + info_num

    logger.info("calc out the snp_info_row_num = %d."%(snp_info_row_num))
    ###########################################################################################
    # plot tree to excel file
    logger.info("plot tree to excel file.")
    ret = os.system("""
    #eg. python3 tree2excel_v2.py -c color_file -o out.xlsx -i snp_info_row_num  out.newick > out.maxd_order
    %s %s -c %s  -o %s.tree.xlsx -i %d %s.newick > %s.maxd_order
    """%(python3 , tree_py , color,  output_prefix , snp_info_row_num , output_prefix , output_prefix)
    )

    check_ret(ret,"plot tree to excel file")

    ###########################################################################################
    # get sample information start col and get sample order
    logger.info("get sample information start col and get sample order.")
    maxd_order_file = open("%s"%(args.output+".maxd_order"),"r")
    maxd = int(maxd_order_file.readline().strip())
    maxd_order_file.close()

    # 
    ret = os.system("""
    tail -n +2 %s.maxd_order > %s.order 
    """%(output_prefix, output_prefix ))

    check_ret(ret,"get sample information start col and get sample order")

    
    ###########################################################################################
    # write sample information to excel file
    logger.info("write sample information to excel file.")
    ret = os.system("""
    #eg. python3 sampleinf2excel_V2.py 
    %s %s -o %s.inf.xlsx -e %s.tree.xlsx -i %s -r %d -s %d,%d -d %s.order -c %s > %s.heat.start 
    """%(python3 , sampleinf_py,output_prefix, output_prefix , inf , 2,
        snp_info_row_num ,maxd+2 ,output_prefix  , color , output_prefix)
    )

    check_ret(ret,"write sample information to excel file")

    ###########################################################################################
    #get start col
    heat_start_file = open("%s.heat.start"%(output_prefix),"r")
    heat_start = int(heat_start_file.readline().strip()) + 1
    heat_start_file.close()
    # os.remove("%s.heat.start"%(output_prefix))

    ###########################################################################################
    #plot heat to excel file
    logger.info("plot genotype matrix to excel file.")
    ret = os.system("""
    %s %s -i %s.heat -o %s.Haplotype.xlsx -e %s.inf.xlsx -v %s.vcf.gz -r %d -s %d,%d -d %s.order -c %s -t %s.cluster  %s %s %s > %s.next.start
    """%(python3, pheat_py, output_prefix, output_prefix , output_prefix , output_prefix, 
        2 , 1, heat_start , output_prefix , color , output_prefix ,
        "-R %s"%(Ref) if Ref else "" , "-m %s"%(snpinf) if snpinf else "" ,"-F %s"%(funcannf) if funcannf else ""  ,
        output_prefix )
    )

    check_ret(ret,"add heat matrix")

    ###########################################################################################
    #
    #plot dp to excel file
    if args.Depth:
        logger.info("plot RDV to excel file.")
        sfile="%s.next.start"%(output_prefix)
        with open(sfile) as f:
            nstart = f.readline().strip()


        ret = os.system("""
        %s %s \
        -r %s \
        -D %s \
        -d %s.order \
        -c %s \
        -x 2 \
        -s  %s\
        -e %s.Haplotype.xlsx \
        -t %s \
        -o %s.Haplotype.xlsx 
        """%(python3, depth2excel, region , args.Depth , output_prefix ,args.Depthbin,
        nstart, output_prefix,tabix,output_prefix )
        )
        check_ret(ret,"add RDV matrix")
    ###########################################################################################
    # remove tmp file
    logger.info("remove tmp file.")
    os.remove("%s.vcf.gz"%(output_prefix))
    os.remove("%s.order"%(output_prefix))
    os.remove("%s.maxd_order"%(output_prefix))
    os.remove("%s.newick"%(output_prefix))
    os.remove("%s.heat"%(output_prefix))
    os.remove("%s.cluster"%(output_prefix))
    os.remove("%s.heat.start"%(output_prefix))
    os.remove("%s.tree.xlsx"%(output_prefix))
    os.remove("%s.inf.xlsx"%(output_prefix))
    os.remove("%s.next.start"%(output_prefix))

    logger.info("Done.")

       

if __name__ == "__main__":
    main1()