# import binascii
# -*-coding:UTF-8-*-

import sys
import os
import getopt
import datetime
import random
from optparse import OptionParser

# #-debug_access+nomemcbk+dmptf -debug_region+cell instead -PP
# #comp_args = """vcs -lca -full64 -partcomp=autoopart_low \
comp_args = """  \
vcs -lca -full64 \
-Marchive=2000      \
-no_error ZONMCMIPV \
+nospecify +evalorder \
+notimingcheck \
+lint=TFIPC-L \
+ntb_solver_array_size_warn=100000000 \
-sverilog -kdb \
+v2k +vcs+lic+wait \
-timescale=100ps/10ps \
-debug_all \
+libext+.sv+.v+.V+.vp+.vlib \
-ntb_opts uvm-1.2 \
-assert dve -cc gcc \
-debug_all+nomemcbk+dmptf \
-debug_region+cell \
+define+SYNOPSYS_SV+NTB \
+define+no_timing \
-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a \
-f ./filelist/asic.f """

# ##-cm line+cond+fsm+tgl+branch+assert -cm_tgl mda \
# ##-cm_line contassign """
# ##+define+PEA_SIZE=1  \
# ##+define+ALUARITH=1 \
# ##+define+PEA_UT_VERIFY \


clean_args = """    \
rm -rf \
build/output/simv* \
build/output/csrc  \
build/log/*.log \
output*.log \
ucli.key vc_hdrs.h .vpd DVEfiles \
"""


run_args = """ \
build/output/simvcssvtb +UVM_LOG_RECORD \
-timescale=100ps/10ps \
+UVM_TIMEOUT="100000000000ps,YES" \
+vpdupdate \
+UVM_VERBOSITY=UVM_HIGH \
"""

define_args = """ """
sim_options = """ \
+UVM_VERBOSITY=UVM_NONE \
+UVM_TIMEOUT=50000000.YES \
+UVM_MAX_QUIT_COUNT=10.YES \
+UVM_RESOURCE_DB_TRACE \
+define+UVM_REG_FIELD_LEVEL_ATTRIBURE \
-assert dumpoff \
+vcs+flush+all \
-licwait 300 \
"""


