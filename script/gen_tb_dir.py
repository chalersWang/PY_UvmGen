# import binascii
# -*-coding:UTF-8-*-


import os
import gen_tb_filelist
import gen_env_file
import gen_vip_file
import gen_case_file
import gen_tb_file

###################################################################################################
# history
# v0.1 2022-01-29 wangxinxin
# generate testbench dir and uniform filename which has uniform class name
###################################################################################################

print("hello gen_tb_dir")


class gen_tb_dir:
    def __init__(self, tb_name, InArray, novifArray, module_name):
        self.tb_name = tb_name
        self.InArray = InArray
        self.novifArray = novifArray
        self.module_name = module_name
        self.local_dir = os.getcwd()
        # print(InArray)

    def f_gen_tb_dir(self):
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        # print(self.InArray)
        print('mkdir testbench of ' + self.tb_name + '\n')
        os.chdir(self.local_dir)
        print("************Current dir is : %s" % os.getcwd())
        if not os.path.isdir(self.tb_name):
            print('verification/' + self.tb_name + ' dir is created first')
            os.mkdir(self.tb_name)

        os.chdir(self.tb_name)
        print("************Current dir is : %s" % os.getcwd())
        print(self.tb_name)
        # ###reference
        if not os.path.isdir('reference'):
            print('verification/' + self.tb_name + '/reference dir is created')
            os.mkdir('reference')
        os.chdir('reference')
        print("************Current dir is : %s" % os.getcwd())
        print(self.tb_name)
#        if (not os.path.isfile('ReadMe.txt')):
#            self.f_file=open('ReadMe.txt',"w+")
#        self.f_file.write("the reference dir storer cmodel from tool-chain team")
#        self.f_file.close()

        os.chdir('./../')
        print('\n')
        if not os.path.isdir('env'):
            print('verification/' + self.tb_name + '/env dir is created')
            os.mkdir('env')
        os.chdir('env')
        print("************Current dir is : %s" % os.getcwd())
        gen_env_file.main(self.tb_name, self.InArray, self.novifArray, self.module_name)

        # ###reg model
        os.chdir('./../')
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('regmodel'):
            print('verification/' + self.tb_name + '/regmodel dir is created')
            os.mkdir('regmodel')

        # ####SVA
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('sva'):
            print('verification/' + self.tb_name + '/sva dir is created')
            os.mkdir('sva')
        
        # ####Coverage
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('coverage'):
            print('verification/' + self.tb_name + '/coverage dir is created')
            os.mkdir('coverage')

        # ######
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        # # add tcl and testpan dir by wangxx at 20220129
        if not os.path.isdir('tcl'):
            print('verification/' + self.tb_name + '/tcl dir is created')
            os.mkdir('tcl')
        if not os.path.isdir('testplan'):
            print('verification/' + self.tb_name + '/testplan dir is created')
            os.mkdir('testplan')
        if not os.path.isdir('filelist'):
            print('verification/' + self.tb_name + '/filelist dir is created')
            os.mkdir('filelist')
        os.chdir('filelist')
        print("************Current dir is : %s" % os.getcwd())
        gen_tb_filelist.main(self.tb_name, self.InArray, self.novifArray, self.module_name)
        # #######
        os.chdir('./../')
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('run'):
            print('verification/' + self.tb_name + '/run dir  is created')
            os.mkdir('run')
        os.chdir('run')
        print("************Current dir is : %s" % os.getcwd())

        # linux format
        # os.system('cp ../../../common/scrpt/bootenv/bootenv.sh ./../')
        # os.system('cp ../../../common/scrpt/srun/srun.py ./')
        # os.system('cp ../../../common/scrpt/srun/list_regress.py ./')

        # windows format
        os.system('cp ..\..\..\common\script\\bootenv\\bootenv.sh .\..')
        os.system('cp ..\..\..\common\script\srun\srun.py .')
        os.system('cp ..\..\..\common\script\srun\list_regress.py .')

        # ###########testbench top
        os.chdir('./../')
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('tb'):
            print('verification/' + self.tb_name + '/tb dir  is created')
            os.mkdir('tb')
        os.chdir('tb')
        print("************Current dir is : %s" % os.getcwd())
        gen_tb_file.main(self.tb_name, self.InArray, self.novifArray, self.module_name)
        # ###########testcase dir
        os.chdir('./../')
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('testcase'):
            print('verification/' + self.tb_name + '/testcase dir  is created')
            os.mkdir('testcase')
        os.chdir('testcase')
        print("************Current dir is : %s" % os.getcwd())
        gen_case_file.main(self.tb_name, self.InArray)

#        file_name=self.tb_name + 'base_test.sv'
#            self.f_file=open(file_name,"w+")
#            self.f_file.write("class %s_base_test extends uvm_test\n" %(self.tb_name))
#            self.f_file.write("     %s_env env;\n" %(self.tb_name))
#            self.f_file.write("endclass:%s_base_test" %(self.tb_name))
#            self.f_file.close()

        # ##########UVM component
        os.chdir('./../')
        print("************Current dir is : %s" % os.getcwd())
        print('\n')
        if not os.path.isdir('uvc'):
            print('verification/' + self.tb_name + '/uvc dir  is created')
            os.mkdir('uvc')
        os.chdir('uvc')
        print("************Current dir is : %s" % os.getcwd())
        gen_vip_file.main(self.tb_name, self.InArray, self.novifArray, self.module_name)

#        self.f_file=open(VipReadMe.txt,"w+")
#        self.f_file.write("The dir store all vips,according to interface of dut\n")
#        self.f_file.close()

#        os.mkdir('xxx_vip')
#        os.chdir('xxx_vip')
#        array_vip=['agent','vif','monr','dvr','seqr','trans']
#        for i in range(len(array_vip)):
#            file_name=self.tb_name + '_xxx_'+arrray_vip[i].sv
#            self.f_file=open(file_name,"w+")
#            self.f_file.close()

        os.chdir(self.local_dir)

    def f_gen_dir(self):
        self.f_gen_tb_dir()


def main(tb_name, InArray, novifArray, module_name):
    # def main():
    print("gen_tb_dir.main")
    g_dir = gen_tb_dir(tb_name, InArray, novifArray, module_name)
    g_dir.f_gen_dir()


if __name__ == '__main__':
    print("gen_tb_dir")
    tb_name = 'rce_cmu'
    main(tb_name)

# ####################################################
# # add by wangxx at 2022-02-08
#
#
# # ef main(tb_name, InArray, novifArray, module_name):
# #    print("gen_tb_dir.main")
# #    g_dir = gen_tb_dir(tb_name, InArray, novifArray, module_name)
# #    g_dir.f_gen_dir()
#
#
# if __name__ == 'gen_tb_dir':
#     print("gen_tb_dir")
#     tb_name = 'rce_cmu'
#     InArray = []
#     novifArray = []
#     module_name = []
#     main(tb_name, InArray, novifArray, module_name)

