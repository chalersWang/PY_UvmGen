# import binascii
# -*-coding:UTF-8-*-

import csv
import sys
import os
import re
# import shutil
import datetime
import glob
import subprocess
import multiprocessing
import random
import time
from multiprocessing import Pool
from optparse import OptionParser


def rd_case_from_file(regress_filename):
    with open(regress_filename) as f:
        f_csv = csv.reader(f)
        testname_list = []
        # test_runnum = []
        # print(type(f_csv))    #print:<class '_csv.reader'>
        for row in f_csv:
            # print(row)        #print array line
            for testname in row:
                # print(testname)   #traversal casename
                # print(type(testname))
                # list_str = testname.split(r"+",testname")
                # list_str = re.split(r"+",testname)
                testname_list.append(testname)
                # testname_list.append(list_str[0])
                # print(list_str[0])
                # test_runnum.append(list_str[1])
                # print(list_strr[1])

                # for match_strr in list_str:
                #   if rer.match("TESTNAME",match_str)
                #   print(match_str)
                #   testname_list.append(match_str[9:])
                #   testnaem_list.append(match_str)
                #   print(testname_list)
    return testname_list    # test_runnum


def regress(case):
    # covert path to filename
    # print(case)
    list_str = re.split(r" +", case)
    case_name = list_str[0]
    print(case_name)
    run_num = list_str[1]
    print(run_num)
    # filst0 = (filst.split('/'))
    # print(filst0[2])
    # regress_filename0 = filst0[-1]
    # print(regress_filename0)
    start_time = datetime.datetime.now()
    run_cnt = 0
    sub_path_path = os.getcwd()
    sub_path_path = sub_path_path.strip()
    sub_path_mkdir = sub_path_path+'/'+sub_path+create_date+'/'+case_name
    print(sub_path_mkdir)
    exists_sub_dir = os.path.exists(sub_path_mkdir)
    if not exists_sub_dir:
        os.makedirs(sub_path_mkdir)
    sub_output_dir = sub_path_mkdir+'/build/output'
    sub_outpur_exist = os.path.exists(sub_output_dir)
    if not sub_outpur_exist:
        os.makedirs(sub_output_dir)
    sub_path_sub = 'regress_result/'+sub_path_mkdir.split('/')[-2]+'/'+sub_path_mkdir.split('/')[-1]
    print('sub_path_sub '+sub_path_sub)
    while run_cnt < int(run_num):
        random.seed()
        seed_val = str(random.random())
        seed_val = seed_val.strip('0.')
        if run_cnt == 0:
            sim_cmd = 'srun.py -r -c --cov --tc='+case_name+' --seed='+seed_val+' -p %s' % sub_path_sub+''
        else:
            sim_cmd = 'srun.py -r --cov --tc=' + case_name + ' --seed=' + seed_val + ' -p %s' % sub_path_sub + ''
        run_cnt += 1
        print(sim_cmd)
        os.system(sim_cmd)
        time.sleep(1)
        print("3......")
        time.sleep(1)
        print("1......")
        time.sleep(1)
        print("1......")
    # run_cnt = 0
    end_time = datetime.datetime.now()
    sub_time1 = (end_time-start_time).seconds/60
    sub_time = ('%.2f' % sub_time1)
    # path = os.path.join(os.getcwd(),"sim",name)
    # print(path)
    f = open(sub_date_path+"/regression_result.txt", 'a+')
    f.write(time.asctime(time.localtime(time.time()))+"\t"+'\n')
    check_log_path = os.path.join(sub_path_mkdir, '*.log')
    print('check_log_path'+check_log_path)
    for file_path in glob.glob(check_log_path):
        filename = file_path.split("/")[-1]
        if filename != 'compile.log':
            # cmd = 'gerp UVM_TEST_PASSED .//' +sub_path_sub+'/sim.log'+' >/dev/null 2>&1'
            cmd = 'grep UVM_TEST_PASSED '+file_path+' >/dev/null 2>&1'
            print('file_path'+file_path)
            print('cmd_'+cmd)
            if subprocess.call(cmd, shell=True) == 0:
                result = '{:<35'.format(filename)+"\t"+" PASS"+"\t"+"simulation time"+sub_time+"miutes"
                f.write(result+"\n")
                # print('========================last_pass_name:',name)
                # shutil.rmtree(path)
            else:
                result = '{:<35'.format(filename)+"\t"+" FAIL"+"\t"+"simulation time"+sub_time+"miutes"
                f.write(result + "\n")
    f.close()


