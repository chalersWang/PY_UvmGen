# import binascii
# -*-coding:UTF-8-*-

import os
import sys

###################################################################################################
#history
#v0.1 2022-01-29 wangxinxin
#generate testbench fileist
###################################################################################################

print("hello gen_tb_filelist")


class gen_tb_filelist:

    def __init__(self, tb_name, InArray, novifArray, module_name):
        self.tb_name = tb_name
        self.InArray = InArray
        self.novifArray = novifArray
        self.module_name = module_name
        self.local_dir = os.getcwd()

    def f_gen_tb_filelist(self):
            print("gen filist/%s_tb.f" %(self.tb_name))
            os.chdir(self.local_dir)
            file_name = "tb.f"
            self.f_file = open(file_name, "w+")
            self.f_file.write("+v2k                         \n")
            self.f_file.write("-sverilog                    \n")
            self.f_file.write("+incdir+$VER_HOME/regmodel   \n")
            self.f_file.write("+incdir+$VER_HOME/reference  \n")
            self.f_file.write("+incdir+$VER_HOME/env        \n")
            self.f_file.write("+incdir+$VER_HOME/sva        \n")
            self.f_file.write("+incdir+$VER_HOME/testcase   \n")

            ahb_num = 0
            axi_num = 0
            apb_num = 0
            self.f_file.write("\n")
            for index in range(len(self.InArray)):
                if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                    ahb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s               \n" % (ahb_info[0]))
                    ahb_num += 1
                if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                    axi_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s               \n" % (axi_info[0]))
                    axi_num += 1
                if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                    apb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s               \n" % (apb_info[0]))
                    apb_num += 1
                if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s               \n" % self.InArray[index][0])
            self.f_file.write("\n")
            ahb_num = 0
            axi_num = 0
            apb_num = 0
            self.f_file.write("\n")
            for index in range(len(self.InArray)):
                if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                    ahb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s/%s_UvcTop.svh \n" % (ahb_info[0], ahb_info[0]))
                    ahb_num += 1
                if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                    axi_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s/%s_UvcTop.svh \n" % (axi_info[0], axi_info[0]))
                    axi_num += 1
                if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                    apb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("+incdir+$VER_HOME/uvc/%s/%s_UvcTop.svh \n" % (apb_info[0], apb_info[0]))
                    apb_num += 1
                if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'apxi' and self.InArray[index][0][0:3] != 'apb':
                    self.f_file.write("$VER_HOME/uvc/%s/%s_vif.sv              \n" % (self.InArray[index][0], self.InArray[index][0]))
                    self.f_file.write("$VER_HOME/uvc/%s/%s_UvcTop.sv           \n" % (self.InArray[index][0], self.InArray[index][0]))

            self.f_file.write("$VER_HOME/env/%s_EnvTop.svh                     \n" % self.tb_name)
            self.f_file.write("$VER_HOME/testcase/%s_TestTop.svh               \n" % self.tb_name)
            self.f_file.write("$VER_HOME/tb/para_define.sv                     \n")
            self.f_file.write("$VER_HOME/tb/clock_gen.sv                       \n")
            self.f_file.write("$VER_HOME/tb/tb_top.sv                          \n")
            self.f_file.close()
            os.chdir(self.local_dir)

    def f_gen_cmodel_file(self):
        print("gen filist/cmodel.f")
        os.chdir(self.local_dir)
        file_name = "cmodel.f"
        self.f_file = open(file_name, "w+")
        self.f_file.write("//add cmodel lib file and cmodel file here if you want   \n")
        self.f_file.write("//../reference/%s_cmodel/lib_mu_wrapper.a                \n" % self.tb_name)
        self.f_file.write("//../reference/%s_cmodel/libsystemc.a                    \n" % self.tb_name)
        self.f_file.write("//../reference/%s_wrapper.c                              \n" % self.tb_name)
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_vip_file(self):
        print("gen filist/vip.f")
        os.chdir(self.local_dir)
        file_name = "vip.f"
        self.f_file = open(file_name, "w+")
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' or self.InArray[index][0][0:3] == 'axi' or self.InArray[index][0][0:3] == 'apb':
                if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                    self.f_file.write("//ahb vip setting and designware_home path                               \n")
                    self.f_file.write("+define+SVT_AHB_DISABLE_IMPLICIT_BUS_CONNECTIO                           \n")
                    self.f_file.write("+define+SVT_AHB_MAX_DATA_USER_WIDTH=32                                   \n")
                    self.f_file.write("+define+SVT_AHB_MAX_DATA_WIDTH=32                                        \n")
                    self.f_file.write("+define+SVT_AHB_MAX_ADDR_WIDTH=32                                        \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/ahb/lib/include/sverilog         \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/ahb/lib/src/sverilog/vcs         \n")
                    self.f_file.write("/network/project/public/uvm_vip/ahb/lib/include/sverilog/svt_ahb.uvm_pkg \n")
                    self.f_file.write("/network/project/public/uvm_vip/ahb/lib/include/sverilog/svt_ahb_if.svi  \n")
                    self.f_file.write("\n")
                    ahb_num += 1
                if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                    self.f_file.write("//axi vip setting and designware_home path                               \n")
                    self.f_file.write("+define+SVT_AXI_MAX_DATA_WIDTH=128                                       \n")
                    self.f_file.write("+define+SVT_AXI_MAX_ADDR_WIDTH=32                                        \n")
                    self.f_file.write("+define+SVT_AXI_MAX_BURST_LENGTH_WIDTH=4                                 \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/axi/lib/include/sverilog         \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/axi/lib/src/sverilog/vcs         \n")
                    self.f_file.write("/network/project/public/uvm_vip/axi/lib/include/sverilog/svt_ahb.uvm_pkg \n")
                    self.f_file.write("/network/project/public/uvm_vip/axi/lib/include/sverilog/svt_ahb_if.svi  \n")
                    self.f_file.write("\n")
                    axi_num += 1
                if self.InArray[index][0][0:3] == 'apb' and apb_num is 0:
                    self.f_file.write("//apb vip setting and designware_home path                               \n")
                    self.f_file.write("+define+SVT_APB_MAX_DATA_WIDTH=128                                       \n")
                    self.f_file.write("+define+SVT_APB_MAX_ADDR_WIDTH=32                                        \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/apb/lib/include/sverilog         \n")
                    self.f_file.write("+incdir+/network/project/public/uvm_vip/apb/lib/src/sverilog/vcs         \n")
                    self.f_file.write("/network/project/public/uvm_vip/apb/lib/include/sverilog/svt_ahb.uvm_pkg \n")
                    self.f_file.write("/network/project/public/uvm_vip/apb/lib/include/sverilog/svt_ahb_if.svi  \n")
                    self.f_file.write("\n")
                    apb_num += 1
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_asic_file(self):
        print("gen filist/asic.f")
        os.chdir(self.local_dir)
        file_name = "asic.f"
        self.f_file = open(file_name, "w+")
        self.f_file.write("//add define here if you want                                        \n")
        self.f_file.write("//+define+ASIC=1+                                                    \n")
        self.f_file.write("//+define+TSMC28HPCP                                                 \n")
        self.f_file.write("//+define+TSMC28HPCP=1+                                              \n")
        self.f_file.write("//+define+UNIT_DELAY                                                 \n")
        self.f_file.write("//+define+ASIC                                                       \n")
        self.f_file.write("//+define+MU_SIM                                                     \n")
        self.f_file.write("//+define+CU+TRACER                                                  \n")
        self.f_file.write("//+define+UVM_HDL_MAX_WIDTH=1300                                     \n")
        self.f_file.write("//+define+UVM_PACKAER_MAX_BYTES=1500000                              \n")
        self.f_file.write("//+define+UVM_DISABLE_AUTO_ITEM_RECORDING                            \n")
        self.f_file.write("//+define+SVT_UVM_TECHNOLOGY                                         \n")
        self.f_file.write("//+define+SYNOPSYS                                                   \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("-y /network/tools/synopsys/syn_vM-2016.12-SP3.old/dw/sim_ver         \n")
        self.f_file.write("+libext+.v+                                                          \n")
        self.f_file.write("+incdir /network/tools/synopsys/syn_vM-2016.12-SP3.old/dw/sim_ver    \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("//designe file should be modified                                    \n")
        self.f_file.write("//-f ${JIN_RTL}/../design.f                                          \n")
        self.f_file.write("-f ${VER_HOME}/filelist/vip.f                                        \n")
        self.f_file.write("-f ${VER_HOME}/filelist/tb.f                                         \n")
        self.f_file.write("-f ${VER_HOME}/filelist/cmodel.f                                     \n")
        self.f_file.close()
        os.chdir(self.local_dir)


def main(tb_name, InArray, novifArray, module_name):
    print("gen_tb_filelist.main")
    g_tb_filelist = gen_tb_filelist(tb_name, InArray, novifArray, module_name)
    g_tb_filelist.f_gen_tb_filelist()
    g_tb_filelist.f_gen_asic_file()
    g_tb_filelist.f_gen_vip_file()
    g_tb_filelist.f_gen_cmodel_file()


if __name__ == '__main__':
    print("gen_tb_filelist")
    tb_name = 'cmu'
    main(tb_name)

# ####################################################
# # add by wangxx at 2022-02-08
# if __name__ == 'gen_tb_filelist':
#     print("gen_tb_filelist")
#     tb_name = 'cmu'
#     InArray = []
#     novifArray = []
#     module_name = []
#     main(tb_name, InArray, novifArray, module_name)


