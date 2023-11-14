# import binascii
# -*-coding:UTF-8-*-

import os
import sys

###################################################################################################
# history
# v0.1 2022-01-29 wangxinxin
# generate testbench/tb dir:all file
###################################################################################################

print("hello gen_tb_file")


class gen_tb_file:

    def __init__(self, tb_name, InArray, novifArray, module_name):
        self.tb_name = tb_name
        self.InArray = InArray
        self.novifArray = novifArray
        self.module_name = module_name
        self.local_dir = os.getcwd()

    def f_gen_para_define(self):
        print('gen tb/para_deine.sv')
        os.chdir(self.local_dir)
        file_name = "para_define.sv"
        self.f_file = open(file_name, "w+")
        self.f_file.write("`define AXI_MID_W_D      4                       \n")
        self.f_file.write("`define CLK_FREQ_122M    8.138  //122.88M        \n")
        self.f_file.write("`define CLK_FREQ_1PARA1  8.138  //122.88M        \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_clock_gen(self):
        print('gen tb/clock_gen.sv')
        os.chdir(self.local_dir)
        file_name = "clock_gen.sv"
        self.f_file = open(file_name, "w+")
        self.f_file.write("module clock_gen#(DEFAULT_PERIOD=10)(output bit clk)     \n")
        self.f_file.write("     real clk_period;                                    \n")
        self.f_file.write("     int start;                                          \n")
        self.f_file.write("     initial begin                                       \n")
        self.f_file.write("             clk_period=DEFAULT_PERIOD;                  \n")
        self.f_file.write("             clk=0;                                      \n")
        self.f_file.write("             #1;                                         \n")
        self.f_file.write("             //start=({$random}%($rtoi(clk_period)))     \n")
        self.f_file.write("             //#start;                                   \n")
        self.f_file.write("             forever begin                               \n")
        self.f_file.write("                     #(clk_period/2.0)clk=~clk;          \n")
        self.f_file.write("                     end                                 \n")
        self.f_file.write("             end                                         \n")
        self.f_file.write("endmodule                                                \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_tb_top(self):
        print('gen tb/tb_top.sv')
        os.chdir(self.local_dir)

        file_name = "tb_top.sv"
        self.f_file = open(file_name, "w+")
        self.f_file.write("module tb_top;                                           \n")
        self.f_file.write("     import uvm_pkg::*;                                  \n")
        self.f_file.write("     import svt_uvm_pkg::*;                              \n")

        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                self.f_file.write("     import svt_ahb_uvm_pkg::*;                  \n")
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and ahb_num is 0:
                self.f_file.write("     import svt_axi_uvm_pkg::*;                  \n")
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and ahb_num is 0:
                self.f_file.write("     import svt_apb_uvm_pkg::*;                  \n")
                apb_num += 1

        self.f_file.write("     import %s_TestTop::*;                               \n" % self.tb_name)
        self.f_file.write("     wire clk;                                           \n")
        self.f_file.write("     reg  rst_n;                                         \n")
        self.f_file.write("     clock_gen #(`CLK_PERIOD_PARA1) u_clk (.clk(clk));   \n")

        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_if %s_vip_if();                      \n" % (ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_if %s_vip_if();                      \n" % (axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_if %s_vip_if();                      \n" % (apb_info[0], apb_info[0]))
                apb_num += 1

        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     typedef virtual %s_vif v_if%s;              \n" % (self.InArray[index][0], index))
        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_vif u_%s_vif(tb_top.clk,tb_top.rst_n);   \n" % (self.InArray[index][0], self.InArray[index][0]))

        self.f_file.write("\n")
        self.f_file.write("     %s DUT (\n" % self.module_name[0])
        # self.f_file.write("     %s DUT (\n" % self.module_name)     # add by wangxx at 2022-02-08 20:15
        self.f_file.write("\n")
        for i in range(len(self.novifArray)):
            if self.novifArray[i].split()[-1] == ',':
                signal = self.novifArray[i].split()[-2]
            else:
                signal = self.novifArray[i].split()[-1].strip(',')
            self.f_file.write("     .%s (%s),                     \n" % (signal, signal))
        self.f_file.write("\n")
        for i in range(len(self.InArray)):
            for j in range(len(self.InArray[i])-1):
                if self.InArray[i][j+1].split()[-1] == ',':
                    signal = self.InArray[i][j+1].split()[-2]
                else:
                    signal = self.InArray[i][j+1].split()[-1].strip(',')
                # #add vip virtual interface
                if self.InArray[i][0][0:3] == 'ahb':
                    ahb_info = self.InArray[i][0].split("#", 2)
                    self.f_file.write("     .%s (%s_vip_if.%s_if[%s].%s),       \n" % (signal, ahb_info[0], ahb_info[1], ahb_info[2], signal))
                if self.InArray[i][0][0:3] == 'axi':
                    axi_info = self.InArray[i][0].split("#", 2)
                    self.f_file.write("     .%s (%s_vip_if.%s_if[%s].%s),       \n" % (signal, axi_info[0], axi_info[1], axi_info[2], signal))
                if self.InArray[i][0][0:3] == 'apb':
                    apb_info = self.InArray[i][0].split("#", 2)
                    self.f_file.write("     .%s (%s_vip_if.%s_if[%s].%s),       \n" % (signal, apb_info[0], apb_info[1], apb_info[2], signal))
                if self.InArray[i][0][0:3] != 'ahb' and self.InArray[i][0][0:3] != 'axi' and self.InArray[i][0][0:3] != 'apb' :
                    self.f_file.write("     .%s (u_%s_vif.%s),                  \n" % (signal, self.InArray[i][0], signal))
            self.f_file.write("\n")
        self.f_file.write(" );//DUT inst                                        \n")

        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb':
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     assign %s_vip_if.hresetn=hrst_n;               \n" % (ahb_info[0]))
                self.f_file.write("     assign %s_vip_if.hclk=hclk;                    \n" % (ahb_info[0]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].hresetn=hrst_n;     \n" % (ahb_info[0], ahb_info[1], ahb_info[2]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].hclk=hclk;          \n" % (ahb_info[0], ahb_info[1], ahb_info[2]))
            if self.InArray[index][0][0:3] == 'apb':
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     assign %s_vip_if.presetn=prst_n;               \n" % (apb_info[0]))
                self.f_file.write("     assign %s_vip_if.pclk=pclk;                    \n" % (apb_info[0]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].presetn=prst_n;     \n" % (apb_info[0], apb_info[1], apb_info[2]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].pclk=pclk;          \n" % (apb_info[0], apb_info[1], apb_info[2]))
            if self.InArray[index][0][0:3] == 'axi':
                axi_info = self.InArray[index][0].split("#", 2)
                # self.f_file.write("     assign %s_vip_if.aresetn=arst_n;               \n" %(axi_info[0]))
                self.f_file.write("     assign %s_vip_if.aclk=aclk;                     \n" % (axi_info[0]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].aresetn=arst_n;      \n" % (axi_info[0], axi_info[1], axi_info[2]))
                self.f_file.write("     assign %s_vip_if.%s_if[%s].aclk=aclk;           \n" % (axi_info[0], axi_info[1], axi_info[2]))

        self.f_file.write("\n")

        self.f_file.write("     initial begin                                                   \n")
        self.f_file.write("             rst_n=1'b0;                                             \n")
        self.f_file.write("             fork    begin                                           \n")
        self.f_file.write("                     repeat(2)@(posedge clk);                        \n")
        self.f_file.write("                     rst_n=1'b1;                                     \n")
        self.f_file.write("                     $display(\"%0d ns rst_n release ...\",$time)    \n")
        self.f_file.write("                     end                                             \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("                     begin                                           \n")
        self.f_file.write("                     end                                             \n")
        self.f_file.write("             join                                                    \n")
        self.f_file.write("             end                                                     \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("     initial begin                                                   \n")
        self.f_file.write("             //#1;                                                   \n")

        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("\n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     uvm_config_db#(virtual svt_%s_if)::set(null,\"*\",\"vif\",%s_vip_if;) \n" % (ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     uvm_config_db#(virtual svt_%s_if)::set(null,\"*\",\"vif\",%s_vip_if;) \n" % (axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     uvm_config_db#(virtual svt_%s_if)::set(null,\"*\",\"vif\",%s_vip_if;) \n" % (apb_info[0], apb_info[0]))
                apb_num += 1
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'apxi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     //uvm_config_db#(v_if%s)::set(null,\"uvm_test_top.env.u_%s_agent\",\"%s_vif\",u_%s_vif;) \n" % (index, self.InArray[index][0], self.InArray[index][0], self.InArray[index][0]))
                self.f_file.write("     uvm_config_db#(v_if%s)::set(null,\"*\",\"%s_vif\",u_%s_vif;) \n" % (index, self.InArray[index][0], self.InArray[index][0]))
            self.f_file.write("\n")
        self.f_file.write("     run_test();     \n")
        self.f_file.write("     end\n")

        # #######dump wave form
        self.f_file.write("///// dump vpd,later add start end time para             \n")
        self.f_file.write("reg[1023:0] vpdfile;                                     \n")
        self.f_file.write("initial  begin                                           \n")
        self.f_file.write("         if($value$plusargs(\"VPDNAME=%S\",vpdfile))     \n")
        self.f_file.write("             begin                                       \n")
        self.f_file.write("             $vcdplufile(vpdfile);                       \n")
        self.f_file.write("             $vcdpluson();                               \n")
        self.f_file.write("             end                                         \n")
        self.f_file.write("         end                                             \n")
        self.f_file.write("                                                         \n")

        self.f_file.write("///// dump fsdb                                          \n")
        self.f_file.write("reg[1023:0] fsdb_file;                                   \n")
        self.f_file.write("initial  begin                                           \n")
        self.f_file.write("         if($value$plusargs(\"FSDBNAME=%S\",fsdb_file))  \n")
        self.f_file.write("             begin                                       \n")
        self.f_file.write("             $fsdbDumpfile(fsdb_file);                   \n")
        self.f_file.write("             $fsdbDumpvars(0);                           \n")
        self.f_file.write("             //$fsdbDumpoff();                           \n")
        self.f_file.write("             $fsdbDumpon();                              \n")
        self.f_file.write("             end                                         \n")
        self.f_file.write("         end                                             \n")
        self.f_file.write("                                                         \n")

        self.f_file.write("endmodule                                                \n")
        self.f_file.close()
        os.chdir(self.local_dir)


def main(tb_name, InArray, novifArray, module_name):
    print("gen_tb_file.main")
    g_tb_file = gen_tb_file(tb_name, InArray, novifArray, module_name)
    g_tb_file.f_gen_tb_top()
    g_tb_file.f_gen_clock_gen()
    g_tb_file.f_gen_para_define()


if __name__ == '__main__':
    print("gen_tb_file")
    tb_name = 'cmu'
    main(tb_name)


# ####################################################
# # add by wangxx at 2022-02-08
# if __name__ == 'gen_tb_file':
#     print("gen_tb_file")
#     tb_name = 'cmu'
#     InArray = []
#     novifArray = []
#     module_name = []
#     main(tb_name, InArray, novifArray, module_name)

