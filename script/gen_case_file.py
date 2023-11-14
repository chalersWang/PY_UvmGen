# import binascii
# -*-coding:UTF-8-*-

import os
import sys

###################################################################################################
# history
# v0.1 2022-01-29 wangxinxin
# generate testbench/testcase dir :all test case and sequece
###################################################################################################

print("hello gen_case_file")


class gen_case_file:

    def __init__(self,tb_name,InArray):
        self.tb_name = tb_name
        self.InArray = InArray
        self.local_dir = os.getcwd()

    def f_gen_case_examplecase(self):
        print("gen testcase/%s_example_test.sv" % self.tb_name)
        # os.chdir(self.local_dir)
        file_name = self.tb_name+'_example_test.sv'
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_TESTCASE_V_                                      \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_TESTCASE_V_                                      \n" % (self.tb_name.upper()))

        self.f_file.write("class %s_example_seq extends %s_virtual_seq_lib;             \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     uvm_status_e    status;                                 \n")
        self.f_file.write("     uvm_reg_data_t  value;                                  \n")
        self.f_file.write("     constraint xxx_cst{                                     \n")
        self.f_file.write("         xxx=='h0                                            \n")
        self.f_file.write("     }                                                       \n")
        self.f_file.write("     `uvm_object_utils(%s_example_seq)                       \n" % self.tb_name)
        self.f_file.write("     function new(string name =\" %s_example_seq\");         \n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                             \n")
        self.f_file.write("     endfunction                                             \n")
        self.f_file.write("     virtual task body();                                    \n")
        self.f_file.write("         `uvm_info(get_full_name(),\"pre_body\",UVM_LOW)     \n")
        self.f_file.write("         ////add here                                        \n")
        self.f_file.write("         #2000;                                              \n")
        self.f_file.write("     endtask                                                 \n")
        self.f_file.write("endclass                                                     \n")
        self.f_file.write("\n\n\n")

        self.f_file.write("class %s_example_test extends %s_base_test;                  \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     `uvm_component_utils(%s_example_test)                   \n" % self.tb_name)
        self.f_file.write("     function new(string name =\" %s_virtual_example_test\",uvm_component parent=null);\n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                             \n")
        self.f_file.write("     endfunction                                             \n")
        self.f_file.write("     virtual function void build_phase(uvm_phase phase);     \n")
        self.f_file.write("         supper.build_phase(parent);                         \n")
        self.f_file.write("         uvm_config_db#(uvm_object_wrapper)::set(this,\"env.%s_vseqr.main_phase\",\"default_sequence\",%s_example_seq::type_id::get());\n" %(self.tb_name,self.tb_name))
        self.f_file.write("         `uvm_info(get_type_name(),\"config default sequence end\",UVM_LOW)     \n")
        self.f_file.write("     endfunction                                             \n")
        self.f_file.write("endclass                                                     \n")

        self.f_file.write("`endif                                                       \n")
        self.f_file.close()

    def f_gen_case_basecase(self):
        print("gen %s_base_test.sv" % self.tb_name)
        # os.chdir(self.local_dir)
        file_name = self.tb_name+'_base_test.sv'
        self.f_file = open(file_name, "w+")

        ahb_num = 0
        axi_num = 0
        apb_num = 0

        # has_regmodel = input("Whether has regmodel in this env ? (yes/no): ")
        has_regmodel = input("Whether has regmodel in this env ? (1:yes/0:no): ")

        self.f_file.write("`ifndef _%s_BASE_TEST_V_                                     \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_BASE_TEST_V_                                     \n" % (self.tb_name.upper()))

        self.f_file.write("class %s_base_test extends uvm_test;                         \n" % self.tb_name)
        self.f_file.write("     %s_env      env;                                        \n" % self.tb_name)
        self.f_file.write("     `uvm_component_utils(%s_base_test)                      \n" % self.tb_name)
        self.f_file.write("     uvm_event   event_start;                                \n")

        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     virtual %s_vif %s_if;                            \n" % (self.tb_name, self.tb_name))

        self.f_file.write("     %s_config   %s_cfg;                                     \n" % (self.tb_name, self.tb_name))

        # if has_regmodel == 'yes':
        if has_regmodel:
            self.f_file.write("     ral_block_%s_reg_top    RM;                         \n" % self.tb_name)

        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_cust_config  %s_cfg;                         \n" % (ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_cust_config  %s_cfg;                         \n" % (axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_cust_config  %s_cfg;                         \n" % (apb_info[0], apb_info[0]))
                apb_num += 1

        self.f_file.write("        ////add here                                         \n")
        self.f_file.write("     function new(string name =\" %s_base_test\",uvm_component parent=null);\n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                             \n")
        self.f_file.write("     endfunction                                             \n")
        self.f_file.write("     virtual function void build_phase(uvm_phase phase);     \n")
        self.f_file.write("         supper.build_phase(parent);                         \n")
        self.f_file.write("         env=%s_env::type_id::create(\"env\",this);          \n" % self.tb_name)
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this); \n" % (ahb_info[0], ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this); \n" % (axi_info[0], axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and apb_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this); \n" % (apb_info[0], apb_info[0], apb_info[0]))
                apb_num += 1

        self.f_file.write("         %scfg=%s_config::type_id:create(\"%s_cfg\",this);                 \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("         void'(%s_cfg.randomize());                                        \n" % self.tb_name)
        self.f_file.write("                                                                             \n")
        self.f_file.write("         uvm_config_db#(%s_config)::set(this,\"*\",\"%s_cfg\",%s_cfg); \n" % (self.tb_name, self.tb_name, self.tb_name))

        ahb_num=0
        axi_num=0
        apb_num=0

        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         uvm_config_db#(svt_%s_system_configuration)::set(this,\"env.%s_%s_env\",\"cfg\",%s_cfg.%s_cfg); \n" % (ahb_info[0], ahb_info[0], ahb_info[1], ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         uvm_config_db#(svt_%s_system_configuration)::set(this,\"env.%s_%s_env\",\"cfg\",%s_cfg.%s_cfg); \n" % (axi_info[0], axi_info[0], axi_info[1], axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and apb_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         uvm_config_db#(svt_%s_system_configuration)::set(this,\"env.%s_%s_env\",\"cfg\",%s_cfg.%s_cfg); \n" % (apb_info[0], apb_info[0], apb_info[1], apb_info[0], apb_info[0]))
                apb_num += 1
        self.f_file.write("                                                                             \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("         uvm_config_db#(virtual %s_vif)::get(this,\"\",\"%s_vif\",%s_if); \n" % (self.InArray[index][0], self.InArray[index][0], self.InArray[index][0]))

        self.f_file.write("                                                                             \n")
        self.f_file.write("     endfunction                                                             \n")

        self.f_file.write("     virtual task run_phase(uvm_phase phase);                                \n")
        # if has_regmodel == 'yes':
        if has_regmodel:
            self.f_file.write("     RM=env.regmodel;                                                    \n")
        self.f_file.write("         super.run_phase(parent);                                            \n")
        self.f_file.write("         phase.raise_objection(this);                                        \n")
        self.f_file.write("         fork                                                                \n")
        self.f_file.write("         ////add here                                                        \n")
        self.f_file.write("         join                                                                \n")
        self.f_file.write("         phase.drop_objection(this);                                         \n")
        self.f_file.write("     endtask                                                                 \n")

        self.f_file.write("     virtual task main_phase(uvm_phase phase);                               \n")
        self.f_file.write("         super.main_phase(parent);                                           \n")
        self.f_file.write("         phase.phase_done.set_drain_time(this,4000);                         \n")
        self.f_file.write("         ////add here                                                        \n")
        self.f_file.write("     endtask                                                                 \n")

        self.f_file.write("     virtual function void extract_phase(uvm_phase phase);                   \n")
        self.f_file.write("         ////add here                                                        \n")
        self.f_file.write("     endtfunction                                                            \n")

        self.f_file.write("     virtual function void report_phase(uvm_phase phase);                    \n")
        self.f_file.write("         uvm_report_sever    sever;                                          \n")
        self.f_file.write("         int                 err_num;                                        \n")
        self.f_file.write("         super.report_phase(parent);                                         \n")
        self.f_file.write("         server=get_report_server();                                         \n")
        self.f_file.write("         if(err_num==0)                                                      \n")
        self.f_file.write("             `uvm_info(get_type_name(),\"===UVM_TEST_PASSED===\",UVM_NONE)   \n")
        self.f_file.write("         else                                                                \n")
        self.f_file.write("             `uvm_error(get_type_name(),\"===UVM_TEST_FAILED==\")            \n")
        self.f_file.write("     endfunction                                                             \n")

        self.f_file.write("     endfclass                                                               \n")
        self.f_file.write("`endif                                                                       \n")
        self.f_file.close()

    def f_gen_case_seqlib(self):
        print("gen %s_sequence_lib.sv" % self.tb_name)
        # os.chdir(self.local_dir)
        file_name = self.tb_name+'_sequence_lib.sv'
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_SEQUENCE_LIB_V_                                                  \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_SEQUENCE_LIB_V_                                                  \n" % (self.tb_name.upper()))

        self.f_file.write("class %s_virtual_seq_lib extends uvm_sequence;                               \n" % self.tb_name)
        self.f_file.write("     %s_event   %s_evt;                                                      \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     %s_config  %s_cfg;                                                      \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     ////add here                                                            \n")
        self.f_file.write("     //typedef virtual %s_vif  %s_if                                         \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     //v_if  %s_vif                                                          \n" % self.tb_name)
        self.f_file.write("     `uvm_object_utils_begin(%s_virtual_seq_lib)                             \n" % self.tb_name)
        self.f_file.write("     `uvm_object_utils_end                                                   \n")

        self.f_file.write("     function new(string name =\" %s_virtual_seq_lib\");                     \n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                                             \n")
        self.f_file.write("         %s_cfg=new();                                                       \n" % self.tb_name)
        self.f_file.write("         uvm_config_db#(%s_event)::set::(null,\"*\",\"%s_event\",%s_evt);    \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("         uvm_config_db#(%s_config)::set::(null,\"*\",\"%s_config\",%s_cfg);  \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("     endfunction                                                             \n")

        self.f_file.write("     virtual task pre_body();                                                \n")
        self.f_file.write("         `uvm_info(get_full_name(),\"pre_body\",UVM_LOW)                     \n")
        self.f_file.write("         if(starting_phase!=null)                                            \n")
        self.f_file.write("             starting_phase.raise_objection(this,\"virtual sequence finished\");  \n")
        self.f_file.write("         if(!uvm_config_db#(%s_event)::get(null,get_full_name(),\"%s_event\",%s_evt))   \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("             `uvm_fatal(get_type_name(),\"can not get event object\")        \n")
        self.f_file.write("         ////wait(%s_if.rst);                                                \n" % self.tb_name)
        self.f_file.write("         #2000;                                                              \n")
        self.f_file.write("     endtask                                                                 \n")

        self.f_file.write("     virtual task postbody();                                                \n")
        self.f_file.write("         `uvm_info(get_full_name(),\"post_body\",UVM_LOW)                    \n")
        self.f_file.write("         #2000;                                                              \n")
        self.f_file.write("         if(starting_phase!=null)                                            \n")
        self.f_file.write("             starting_phase.drop_objection(this,\"virtual sequence finished\");   \n")
        self.f_file.write("     endtask                                                                 \n")

        self.f_file.write("     endfclass                                                               \n")
        self.f_file.write("`endif                                                                       \n")
        self.f_file.close()

    def f_gen_caselist_file(self):
            print("gen testcase/%s_TestTop.svh" % self.tb_name)
            # os.chdir(self.local_dir)
            file_name = self.tb_name + '_TestTop.svh'
            self.f_file = open(file_name, "w+")

            self.f_file.write("`ifndef _%s_TEST_TOP_V_                                                  \n" % (self.tb_name.upper()))
            self.f_file.write("`define _%s_TEST_TOP_V_                                                  \n" % (self.tb_name.upper()))

            self.f_file.write("package %s_TestTop;                                                      \n" % self.tb_name)
            self.f_file.write("import uvm_pkg::*;                                                       \n")
            self.f_file.write("//import the SVT UVM PKG                                                 \n")
            self.f_file.write("import svt_uvm_pkg::*;                                                   \n")
            self.f_file.write("//import the SVT VIP PKG                                                 \n")

            ahb_num = 0
            axi_num = 0
            apb_num = 0
            for index in range(len(self.InArray)):
                if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                    ahb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import svt_%s_uvm_pkg::*;                                   \n" % ahb_info[0])
                    ahb_num += 1
                if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                    axi_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import svt_%s_uvm_pkg::*;                                   \n" % axi_info[0])
                    axi_num += 1
                if self.InArray[index][0][0:3] == 'apb' and apb_num is 0:
                    apb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import svt_%s_uvm_pkg::*;                                   \n" % apb_info[0])
                    apb_num += 1
            self.f_file.write("                                                                         \n")
            ahb_num = 0
            axi_num = 0
            apb_num = 0
            for index in range(len(self.InArray)):
                if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                    ahb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import %s_UvcTop::*;                                        \n" % (ahb_info[0]))
                    ahb_num += 1
                if self.InArray[index][0][0:3] == 'axi' and ahb_num is 0:
                    axi_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import %s_UvcTop::*;                                        \n" % (axi_info[0]))
                    axi_num += 1
                if self.InArray[index][0][0:3] == 'apb' and ahb_num is 0:
                    apb_info = self.InArray[index][0].split("#", 2)
                    self.f_file.write("     import %s_UvcTop::*;                                        \n" % (apb_info[0]))
                    apb_num += 1
                if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                    self.f_file.write("     import %s_UvcTop::*;                                        \n" % self.InArray[index][0])
            self.f_file.write("                                                                         \n")
            self.f_file.write("     import %s_EnvTop::*;                                                \n" % self.tb_name)
            self.f_file.write("     `include \"%s_base_test.sv\";                                       \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_sequence_lib.sv\";                                  \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_example_case.sv\";                                  \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_function_case1.sv\";                                \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_function_case2.sv\";                                \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_function_case3.sv\";                                \n" % self.tb_name)
            self.f_file.write("     //`include \"%s_function_case4.sv\";                                \n" % self.tb_name)
            self.f_file.write("endpackage                                                               \n")
            self.f_file.write("`endif                                                                   \n")
            self.f_file.close()


def main(tb_name, InArray):
    print("gen_case_file.main")
    g_case_file = gen_case_file(tb_name, InArray)
    g_case_file.f_gen_case_seqlib()
    g_case_file.f_gen_case_basecase()
    g_case_file.f_gen_case_examplecase()
    g_case_file.f_gen_caselist_file()


if __name__ == '__main__':
    print("gen_case_file")
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
# if __name__ == 'gen_case_file':
#     print("gen_case_file")
#     tb_name = 'rce_cmu'
#     InArray = []
#     main(tb_name, InArray)





