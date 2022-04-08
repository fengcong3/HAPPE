#fengcong@caas.cn
#2020-9-1 15:15:39
#usage:python __file__ -r chr1A_part1:0-50 -a 10 -b 10 -f test.bed.gz > out.txt
import gzip
import sys,os
import argparse
import subprocess 

part_len="/public/agis/chengshifeng_group/fengcong/WGRS/software/Fc-code/partlen.txt"


if __name__ == "__main__":
    cmdparser = argparse.ArgumentParser(description="11./fengcong@caas.cn" )

    cmdparser.add_argument("-r","--region", dest="region",type=str, required=True,
                            help="region,0-based,e.g. -r chrUn:1-50")
    cmdparser.add_argument("-a","--average", dest="average",type=float, required=True,
                            help="average depth of that chromosome,e.g -a 7.82")
    cmdparser.add_argument("-b","--bin", dest="bin",type=int, default=1,
                            help="bin size,default:1")
    cmdparser.add_argument('-f', metavar='depthfile', type=str, 
                        help='depth bed file(can be bgziped)')
    cmdparser.add_argument("-t","--step", dest="step",type=int,
                            help="step,default : --bin")
    cmdparser.add_argument("-s","--stdin", dest="stdin",action="store_true",
                        help="read data from stdin,ignore depthfile")
    
    args = cmdparser.parse_args()

    inf = None

    if args.stdin:
        inf = sys.stdin
    else:
        if args.depthfile != None:
            infn = args.depthfile
            if infn.endswith(".gz"):
                inf = gzip.open(infn,"rt")
            else:
                inf = open(infn,"r")
        else:
            print("no depthfile")
            exit(-1)
    

    part_len_d={}
    infp = open(part_len,"r")
    for line in infp.readlines():
        part_len_d[line.strip().split()[0]] = int(line.strip().split()[1])
    infp.close()
    
    chromosome = args.region.split(":")[0]
    start = int(args.region.split(":")[1].split("-")[0])
    end = int(args.region.split(":")[1].split("-")[1])

    depth_list=[]
    for i in range(start,end,1):
        depth_list.append(0)


    line = inf.readline()
    while line:
        ls = line.strip().split()
        
        if chromosome == ls[0]:
            for i in range(int(ls[1]),int(ls[2]),1):
                if i >= start and i < end:
                    depth_list[i-start] = float(ls[3]) /args.average


        line = inf.readline()

    step=args.step
    if step ==None:
        step=args.bin
    # bin_num=0
    # bin_sum=0
    # bin_pos=start
    # for i in depth_list:
    #     bin_sum += i
    #     bin_num+=1
        
    #     if bin_num == args.bin:
    #         sys.stdout.write("%d\t%f\n"%(bin_pos,bin_sum/bin_num))
    #         bin_num=0
    #         bin_sum=0

    #     bin_pos+=1

    start_pos=0
    ab_start_pos=start if not chromosome.endswith("part2") else start+part_len_d[chromosome.replace("part2","part1")]
    # end_pos=len(depth_list)-1-args.bin+1
    while start_pos <=len(depth_list)-1:
        bin_sum=0
        endd=start_pos+args.bin
        if endd > len(depth_list):
            endd=len(depth_list)
        for i in range(start_pos,endd):
            bin_sum+=depth_list[i]
        sys.stdout.write("%d\t%f\n"%(ab_start_pos,bin_sum/args.bin))
        # sys.stdout.write("%f\n"%(bin_sum/args.bin))
        start_pos+=step
        ab_start_pos+=step

    
    inf.close()