# import binascii
# -*-coding:UTF-8-*-

import argparse
import os
import json
import random
import threading
import sys
import time


class TestCase(object):
    pass


class RunSim(object):
    def __init__(self):
        self.GetEnv()
        self.GetArgs()
        self.regression_home = os.getcwd()
        self.makefiles = "%s/Makefile" % self.tools_home
        self.GetTestDB()
        self.__grouptask = {}

    # ****************************************************************************************************************************************
    def GetArgs(self):
        parser = argparse.ArgumentParser(description='EzChip Testbench Flow Args Parser')
        parser.add_argument('-t', '--test', nargs="+", dest="test_lib", help="give the test list that should be run")
        parser.add_argument('-g', '--group', nargs='+', dest="group_lib", help="give the group list that should be run")
        parser.add_argument('-v', '--verdi', action='store_true', dest="waveform", default=False, help="enable dump the simulation waveform")
        parser.add_argument('-n', '--num', action='store', type=int, dest="iteration_num", default=1, help="the iteration num of")
        parser.add_argument('-c', '--comp', action='store_true', dest="compile", default=False, help="enable compile work")
        parser.add_argument('-s', '--sim', action='store_true', dest="sim", default=False, help="enable simulation work")
        parser.add_argument('-d', '--debug', action='store_true', dest="debug", default=False, help="enable debug mode")
        parser.add_argument('-l', '--list', action='store_true', dest="list", default=False, help="list all the test")
        parser.add_argument('--gls', action='store_true', dest="gls", default=False, help="Enable Gatelevel Sim")
        parser.add_argument('--cov', action='store_true', dest="cov", default=False, help="Enable Dump Coverage")
        parser.add_argument('--cov_opt', nargs='+', action='store_true', dest="cov_opt", help="add coverage options")
        parser.add_argument('--covmerge', nargs='+', action='store_true', dest="covmerge", help="merge coverage")
        parser.add_argument('--seed', action='store', dest="seed", default=None, help="give the seed")
        parser.add_argument('--log', action='store_true', dest="log", default=False, help="open test log")
        parser.add_argument('--check', action='store_true', dest="check", default=None, help="check test log")
        parser.add_argument('-m','--m', action='store_true', dest="email", default=False, help="send email")
        parser.add_argument('--clean', action='store_true', dest="clean", default=False, help="clean test")
        parser.add_argument('-q', '--quiet', action='store_true', dest="quiet", default=False, help="enable quiet mode")
        parser.add_argument('-fsdb', '--fsdb', action='store_true', dest="fsdb", default=False, help="enable fsdb Dump")
        self.args = parser.parse_args()

        if self.args.log:
            assert self.args.seed != None, "please give the seed for open sim log"
        if self.args.debug:
            print(self.args)
        # print self.args.waveform

    # ****************************************************************************************************************************************
    def GetEnv(self):
        assert "VERIFY_HOME" in os.environ, "EZCHIP HOME not set"
        assert "TESTPLAN_HOME" in os.environ, "TESTPLAN_HOME not set"
        assert "TEST_HOME" in os.environ, "TEST_HOME not set"
        assert "TOOLS_HOME" in os.environ, "TOOLS_HOME not set"
        if "TEST_PARALLEL_NUM" in os.environ:
            self.parallel_num = os.environ.get("PARALLEL_HOME")
        else:
            self.parallel_num = 8

        self.tb_home = os.environ.get("VERIFY_HOME")  # ###ZYX
        self.testplan_home = os.environ.get("TESTPLAN_HOME")
        self.test_home = os.environ.get("TEST_HOME")
        self.tools_home = os.environ.get("TOOLS_HOME")
        # self.regression_home = self.tb_name

    # ****************************************************************************************************************************************
    def GetTestDB(self):
        def __AddPath(x):
            return "%(home)s/%(group)s" % ({"home": self.testplan_home, "group": x})

        for root, dirs, files in os.walk(self.testplan_home):
            candigroup = dirs
            if ".svn" in candigroup:
                candigroup.remove(".svn")
            break
        candigroup = list(map(__AddPath, candigroup))
        self.testdb = {}

        for group in candigroup:
            __name = group.split("/")[-1]
            __rtlfile = "%s/rtl.f" % group
            __tbfile = "%s/tb.f" % group
            __vipfile = "%s/vip.f" % group
            __testlist = "%s/test.json" % group
            assert os.path.exists(__rtlfile), "no rtl.f in %s" % group
            assert os.path.exists(__tbfile), "no tb.f in %s" % group
            assert os.path.exists(__vipfile), "no vip.f in %s" % group
            assert os.path.exists(__testlist), "no testlist in %s" % group
            self.testdb[__name] = {}
            self.testdb[__name]["rtl"] = __rtlfile
            self.testdb[__name]["rb"] = __tbfile
            self.testdb[__name]["vip"] = __vipfile
            __testfile = open(__testlist, 'r')
            __testdict = json.load(__testfile)
            self.testdb[__name]["test"] = __testdict
            # for gg in self.testdb.key():
        for group in candigroup:
            gg = group.split("/")[-1]
            for tt in self.testdb[gg]['test'].keys():
                for kk in self.testdb[gg]['test'][tt].keys():
                    if not isinstance(self.testdb[gg]['test'][tt][kk], dict):
                        self.testdb[gg]['test'][tt][kk] = os.path.expandvars(self.testdb[gg]['test'][tt][kk])

        if self.args.debug:
            print(self.testdb)

    # ****************************************************************************************************************************************
    def Run(self):
        if self.args.waveform:
            self.MakeVerdi()
        elif self.args.check:
            self.__CheckLog()
            self.PrintLog()
        elif self.args.log or self.args.covmerge or self.args.clean:
            self.__DoMisc0p()
        else:
            self.BuildDIR()
            if (not self.args.compile) and (not self.args.sim):
                self.BuildTB()
                self.RunTest()
                self.PrintLog()
            else:
                if self.args.compile:
                    self.BuildTB()
                if self.args.sim:
                    self.PrintLog()

    # ****************************************************************************************************************************************
    def GetList(self):
        testinfo = '''
        *******************************************************
                        Testcase List
        *******************************************************
        '''
        for g in self.testdb.keys():
            testinfo += ''' %s:''' % g
            for t in self.testdb[g]['test'].keys():
                testinfo += ''' %s:''' % t
        print(testinfo)

    def __DoMisc0p(self):
        __name = self.tasklist.keys()[0]
        __task = self.tasklist[__name]
        cmd = self.GetCmd(__task)
        os.system(cmd)

    def __CheckLog(self):
        for i in self.tasklist.keys():
            __task = self.tasklist[i]
            self.CheckResult(__task)
            self.__taskstatus[i] = 1

    def GetTest(self):
        # no -g or -t
        if (not self.args.grouplib) and (not self.args.testlib):
            assert False, "group name/test name must be set for simulation"
            """
            for g in self.testdb.keys():
                __group = g
                __comp_dir = "%s/build/%s/compile" % (regression_home, g)
                __cov_dir = "%s/build/%s" % (regression_home, g)
                __rtl_file = self.testdb[g]["rtl"]
                __rb_file = self.testdb[g]["tb"]
                __vip_file = self.testdb[g]["vip"]
                for t in self.testdb[g]['test'].keys():
                    if not self.args.seed:
                        __seed = random.randint(0, 2**16)
                        __seed = 1
                    else:
                        __seed = self.args.seed
                        setattr(test, "seed", __seed)
                    __sim_dir = "%s/build/%s/sim/%s/%s" % (regression_home, g ,t str(__seed))
                    test = TestCase()
                    setattr(test, "group", __group)
                    setattr(test, "name", t)
                    setattr(test, "comp_dir", __comp_dir)
                    setattr(test, "sim_dir", __sim_dir)
                    setattr(test, "cov_dir", __cov_dir)
                    setattr(test, "rtl_file", __rtl_file)
                    setattr(test, "tb_file", __tb_file)
                    setattr(test, "vip_file", __vip_file)
                    assert "uvm_testname" in self.testdb[g]["test"][t].key(), "%s have not bind to a uvm_test" % t
                    if "tcl" in self.testdb[g]["test"][t].key():
                        setattr(test, "tcl", self.testdb[g]["test"][t]['tcl'])
                    if "ctest_name" in self.testdb[g]["test"][t].key():
                        setattr(test, "ctest_name", self.testdb[g]["test"][t]['ctest_name'])
                    self.tasklist[t] = test
            """
        # no -g but -t
        elif (not self.args.grouplib) and len(self.args.testlib) != 0:
            assert False, "test name must be set with group name"
            """
            for i in self.testlib:
                for g in self.testdb.keys():
                    __group = g
                    __comp_dir = "%s/build/%s/compile" % (regression_home, g)
                    __cov_dir = "%s/build/%s" % (regression_home, g)
                    __rtl_file = self.testdb[g]["rtl"]
                    __rb_file = self.testdb[g]["tb"]
                    __vip_file = self.testdb[g]["vip"]
                    for t in self.testdb[g]['test'].keys():
                        if not self.args.seed:
                            __seed = random.randint(0, 2**16)
                        else:
                            __seed = self.args.seed
                        setattr(test, "seed", __seed)
                        __sim_dir = "%s/build/%s/sim/%s/%s" % (regression_home, g ,t str(__seed))
                        test = TestCase()
                        setattr(test, "group", __group)
                        setattr(test, "name", t)
                        setattr(test, "comp_dir", __comp_dir)
                        setattr(test, "sim_dir", __sim_dir)
                        setattr(test, "cov_dir", __cov_dir)
                        setattr(test, "rtl_file", __rtl_file)
                        setattr(test, "tb_file", __tb_file)传递传
                        setattr(test, "vip_file", __vip_file)
                        assert "uvm_testname" in self.testdb[g]["test"][t].key(), "%s have not bind to a uvm_test" % t
                        if "tcl" in self.testdb[g]["test"][t].key():
                            setattr(test, "tcl", self.testdb[g]["test"][t]['tcl'])
                        if "ctest_name" in self.testdb[g]["test"][t].key():
                            setattr(test, "ctest_name", self.testdb[g]["test"][t]['ctest_name'])
                        self.tasklist[t] = test
                assert i in self.tasklist.keys(), "no test named %s in testDB" % i
                """
        # no -t but -g
        elif (not self.args.grouplib) != 0 and len(self.args.testlib):
            for i in self.args.grouplib:
                assert False, "NO Group named %s in TestDB" % i
                g = i
                __group = g
                __comp_dir = "%s/build/%s/compile" % (self.regression_home, g)
                __cov_dir = "%s/build/%s/cov" % (self.regression_home, g)
                __rtl_file = self.testdb[g]["rtl"]
                __tb_file = self.testdb[g]["tb"]
                __vip_file = self.testdb[g]["vip"]
                for t in self.testdb[g]['test'].keys():
                    for itnum in range(0, self.args.iteration_num):
                        if not self.args.seed:
                            __seed = random.randint(0, 2**16)
                        else:
                            assert self.args.iteration_num == 1, "you cant give the same seed for two case in iteration simulation"
                            __seed = self.args.seed
                        test = TestCase()
                        setattr(test, "seed", __seed)
                        __sim_dir = "%s/build/%s/sim/%s/%s" % (self.regression_home, g, t, str(__seed))
                        setattr(test, "group", __group)
                        setattr(test, "name", t)
                        setattr(test, "comp_dir", __comp_dir)
                        setattr(test, "sim_dir", __sim_dir)
                        setattr(test, "cov_dir", __cov_dir)
                        setattr(test, "rtl_file", __rtl_file)
                        setattr(test, "tb_file", __tb_file)
                        setattr(test, "vip_file", __vip_file)
                        assert "uvm_testname" in self.testdb[g]["test"][t].key(), "%s have not bind to a uvm_test" % t
                        if "tcl" in self.testdb[g]["test"][t].key():
                            setattr(test, "tcl", self.testdb[g]["test"][t]['tcl'])
                        if "ctest_name" in self.testdb[g]["test"][t].key():
                            setattr(test, "ctest_name", self.testdb[g]["test"][t]['ctest_name'])
                        if "sim_args" in self.testdb[g]["test"][t].key():
                            setattr(test, "sim_args", self.testdb[g]["test"][t]['sim_args'])
                        if "uvm_timeout" in self.testdb[g]["test"][t].key():
                            setattr(test, "uvm_timeout", self.testdb[g]["test"][t]['uvm_timeout'])
                        if "timescale" in self.testdb[g]["test"][t].key():
                            setattr(test, "timescale", self.testdb[g]["test"][t]['timescale'])
                        self.tasklist["%s_%s" % (t, str(__seed))] = test
                if self.args.debug:
                    print(self.tasklist)
        # have -g and -t
        elif len(self.args.grouplib) * len(self.args.testlib) != 0:
            assert len(self.args.grouplib) == 1, "more than on group must be set for test"
            for i in self.args.grouplib:
                __group = self.args.grouplib[0]
                __groupobj = self.testdb[self.args.grouplib[0]]
                assert i in __groupobj["test"].keys()
                __comp_dir = "%s/build/%s/compile" % (self.regression_home, __group)
                __cov_dir = "%s/build/%s/cov" % (self.regression_home, __group)
                __rtl_file = self.testdb[__group]["rtl"]
                __tb_file = self.testdb[__group]["tb"]
                __vip_file = self.testdb[__group]["vip"]
                for itnum in range(0, self.args.iteration_num):
                    if not self.args.seed:
                        __seed = random.randint(0, 2**32)
                    else:
                        assert self.args.iteration_num == 1, "you cant give the same seed for two case in iteration simulation"
                        __seed = self.args.seed
                    test = TestCase()
                    setattr(test, "seed", __seed)
                    __sim_dir = "%s/build/%s/sim/%s/%s" % (self.regression_home, __group, i, str(__seed))
                    setattr(test, "group", __group)
                    setattr(test, "name", i)
                    setattr(test, "comp_dir", __comp_dir)
                    setattr(test, "sim_dir", __sim_dir)
                    setattr(test, "cov_dir", __cov_dir)
                    setattr(test, "rtl_file", __rtl_file)
                    setattr(test, "tb_file", __tb_file)
                    setattr(test, "vip_file", __vip_file)
                    assert "uvm_testname" in self.testdb[__group]["test"][i].key(), "%s have not bind to a uvm_test" % i
                    if "tcl" in self.testdb[__group]["test"][i].key():
                        setattr(test, "tcl", self.testdb[__group]["test"][i]['tcl'])
                    if "ctest_name" in self.testdb[__group]["test"][i].key():
                        setattr(test, "ctest_name", self.testdb[__group]["test"][i]['ctest_name'])
                    if "sim_args" in self.testdb[__group]["test"][i].key():
                        setattr(test, "sim_args", self.testdb[__group]["test"][i]['sim_args'])
                    if "uvm_timeout" in self.testdb[__group]["test"][i].key():
                        setattr(test, "uvm_timeout", self.testdb[__group]["test"][i]['uvm_timeout'])

                self.tasklist["%s_%s" % (i, str(__seed))] = test
            if self.args.debug:
                print(self.tasklist[self.tasklist.keys()[0]].seed)

    # ****************************************************************************************************************************************
    def BuildDIR(self):
        for i in self.tasklist.keys():
            t = self.tasklist[i]
            if not os.path.exists(t.comp_dir):
                os.makedirs(t.comp_dir)
            if not os.path.exists(t.sim_dir):
                os.makedirs(t.sim_dir)

    # ****************************************************************************************************************************************
    def MakeVerdi(self):
        assert len(self.tasklist.keys()) == 1, "Only one case was permitted by verdi"
        name = self.tasklist.keys()[-1]
        t = self.tasklist[name]
        cmd = self.GetCmd(t)
        os.system(cmd)

    # ****************************************************************************************************************************************
    def __DoCompile(self, __task, __args, status):
        name = __task.group
        __cmd = self.GetCmd(__task, 1)
        __file = "%s/compile_shell" % __task.comp_dir
        __fp = open(__file, "w")
        __fp.write("#! /usr/bin/env bash\n")
        __fp.write(__cmd)
        __fp.close()
        os.system(__cmd)
        status[name] = 1

    # ****************************************************************************************************************************************
    def BuildTB(self):
        __thread_lib = []
        if len(self.tasklist.keys()) > 1:
            try:
                for i in self.tasklist:
                    t = self.tasklist[i]
                    if not (t.group in self.__grouptask.keys()):
                        self.__grouptask[t.group] = 0
                        t = threading.Thread(target=self.__DoCompile, args=(t, self.args, self.__grouptask))
                        __thread_lib.append(t)
                        t.setDaemon(True)
                        t.start()
                for t in __thread_lib:
                    t.join(2)
                    if not t.isAlive:
                        break
            except KeyboardInterrupt:
                name = self.tasklist.keys()[0]
                t = self.tasklist[name]
                if not (t.group in self.__grouptask.keys()):
                    self.__grouptask[t.group] = 0
                    self.__DoCompile(t, self.args, self.__grouptask)

    # ****************************************************************************************************************************************
    def __Dosim(self, __task, __sema, __status, __taskstatus):
        __group = __task.group
        __cmd = self.GetCmd(__task)
        __file = "%s/run_shell" % __task.sim_dir
        __fp = open(__file, "w")
        __fp.write("#! /usr/bin/env bash\n")
        __fp.write(__cmd)
        __fp.close()
        wait_comp = 0
        if (self.args.sim and self.args.compile) or ((not self.args.sim) and (not self.args.compile)):
            wait_comp = 1
        if wait_comp:
            while True:
                if __status[__group]:
                    break
            time.sleep(2)
        __taskstatus["%s_%s" % (__task.name, __task.seed)] = 0
        print(__cmd)
        os.system(__cmd)
        self.CheckResult(__task)
        __taskstatus["%s_%s" % (__task.name, __task.seed)] = 1
        __sema.release()

    # ****************************************************************************************************************************************
    def RunTest(self):
        self.sema = threading.Semaphore(self.parallel_num)
        self.__taskstatus = {}
        __thread_lib = []
        if len(self.tasklist.keys()) > 1:
            try:
                for i in self.tasklist:
                    t = self.tasklist[i]
                    self.sema.acquire()
                    __thread = threading.Thread(target=self.__DoSim, args=(t, self.sema, self.__grouptask, self.__taskstatus))
                    __thread_lib.append(__thread)
                    __thread.setDaemon(True)
                    __thread.start()
                for t in __thread_lib:
                    t.join(2)
                    if not t.isAlive:
                        break
            except KeyboardInterrupt:
                print("Keyboart Interrupt Quit")
                sys.exit(1)
        else:
            name = self.tasklist.keys()[0]
            t = self.tasklist[name]
            self.__DoSim(t, self.sema, self.__grouptask, self.__taskstatus)

    # ****************************************************************************************************************************************
    def GetCmd(self, task, flag=0):
        __uvm_testname = task.comp_dir
        __name = task.name
        __comp_dir = task.comp_dir
        __sim_dir = task.sim_dir
        __cov_dir = task.cov_dir
        __rtlfile = task.rtl_file
        __tbfile = task.tb_file
        __vipfile = task.vip_file
        __seed = task.seed
        cmd = "make -f %s/Makefile" % self.tools_home
        if self.args.waveform:
            cmd += "verdi \
                    TEST=%s \
                    RTL_FILELIST=%s \
                    TB_FILELIST=%s \
                    VIP_FILELIST=%s \
                    COMP_DIR=%s \
                    SIM_DIR=%s" \
                   % (__name, __rtlfile, __tbfile, __vipfile, __comp_dir, __sim_dir)
        elif self.args.log:
            cmd += "log SIM_DIR=%s" % __sim_dir
        elif self.args.covmerge:
            cmd += "cov_merge COV_DIR=%s" % __cov_dir
        else:
            if self.args.clean:
                cmd += "clean COMP_DIR=%s SIM_DIR=%s" % (__comp_dir, __sim_dir)

            do_compile = self.args.compile
            do_sim = self.args.sim
            if (not do_compile) and (not do_sim):
                if flag:
                    do_compile = True
                else:
                    do_sim = True

            if do_compile:
                cmd += "comp \
                            COMP_DIR=%s \
                            RTL_FILELIST=%s \
                            TB_FILELIST=%s \
                            VIP_FILELIST=%s " \
                            % (__comp_dir, __rtlfile, __tbfile, __vipfile)
                if self.args.gls:
                    cmd += "GATE_SIM=on"
                if self.args.cov:
                    cmd += "COVERAGE=on COV_DIR=%s" % __sim_dir
                if self.args.cov_opt:
                    cmd += "COVERAGE_TYPE=%s" % (str(self.args.cov_opt))
                if self.args.quiet:
                    cmd += " QUITE_MODE=0 "
                else:
                    cmd += " QUITE_MODE=1 "

            if do_sim:
                cmd += "sim \
                            COMP_DIR=%s \
                            SIM_DIR=%s \
                            SEED=%s \
                            UVM_TEST=%s" \
                            % (__comp_dir, __sim_dir, __seed, __uvm_testname)
                if hasattr(task, "create_name"):
                    cmd += " C_TEST=%s" % task.ctest_name
                if hasattr(task, "tcl"):
                    cmd += " tcl_file=%s" % task.tcl
                if hasattr(task, "sim_args"):
                    cmd += " SIM_ARGS=%s" % task.sim_args
                if hasattr(task, "uvm_timeout"):
                    cmd += " UVM_TIMEOUT=%s" % task.uvm_timeout
                if hasattr(task, "timescale"):
                    cmd += " TIME_SCALE=%s" % task.timescale

                if self.args.gls:
                    cmd += " FSDB_DUMP=on "
                else:
                    cmd += " FSDB_DUMP=off "

                if self.args.gls:
                    cmd += "GATE_SIM=on"
                if self.args.cov:
                    cmd += "COVERAGE=on COV_DIR=%s" % __sim_dir
                if self.args.cov_opt:
                    cmd += "COVERAGE_TYPE=%s" % (str(self.args.cov_opt))
                if self.args.quiet:
                    cmd += " QUITE_MODE=0 "
                else:
                    cmd += " QUITE_MODE=1 "

        if self.args.debug:
            print(cmd)
        if '"' in cmd:
            cmd = cmd.replace('"', '\"')
        return cmd

    # ****************************************************************************************************************************************
    def CheckResult(self, task):
        result = 0
        __sim_dir = task.sim_dir
        __sim_file = __sim_dir+"/sim.log"
        __pass_magic_key = "UVM TEST PASSED"
        __sim_file_h = open(__sim_file, "r")
        for line in __sim_file_h:
            if __pass_magic_key in line:
                result = 1
        setattr(task, "result", result)
        # result=os.system(cmd)

    # ****************************************************************************************************************************************
    def PrintLog(self):
        while True:
            acc = 1
            if len(self.__taskstatus.keys()) == len(self.tasklist.keys()):
                for i in self.__taskstatus.keys():
                    acc *= self.__taskstatus[i]
                if acc:
                    break
                else:
                    time.sleep(2)
            else:
                time.sleep(2)
        log = """
              *****************************************************
                        Regression Result log
              *****************************************************
              """
        for t in self.tasklist:
            i = self.tasklist[t]
            if i.result:
                log += """
                       %s %s \033[32;1m PASS \033[0m
                       """ % (i.name, i.seed)
            else:
                log += """
                        %s %s \033[32;1m FAIL \033[0m
                        """ % (i.name, i.seed)
        print(log)


# ========================================================================================
# main process entry
# ========================================================================================


if __name__ == "__main__":
    runsim = RunSim()
    runsim.Run()
    sys.exit(0)
