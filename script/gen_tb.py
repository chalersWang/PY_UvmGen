# import binascii
# -*-coding:UTF-8-*-

import sys
import gen_tb_dir
import CaptureTbInfo
#################################
# history
# v0.1 2022-01-29 wangxinxin
# generate stestbench dir
#################################

# ###if __name__=='__main__':
# ###    tb_name=input("Input your tb name:")
# ###    print("received tb name is:%s\n" %(tb_name))
# ###
# ###    tb_top_file=input("Input your top file with fullpath:")
# ###    print("received tb name is:%s\n" %(tb_top_file))
# ###
# ###   InArray=[]
# ###    novifArray=[]
# ###    module_name=''
# ###    CaptureTbInfo.main(tb_top_file,InArray,novifArray,module_name)
# ###    ##tb_name='rce_mu'
# ###   gen_tb_dir.main(tb_name,InArray,novifArray,module_name)
# ###    #print(InArray)


print("hello gen_tb")

if __name__ == '__main__':
    if len(sys.argv) == 0:
       sys.exit(1)

    arg_index = 1

    tb_name = ''          # #UT dir name:example rce_dma,rne_rccn
    tb_top_file = ''      # #dut top file:
    # ##extract information :from tb_top_file
    InArray = []          # #store vip name and signal:used for agent and tb_top
    novifArray = []       # #store signal not belong to vip interface:used for tb_top
    module_name = []      # #store dut name:used for tb_top

    while arg_index < len(sys.argv):
        arg = sys.argv[arg_index]
        if arg == "-infile":
            arg_index += 1
            tb_top_file = sys.argv[arg_index]
            arg_index += 1

        if arg == "-tbname":
            arg_index += 1
            tb_name = sys.argv[arg_index]
            arg_index += 1

    CaptureTbInfo.main(tb_top_file, InArray, novifArray, module_name)
    print("Show the module name in the gen_tb.py:")
    print(module_name)
    # #tb_name='rce_cmu'
    # gen_tb_dir.main(tb_name, InArray, novifArray, module_name)
    gen_tb_dir.main(tb_name, InArray, novifArray, module_name)
    # print(InArray)