def opt_process(opt):
    global comp_args
    global clean_args
    global define_args
    global sim_options

    seed_val = "1"
    wave_args = """ """

    os.system('mkdir -p build')
    os.chdir('build')
    os.system('mkdir -p log')
    os.system('mkdir -p output')
    os.system('mkdir -p wave')
    os.chdir('./../')

    (options, args) = opt.parse_args()
    is_valid_parse = True
    error_messages = []

    if options.seed_val == ' ':
        seed_val = '1'
    elif options.seed_val.isdigit():
        seed_val = options.seed_val
    elif options.seed_val == 'rand':
        random.seed()
        seed_val = str(random.random())
        seed_val = seed_val.strip('0')

    sub_path = options.sub_path

    if options.clean_data is True:
        os.system(clean_args)
        return 1

    if options.define is not None:
        define_list = options.define.split('+')
        print(define_list)
        for i in range(len(define_list)):
            define_args += '+define+'+define_list[i]+''
        print (define_args)
        # ##define_args += '+define+'+options.define+''

    if options.dump_fsdb is True:
        define_args += ' +define+DUMP_FSDB '
        if sub_path != '':
            wave_args += ' +FSDBNAME=%s/build/wave/'%(sub_path)+options.test_name+'_'+seed_val+'.fsdb'
        else:
            wave_args += ' +dump_fsdbfile '
            wave_args += ' +FSDBNAME=./build/wave/'+options.test_name+'_'+seed_val+'.fsdb'
            # wave_args += ' +FSDBNAME=verdi'+'.fsdb'

    if options.dump_vpd is True:
        define_args += ' +define+DUMP_VPD '
        if sub_path != '':
            wave_args += ' +VPDNAME=%s/build/wave/'%(sub_path)+options.test_name+'_'+seed_val+'.vpd'
        else:
            wave_args += ' +dump_vpdfile '
            wave_args += ' +VPDNAME=./build/wave/'+options.test_name+'_'+seed_val+'.vpd'
            wave_args += ' +vpdbufsize+50 +vpdfileswitchsize+2048 '

    if options.coverage_para is True:
        coverage = ' -cm line+tgl+fsm+cond+branch+assert -cm_name '+options.test_name+'_'+seed_val+' -cm_hier cm_hier.cfg'
    else:
        coverage = ' '

    if options.is_compile is True and options.is_run is False:
        command = comp_args
        if sub_path != '':
            command += ' -cm_dir ./%s/cm_dir ' % sub_path
            command += ' -Mdir=./%s/build/output/csrc -o ./%s/build/output/simvcssvtb ' % (sub_path, sub_path)
            command += ' -l ./%s/compile.log %s ' % (sub_path, define_args)
        else:
            command += ' -Mdir=./build/output/csrc -o ./output/simvcssvtb '
            command += ' -l ./build/log/compile.log'+define_args
        os.system(command)
    elif options.is_run is True and options.is_compile is False:
        command = ' '
        if sub_path != '':
            command += ' %s/%s' % (sub_path, run_args)
            command += ' -l ./%s/' % sub_path
            command += options.test_name+'_'+seed_val+'.log'+define_args+wave_args + coverage
        else:
            command += run_args
            command += ' -l ./build/log/'+options.test_name+'_'+seed_val+'.log'+define_args + coverage
        os.system(command)
    elif (options.is_run is True and options.is_compile is True) or (options.is_run is False and options.is_compile is False):
        command = comp_args
        if sub_path != '':
            command += ' -cm_dir ./%s/cm_dir ' % sub_path
            command += ' -Mdir=./%s/build/output/csrc -o ./%s/build/output/simvcssvtb ' % (sub_path, sub_path)
            command += ' -l ./%s/compile.log %s ' % (sub_path, define_args)
        else:
            command += ' -Mdir=./build/output/csrc -o ./output/simvcssvtb '
            command += ' -l ./build/log/compile.log' + define_args
        if options.assertion is True:
            command += ' -assert dve -debug_all -assert enable_diag -cm_assert'
            command += ' ../seq/cp_pwr/assertiong/'+options.assertion_name+'.sv'
        os.system(command)
        if sub_path != '':
            command += ' %s/%s' % (sub_path, run_args)
            command += ' -l ./%s/' % sub_path
            command += options.test_name+'_'+seed_val+'.log'+define_args+wave_args + coverage
        else:
            command += run_args
            command += ' -l ./build/log/'+options.test_name+'_'+seed_val+'.log'+define_args+wave_args + coverage
        command += ' +ntb_random_seed='+seed_val
        command += ' +UVM_TESTNAME='+options.test_name
        # command += ' -gui &'
        if options.assertion is True:
            command += ' -assert success'
            command += ' -assert report=./assertion/'+options.test_name+'_assertion_report'
            command += ' -assert filter+success'
        os.system(command)
        return 1
    else:
        opt.print_help()
        return None

def get_user_parse():
    try:
        opt = OptionParser()
        # opt.add_option('--f',                 action="store",         dest="filelist",        default="",         help="input rtl and verify filelist")
        opt.add_option('--tc',                  action="store",         dest="test_name",       default="",         help="input simulation testcase name")
        opt.add_option('-r',                    action="store_true",    dest="is_run",          default="False",    help="run testcase simulation")
        opt.add_option('-c',                    action="store_true",    dest="is_compile",      default="False",    help="only compile testcase")
        opt.add_option('-d',                    action="store",         dest="define",          default="None",     help="define params")
        opt.add_option('--seed',                action="store",         dest="seed_val",        default="",         help="random seed value")
        opt.add_option('-f', '--fsdb',          action="store_true",    dest="dump_fsdb",       default="False",    help="swtich dump fsdb waveform")
        opt.add_option('-v', '--vpd',           action="store_true",    dest="dump_vpd",        default="False",    help="swtich dump vpd waveform")
        opt.add_option('--clean',               action="store_true",    dest="clean_data",      default="False",    help="clean compile result")
        opt.add_option('-p', '--path',          action="store",         dest="sub_path",        default="",         help="indicate sub path for regression")
        opt.add_option('-a', '--assertion',     action="store_true",    dest="assertion",       default="False",    help="enable assertion sim")
        opt.add_option('--sva_name',            action="store",         dest="assertion_name",  default="",         help="input assertion name")
        opt.add_option('--cov',                 action="store_true",    dest="coverage_para",   default="False",    help="for coverage count")
    except Exception as ex:
        print("exception:{0}".format(str(ex)))
        return None


if __name__ == "__main__":
    user_paras = get_user_parse()
    if user_paras is None:
        sys.exit(0)
    info = "test_name:{0}"
    info = info.format(user_paras["test_name"])
    print('---------------')
    print(info)
    print(define_args)
    print('---------------')