def gen_vdb():
    vdb_fld_list = []
    vdb_file_list = []
    vdb_path = os.getcwd()
    # ## vdb folder
    for vdb_folder in os.listdir(vdb_path+'regression_result'+create_date):
        this_path = os.path.join(vdb_path+'regression_result'+create_date, vdb_folder)
        if os.path.isdir(this_path):
            vdb_fld_list.append(this_path)
    # ## vdb files
    for vdb_files in vdb_fld_list:
        vdb_name = vdb_files.split("/")[-1]
        print(vdb_name+'vdb_name')
        if vdb_name != 'output':
            vdb_file_list.append(vdb_files+'/cmd_dir.vdb')
    for i in vdb_file_list:
        print('vdb_file_list'+i)
    # ## merge vdb
    vdb_path = vdb_path.strip()
    vdb_dir = vdb_path+'/regression_vdb'
    is_exists = os.path.exists(vdb_dir)
    if not is_exists:
        os.makedirs(vdb_dir)
        merge_files = ''
        for mrg_file in vdb_file_list:
            merge_files = merge_files+' -dir '+mrg_file
        print('merge_files'+merge_files)
        merge_vdb = 'cd '+vdb_dir+'; urg -parallel '+merge_files+' -dbname cm_dir'
        print('merge_vdb'+merge_vdb)
        os.system(merge_vdb)
    else:
        merge_files = ''
        for mrg_file in vdb_file_list:
            merge_files = merge_files + ' -dir ' + mrg_file
        command = 'cd '+vdb_dir+'; mv cm_dir.vdb cm_merge_dir'
        os.system(command)
        merge_vdb = 'cd ' + vdb_dir + '; urg -parallel -dir cm_merge_dir '+merge_files+' -dbname cm_dir ; rm -rf cm_merge_dir'
        os.system(merge_vdb)


def env():
    # dirpath = os.getcwd()       # get current dir path
    os.popen('source ./bootenv.sh')
    os.popen('source /opt/rh/devtoolset-4enable')   # update gcc


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--flist",  action="store", type="string",  dest="filelist",    help="caselist filename")
    (options, args) = parser.parse_args()
    run_starttime = datetime.datetime.now()
    flist = options.filelist
    print(flist.split('.')[0])
    # env       # unset
    caselist = rd_case_from_file(flist)
    print('rd case from file end!')
    # rm_file = ' rm -rf ./regression_result/*'
    # os.system(rm_file)
    # os.remove("")
    file_dir = os.getcwd()
    regr_list = file_dir+'/'+flist
    file_exists = os.path.isfile(regr_list)
    if not file_exists:
        print('regression filelist is not exist!')
        sys.exit(1)
    run_path = os.getcwd()
    run_path = run_path.strip()
    mk_dir = run_path+'/regression_result'
    is_exists = os.path.exists(mk_dir)
    if not is_exists:
        os.makedirs(mk_dir)
    obtain_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    create_date = '/regression_'+obtain_date
    sub_date_path = mk_dir+create_date
    sub_date_exists = os.path.exists(sub_date_path)
    if not sub_date_exists:
        os.makedirs(sub_date_path)
    # out_path = mk_dir+'/output'
    # out_file_exit = os.path.exists(out_path)
    # if not out_file_exit:
    #   os.makedirs(out_path)
    sub_path = 'regression_result'
    for i in caselist:
        print(i)
    # for i in run_num:
    #   print(i)
    pool = multiprocessing.Pool(processes=10)
    print('---------------drop pool start-------------')
    for i in caselist:
        pool.apply_async(regress, (i,))     # ps aux | grep $USER
    print('---------------pool end-------------')
    pool.close()
    # pool.start()
    pool.join()
    time.sleep(1)
    gen_vdb()
    case_info = flist + ' case number is ' + str(len(caselist))
    print(case_info)
    run_stoptime = datetime.datetime.now()
    total_runtime = (run_stoptime-run_starttime).seconds/60
    print('total run time is '+str(total_runtime)+' mimutes')
