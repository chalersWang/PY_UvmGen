# import binascii
# -*-coding:UTF-8-*-

import os
# import sys

###################################################################################################
# history
# v0.1 2022-01-30 wangxinxin
# generate testbench/UT/env dir:all file
###################################################################################################


print("hello gen_env_file")


class gen_env_file:

    def __init__(self, tb_name, InArray, novifArray, module_name):
        self.tb_name = tb_name
        self.InArray = InArray
        self.novifArray = novifArray
        self.module_name = module_name
        self.local_dir = os.getcwd()

    def f_gen_env_event(self):
        print("gen env/%s_event.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name+"_event.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_EVENT_V_                                      \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_EVENT_V_                                      \n" % (self.tb_name.upper()))
        self.f_file.write("                                                          \n")
        self.f_file.write("class %s_event extends uvm_event_pool;                    \n" % self.tb_name)
        self.f_file.write("     uvm_event   evt_start;                               \n")
        self.f_file.write("     uvm_event   evt_end;                                 \n")
        self.f_file.write("     ////add here                                         \n")
        self.f_file.write("     `uvm_object_utils(%s_event)                          \n" % self.tb_name)
        self.f_file.write("                                                          \n")
        self.f_file.write("     function new(string name =\" %s_event\");            \n" % self.tb_name)
        self.f_file.write("         super.new(name);                                 \n")
        self.f_file.write("         evt_start=new();                                 \n")
        self.f_file.write("         evt_end=new();                                   \n")
        self.f_file.write("     endfunction                                          \n")
        self.f_file.write("endclass                                                  \n")
        self.f_file.write("`endif                                                    \n")

        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_config(self):
        print("gen env/%s_config.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name+"_config.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_CONFIG_V_                                        \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_CONFIG_V_                                        \n" % (self.tb_name.upper()))
        self.f_file.write("                                                             \n")
        self.f_file.write("class %s_config extends uvm_object;                          \n" % self.tb_name)
        self.f_file.write("     `uvm_object_utils_begin(%s_config)                      \n" % self.tb_name)
        self.f_file.write("     //`uvm_field_int(aa,UVM_ALL_ON)                         \n")
        self.f_file.write("     `uvm_object_utils_end                                   \n")
        self.f_file.write("                                                             \n")
        self.f_file.write("     function new(string name =\" %s_config\");               \n" % self.tb_name)
        self.f_file.write("         super.new(name);                                   s \n")
        self.f_file.write("     endfunction                                             \n")
        self.f_file.write("endclass                                                     \n")
        self.f_file.write("`endif                                                       \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_fcov(self):
        print("gen env/%s_function_coverage.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name+"_function_coverage.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_FUNCTION_COVERAGE_V_                              \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_FUNCTION_COVERAGE_V_                              \n" % (self.tb_name.upper()))
        self.f_file.write("                                                              \n")
#       ####up covergroup in function coverage by wangxx
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("covergroup %s_cg with function sample(%s_trans %s_tr);\n" % (self.InArray[index][0], self.InArray[index][0], self.InArray[index][0]))
                self.f_file.write("     //cov_1:coverpoint %s_tr.aa;                     \n" % (self.InArray[index][0]))
                self.f_file.write("     //cov_1:coverpoint %s_tr.bb;                     \n" % (self.InArray[index][0]))
                self.f_file.write("     //cross_1|:cross %s_tr.aa,%s_tr.bb;              \n" % (self.InArray[index][0], self.InArray[index][0]))
                self.f_file.write("endgroup                                              \n")
        self.f_file.write("                                                              \n")
        self.f_file.write("`endif                                                        \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_trans(self):
        print("gen env/%s_trans.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name+"_trans.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_TRANSACTION_V_                              \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_TRANSACTION_V_                              \n" % (self.tb_name.upper()))
        self.f_file.write("                                                        \n")
        self.f_file.write("class %s_trans extends uvm_sequence_item;               \n" % self.tb_name)
        self.f_file.write("     //example                                          \n")
        self.f_file.write("     rand logic[63:0] wght0[$];                         \n")
        self.f_file.write("     rand logic[71:0] data0[$];                         \n")
        self.f_file.write("                                                        \n")
        self.f_file.write("     `uvm_object_utils_begin(%s_trans)                  \n" % self.tb_name)
        self.f_file.write("     `uvm_object_utils_end                              \n")
        self.f_file.write("                                                        \n")
        self.f_file.write("     function new(string name =\" %s_event\");          \n" % self.tb_name)
        self.f_file.write("         super.new(name);                               \n")
        self.f_file.write("         extern function get_all_data(string path);     \n")
        self.f_file.write("     endfunction                                        \n")
        self.f_file.write("endclass                                                \n")
        self.f_file.write("                                                        \n")
        self.f_file.write("`endif                                                  \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_vseqr(self):
        print("gen env/%s_virtual_sequencer.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name + "_virtual_sequencer.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_VIRTUAL_SEQUENCER_V_                                     \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_VIRTUAL_SEQUENCER_V_                                     \n" % (self.tb_name.upper()))
        self.f_file.write("                                                                     \n")
        self.f_file.write("class %s_virtual_sequencer extends uvm_sequencer;                    \n" % self.tb_name)
#        ##up sequencer define in vseqr  by wangxx
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb':
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_%s_transaction_sequencer  %s_%s_seqr_%s;         \n" % (ahb_info[0], ahb_info[1], ahb_info[0], ahb_info[1], ahb_info[2]))
            if self.InArray[index][0][0:3] == 'axi':
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_%s_sequencer  %s_%s_seqr_%s;                     \n" % (axi_info[0], axi_info[1], axi_info[0], axi_info[1], axi_info[2]))
            if self.InArray[index][0][0:3] == 'apb':
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_%s_sequencer  %s_%s_seqr_%s;                     \n" % (apb_info[0], apb_info[1], apb_info[0], apb_info[1], apb_info[2]))
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_sequencer  %s_seqr;                                  \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
#        self.f_file.write("     %s_regmode   %s_rm;                 \n" %(self.tb_name, self.tb_name))
        self.f_file.write("     %s_config   %s_cfg;                                             \n" % (self.tb_name, self.tb_name))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     `uvm_component_utils_begin(%s_virtual_sequencer);               \n" % self.tb_name)
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb':
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         `uvm_field_object(%s_%s_serq_%s,UVM_ALL_ON);      \n" % (ahb_info[0], ahb_info[1], ahb_info[2]))
            if self.InArray[index][0][0:3] == 'axi':
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         `uvm_field_object(%s_%s_serq_%s,UVM_ALL_ON);      \n" % (axi_info[0], axi_info[1], axi_info[2]))
            if self.InArray[index][0][0:3] == 'apb':
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("         `uvm_field_object(%s_%s_serq_%s,UVM_ALL_ON);      \n" % (apb_info[0], apb_info[1], apb_info[2]))
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("         `uvm_field_object(%s_serq,UVM_ALL_ON);            \n" % (self.InArray[index][0]))
#        self.f_file.write("         `uvm_field_object(%s_rm,UVM_ALL_ON);                      \n" % self.tb_name)
        self.f_file.write("         `uvm_field_object(%s_cfg,UVM_ALL_ON);                     \n" % self.tb_name)
        self.f_file.write("     `uvm_component_utils_end                                      \n")
        self.f_file.write("                                                                   \n")
        self.f_file.write("     function new(string name =\" %s_virtual_sequencer\",uvm_component parent=null);\n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                                   \n")
        self.f_file.write("     endfunction                                                   \n")
        self.f_file.write("                                                                   \n")
        self.f_file.write("     virtual function void build_phase(uvm_phase phase);           \n")
        self.f_file.write("         supper.build_phase(parent);                               \n")
        self.f_file.write("     endfunction                                                   \n")
        self.f_file.write("endclass                                                           \n")
        self.f_file.write("                                                                   \n")
        self.f_file.write("`endif                                                             \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_scoreboard(self):
        print("gen env/%s_scoreboard.sv" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name + "_scoreboard.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_SCOREBOARD_V_                                            \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_SCOREBOARD_V_                                            \n" % (self.tb_name.upper()))
        self.f_file.write("                                                                     \n")
        self.f_file.write("`include \"%s_function_coverage.sv\";                                \n" % self.tb_name)
        self.f_file.write("class %s_scoreboard extends uvm_scoreboard;                          \n" % self.tb_name)

#        ##up interface in scoreboard by wangxx
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     typedef virtual %s_vif v_if%s;                          \n" % (self.InArray[index][0], index))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     v_if%s u_%s_vif;                                        \n" % (index, self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     %s_config   %s_cfg;                                             \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     %s_event   %s_evt;                                              \n" % (self.tb_name, self.tb_name))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     //%s_regmodel    %s_rm;                                         \n" % (self.tb_name, self.tb_name))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     uvm_tlm_analysis_fifo#(%s_trans)    %s_analysis_fifo;   \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_trans    %s_tr;                                      \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_cg    %s_cg;                                         \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")

        self.f_file.write("     uvm_status_e    status;                                         \n")
        self.f_file.write("     uvm_reg_data_t  value;                                          \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("     `uvm_component_utils_begin(%s_scoreboard);                      \n" % self.tb_name)
        self.f_file.write("     `uvm_component_utils_end;                                       \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("      extern function new(string name=\"%s_scoreboard\",uvm_component parent=null);\n" % self.tb_name)
        self.f_file.write("      ///extern function             build_phase(uvm_phase phase);   \n")
        self.f_file.write("      extern virtual task            reset_phase(uvm_phase phase);   \n")
        self.f_file.write("      extern virtual task            run_phase(uvm_phase phase);     \n")
        self.f_file.write("      extern virtual function void   report_phase(uvm_phase phase);  \n")
        self.f_file.write("      extern virtual task            init_data();                    \n")
        self.f_file.write("      extern virtual task            get_dut_data();                 \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("      ///add here all kind of task() to check DUT                    \n")
        self.f_file.write("endclass                                                             \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("function %s_scoreboard::new(string name=\"%s_scoreboard\",uvm_component parent=null);\n" % (self.tb_name, self.tb_name))
        self.f_file.write("      super.new(name,parent);                                        \n")
        self.f_file.write("      %s_cfg=new();                                                  \n" % self.tb_name)
        self.f_file.write("      %s_evt=new();                                                  \n" % self.tb_name)
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_analysis_fifo=new(\"%s_analysis_fifo\",this);        \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_tr=new();                                            \n" % (self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_cg=new();                                            \n" % (self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("endfunction                                                          \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("task %s_scoreboard::reset_phase(uvm_phase phase);                    \n" % self.tb_name)
        self.f_file.write("     super.reset_phase(phase)                                        \n")
        self.f_file.write("endtask                                                              \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("task %s_scoreboard::run_phase(uvm_phase phase);                      \n" % self.tb_name)
        self.f_file.write("     super.reset_phase(phase)                                        \n")
        self.f_file.write("     if(!uvm_config_db#(%s_event)::get(null,get_full_name(),\"%s_event\",%s_evt));\n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("         `uvm_fatal(get_type_name(),\"can\'t receive event object\") \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("     `uvm_info(get_type_name(),\"scoreboard main phase\",UVM_LOW)    \n")
        self.f_file.write("     init_data();                                                    \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("     fork                                                            \n")
        self.f_file.write("         get_dut_data();                                             \n")
        self.f_file.write("         ////add here:all kind of task                               \n")
        self.f_file.write("     join                                                            \n")
        self.f_file.write("endtask                                                              \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("function %s_scoreboard::report_phase(uvm_phase phase);               \n" % self.tb_name)
        self.f_file.write("     super.report_phase(phase)                                       \n")
        self.f_file.write("endtask                                                              \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("task %s_scoreboard::init_data();                                     \n" % self.tb_name)
        self.f_file.write("     uvm_config_db#(%s_config)::get(null,get_full_name(),\"%s_cfg\",%s_cfg); \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     uvm_config_db#(v_if%s)::get(this,\"\",\"%s_vif\",u_%s_vif);\n" % (index, self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     ////add initial code here                                       \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("endtask                                                              \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("task %s_scoreboard::get_dut_data();                                  \n" % self.tb_name)
        self.f_file.write("     forever begin                                                   \n")
        self.f_file.write("     uvm_config_db#(%s_config)::get(null,get_full_name(),\"%s_cfg\",%s_cfg); \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     uvm_config_db#(v_if%s)::get(this,\"\",\"%s_vif\",u_%s_vif);\n" % (index, self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     ////%s_evt.evt_start.wait_trigger();                            \n" % self.tb_name)
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_analysis_fifo.get(%s_tr);                            \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     ////add initial code                                            \n")
        self.f_file.write("     ////%s_evt.evt_end.trigger();                                   \n" % self.tb_name)
        self.f_file.write("                                                                     \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_cf.sample(%s_tr);                                    \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                     \n")
        self.f_file.write("     end                                                             \n")
        self.f_file.write("endtask                                                              \n")
        self.f_file.write("                                                                     \n")
        self.f_file.write("`endif                                                               \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_env(self):
        print("gen env/%s_env.sv" % self.tb_name)

        ahb_num = 0
        axi_num = 0
        apb_num = 0

        # has_regmodel = input("Whether has regmodel in this env ? (yes/no): ")
        has_regmodel = input("Whether has regmodel in this env ? (1:yes/0:no): ")

        os.chdir(self.local_dir)
        file_name = self.tb_name+"_env.sv"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_ENV_V_                                                               \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_ENV_V_                                                               \n" % (self.tb_name.upper()))
        self.f_file.write("                                                                                 \n")
        self.f_file.write("class %s_env extends uvm_env;                                                    \n" % self.tb_name)
        self.f_file.write("                                                                                 \n")
#        ## add vip agent/system_env in env by wangxx
        for index in range(len(self.InArray)):
            # print("********************************")
            # print(self.InArray[index])
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_system_env   %s_%s_env;                                      \n" % (ahb_info[0], ahb_info[0], ahb_info[1]))
                self.f_file.write("     %s_cust_config      %s_cfg;                                         \n" % (ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_system_env   %s_%s_env;                                      \n" % (axi_info[0], axi_info[0], axi_info[1]))
                self.f_file.write("     %s_cust_config      %s_cfg;                                         \n" % (axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and apb_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     svt_%s_system_env   %s_%s_env;                                      \n" % (apb_info[0], apb_info[0], apb_info[1]))
                self.f_file.write("     %s_cust_config      %s_cfg;                                         \n" % (apb_info[0], apb_info[0]))
                apb_num += 1
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_agent             %s_agt;                                        \n" % (self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     %s_scoreboard       %s_scb;                                                 \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     %s_config           %s_cfg;                                                 \n" % (self.tb_name, self.tb_name))
        self.f_file.write("     %s_event            %s_evt;                                                 \n" % (self.tb_name, self.tb_name))
        self.f_file.write("                                                                                 \n")
        # if has_regmodel == 'yes':
        if has_regmodel:
            self.f_file.write("     ral_block_%s_reg_top        regmodel;                                   \n" % self.tb_name)
            self.f_file.write("     string                      hdl_path;                                   \n")
        self.f_file.write("     %s_virtual_sequencer         %s_vseqr;                                      \n" % (self.tb_name, self.tb_name))
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     `uvm_component_utils(%s_env);                                               \n" % self.tb_name)
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     function new(string name =\" %s_env\",uvm_component parent=null);           \n" % self.tb_name)
        self.f_file.write("         super.new(name,parent);                                                 \n")
        self.f_file.write("     endfunction                                                                 \n")
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     extern virtual function void build_phase(uvm_phase phase);                  \n")
        self.f_file.write("     extern virtual function void connect_phase(uvm_phase phase);                \n")
        self.f_file.write("     extern virtual task          reset_phase(uvm_phase phase);                  \n")
        self.f_file.write("                                                                                 \n")
        self.f_file.write("endclass                                                                         \n")
        self.f_file.write("                                                                                 \n")
#        ####build_phase
        self.f_file.write("function void %s_env::build_phase(uvm_phase phase);                              \n" % self.tb_name)
        self.f_file.write("     super.new(phase);                                                           \n")
        self.f_file.write("                                                                                 \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_agt=%s_agent::type_id::create(\"%s_agt\",this);                  \n" % (self.InArray[index][0], self.InArray[index][0], self.InArray[index][0]))
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     %s_scb=%s_scoreboard::type_id::create(\"%s_scb\",this);                     \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("     %s_cfg=%s_config::type_id::create(\"%s_cfg\",this);                         \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("     %s_evt=%s_event::type_id::create(\"%s_evt\",this);                          \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("     %s_vseqr=%s_virtual_sequencer::type_id::create(\"%s_vseqr\",this);          \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("                                                                                 \n")
#        ## add vip config create in build_phase by wangxx
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("                                                                                 \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     /* Apply the configuration to the system ENV */                     \n")
                self.f_file.write("     %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this);            \n" % (ahb_info[0], ahb_info[0], ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     /* Apply the configuration to the system ENV */                     \n")
                self.f_file.write("     %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this);            \n" % (axi_info[0], axi_info[0], axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     /* Apply the configuration to the system ENV */                     \n")
                self.f_file.write("     %s_cfg=%s_cust_config::type_id::create(\"%s_cfg\",this);            \n" % (apb_info[0], apb_info[0], apb_info[0]))
                apb_num += 1
        self.f_file.write("                                                                                 \n")
        self.f_file.write("                                                                                 \n")
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("     /** construct the system agent **/                                          \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_%s_env=svt_%s_system_env::type_id::create(\"%s_%s_env\",this);   \n" % (ahb_info[0], ahb_info[1], ahb_info[0], ahb_info[0], ahb_info[1]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and axi_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_%s_env=svt_%s_system_env::type_id::create(\"%s_%s_env\",this);   \n" % (axi_info[0], axi_info[1], axi_info[0], axi_info[0], axi_info[1]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and axi_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_%s_env=svt_%s_system_env::type_id::create(\"%s_%s_env\",this);   \n" % (apb_info[0], apb_info[1], apb_info[0], apb_info[0], apb_info[1]))
                apb_num += 1
        self.f_file.write("                                                                                 \n")
        self.f_file.write("     uvm_config_db#(%s_config)::set(null,\"\",\"%s_configuration\",%s_cfg);      \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("     uvm_config_db#(%s_event)::set(null,\"\",\"%s_event\",%s_evt);               \n" % (self.tb_name, self.tb_name, self.tb_name))
        self.f_file.write("                                                                                 \n")
        # if has_regmodel == 'yes':
        if has_regmodel:
            self.f_file.write("     if(regmodel == null)                                                    \n")
            self.f_file.write("         begin                                                               \n")
            self.f_file.write("             uvm_reg::include_coverage(\"*\",UVM_CVR_ALL);                   \n")
            self.f_file.write("             regmodel = ral_block_%s_reg_top::type_id::create(\"regmodel\"); \n" % self.tb_name)
            self.f_file.write("             regmodel.build();                                               \n")
            self.f_file.write("             regmodel.set_hdl_path_root(hdl_path);                           \n")
            self.f_file.write("             regmodel.set_coverage(UVM_CVR_ALL);                             \n")
            self.f_file.write("             regmodel.lock_model();                                          \n")
            self.f_file.write("         end                                                                 \n")
            self.f_file.write("                                                                             \n")
            self.f_file.write("     uvm_config_db#(uvm_reg_block)::set(this, \"ahb_master_env.master[0]\", \"ahb_regmodel\", regmodel);\n")
        self.f_file.write("endfunction                                                                      \n")
        self.f_file.write("                                                                                 \n")
#        ####connect phase
        self.f_file.write("function void %s_env::connect_phase(uvm_phase phase);                            \n" % self.tb_name)
        self.f_file.write("     super.new(phase);                                                           \n")
        self.f_file.write("     //connect cfg port to rm                                                    \n")
        self.f_file.write("                                                                                 \n")
#        ## add agent connection in connect_phase by wangxx
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_agt.%s_mon.mon_analysis_port.connect(%s_scb.%s_analysis_fifo.analysis_export);\n" % (self.InArray[index][0], self.InArray[index][0], self.tb_name, self.InArray[index][0]))
        self.f_file.write("                                                                                 \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb':
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_vseqr.%s_%s_seqr_%s=%s_%s_env.%s[%s].sequencer; \n" % (self.tb_name, ahb_info[0], ahb_info[1], ahb_info[2], ahb_info[0], ahb_info[1], ahb_info[1], ahb_info[2]))
            if self.InArray[index][0][0:3] == 'axi':
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_vseqr.%s_%s_seqr_%s=%s_%s_env.%s[%s].sequencer; \n" % (self.tb_name, axi_info[0], axi_info[1], axi_info[2], axi_info[0], axi_info[1], axi_info[1], axi_info[2]))
            if self.InArray[index][0][0:3] == 'apb':
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     %s_vseqr.%s_%s_seqr_%s=%s_%s_env.%s[%s].sequencer; \n" % (self.tb_name, apb_info[0], apb_info[1], apb_info[2], apb_info[0], apb_info[1], apb_info[1], apb_info[2]))
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     %s_vseqr.%s_seqr=%s_agt.%s_seqr;                    \n" % (self.tb_name, self.InArray[index][0], self.InArray[index][0], self.InArray[index][0]))

        self.f_file.write("                                                                \n")
        self.f_file.write("endfunction                                                     \n")
        self.f_file.write("                                                                \n")
#        #### reset phase
        self.f_file.write("task %s_env::reset_phase(uvm_phase phase);                      \n" % self.tb_name)
        self.f_file.write("                                                                \n")
        # if has_regmodel == 'yes':
        if has_regmodel:
            self.f_file.write("     phase.raise_objection(this, \"Resetting regmodel\");   \n")
            self.f_file.write("     regmodel.reset();                                      \n")
            self.f_file.write("     phase.drop_objection(this);                            \n")
        self.f_file.write("                                                                \n")
        self.f_file.write("endtask                                                         \n")
        self.f_file.write("                                                                \n")
        self.f_file.write("`endif                                                          \n")
        self.f_file.close()
        os.chdir(self.local_dir)

    def f_gen_env_filelist(self):
        print("gen env/%s_EnvTop.svh" % self.tb_name)
        os.chdir(self.local_dir)
        file_name = self.tb_name + "_EnvTop.svh"
        self.f_file = open(file_name, "w+")

        self.f_file.write("`ifndef _%s_ENV_TOP_V_                                     \n" % (self.tb_name.upper()))
        self.f_file.write("`define _%s_ENV_TOP_V_                                     \n" % (self.tb_name.upper()))
        self.f_file.write("                                                           \n")
        self.f_file.write("`incluide \"uvm_macros.svh\"                               \n")
        self.f_file.write("                                                           \n")
        self.f_file.write("package %s_EnvTop;                                         \n" % self.tb_name)
        self.f_file.write("                                                           \n")
        self.f_file.write("     import uvm_pkg::*;                                    \n")
#        ###$add vip package import in EnvTop by wangxx
        self.f_file.write("     /** Import the SVT UVM Package  **/                   \n")
        self.f_file.write("     import svt_uvm_pkg::*;                                \n")
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("                                                           \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import svt_%s_uvm_pkg::*;                     \n" % (ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and ahb_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import svt_%s_uvm_pkg::*;                     \n" % (axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and ahb_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import svt_%s_uvm_pkg::*;                     \n" % (apb_info[0]))
                apb_num += 1
            if self.InArray[index][0][0:3] != 'ahb' and self.InArray[index][0][0:3] != 'axi' and self.InArray[index][0][0:3] != 'apb':
                self.f_file.write("     import %s_UvcTop::*;                          \n" % (self.InArray[index][0]))
        self.f_file.write("                                                           \n")
        ahb_num = 0
        axi_num = 0
        apb_num = 0
        self.f_file.write("                                                           \n")
        self.f_file.write("     /** Import the custom config and sequence about AHB/AXI VIP **/             \n")
        for index in range(len(self.InArray)):
            if self.InArray[index][0][0:3] == 'ahb' and ahb_num is 0:
                ahb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import %s_UvcTop::*;                          \n" % (ahb_info[0]))
                ahb_num += 1
            if self.InArray[index][0][0:3] == 'axi' and ahb_num is 0:
                axi_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import %s_UvcTop::*;                          \n" % (axi_info[0]))
                axi_num += 1
            if self.InArray[index][0][0:3] == 'apb' and ahb_num is 0:
                apb_info = self.InArray[index][0].split("#", 2)
                self.f_file.write("     import %s_UvcTop::*;                          \n" % (apb_info[0]))
                apb_num += 1
        self.f_file.write("                                                           \n")
        self.f_file.write("     typedef class %s_config;                              \n" % self.tb_name)
        self.f_file.write("     typedef class %s_event;                               \n" % self.tb_name)
        self.f_file.write("     typedef class %s_scoreboard;                          \n" % self.tb_name)
        self.f_file.write("     typedef class %s_virtual_sequencer;                   \n" % self.tb_name)
        self.f_file.write("     typedef class %s_env;                                 \n" % self.tb_name)
        self.f_file.write("                                                           \n")
        self.f_file.write("     `include \"../regmodel/%s_reg_top.sv\";               \n" % self.tb_name)
        self.f_file.write("     `include \"%s_config.sv\";                            \n" % self.tb_name)
        self.f_file.write("     `include \"%s_event.sv\";                             \n" % self.tb_name)
        self.f_file.write("     `include \"%s_scoreboard.sv\";                        \n" % self.tb_name)
        self.f_file.write("     `include \"%s_virtual_sequencer.sv\";                 \n" % self.tb_name)
        self.f_file.write("     `include \"%s_env.sv\";                               \n" % self.tb_name)
        self.f_file.write("                                                           \n")
        self.f_file.write("endpackage                                                 \n")
        self.f_file.write("                                                           \n")
        self.f_file.write("`endif                                                     \n")
        self.f_file.close()


def main(tb_name, InArray, novifArray, module_name):
    print("gen_env_file.main")
    g_tb_file = gen_env_file(tb_name, InArray, novifArray, module_name)
    g_tb_file.f_gen_env_env()
    g_tb_file.f_gen_env_scoreboard()
    g_tb_file.f_gen_env_vseqr()
#   g_tb_file.f_gen_env_trans()
    g_tb_file.f_gen_env_config()
    g_tb_file.f_gen_env_event()
    g_tb_file.f_gen_env_fcov()
    g_tb_file.f_gen_env_filelist()


if __name__ == '__main__':
    print("gen_env_file")
    tb_name = 'rce_cmu'
    main(tb_name)

####################################################################################
# add by wangxx 2022-02-08


# def main1(tb_name, InArray, novifArray, module_name):
#     print("gen_env_file.main")
#     g_tb_file = gen_env_file(tb_name, InArray, novifArray, module_name)
#     g_tb_file.f_gen_env_env()
#     g_tb_file.f_gen_env_scoreboard()
#     g_tb_file.f_gen_env_vseqr()
# #   g_tb_file.f_gen_env_trans()
#     g_tb_file.f_gen_env_config()
#     g_tb_file.f_gen_env_event()
#     g_tb_file.f_gen_env_fcov()
#     g_tb_file.f_gen_env_filelist()


# if __name__ == 'gen_env_file':
#     print("gen_env_file")
#     tb_name = 'rce_cmu'
#     InArray = []
#     novifArray = []
#     module_name = []
#     main(tb_name, InArray, novifArray, module_name)
