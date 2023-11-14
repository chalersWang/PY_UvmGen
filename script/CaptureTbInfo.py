# import binascii
# -*-coding:UTF-8-*-

import os
import sys

print("hello CaptureTbInfo")


class capture_tb_info:

    def __init__(self, Infile, InArray, novifArray, module_name):
        self.Infile = Infile
        self.InArray = InArray
        self.novifArray = novifArray
        self.module_name = module_name

    def capture_tbinfo(self):
        print("CaptureInfo.main.capture_tbinfo")
        # Array=[]
        a = []
        b = []
        c = []
        d = []
        e = []
        f = []
        g = []
        h = []
        # i = []
        v = []
        j = []
        k = []
        # l = []
        w = []
        m = []
        n = []
        a_num = 0

#        vip_types=[]
#        polling_active=True
#        while polling_active:
#            integ_vip=input("Whether integer vip in tb(yes/no):")
#            if integ_vip=='yes':
#                vip_type=input("Please input the vip_type(apb/ahb/axi):")
#                vip_types.append(vip_type)
#                repeat=input("Whether integer vip in tb(yes/no):")
#                if repeat=='no':
#                    polling_active=Fase
#            else
#                polling_active=False
#        print("\n-----vip polling reseut-----")
#        for vip_type in vip_types:
#            print("Will integer" + vip_type + "in tb!\n")

        file_in = open(self.Infile, 'r+')
        # ########################################################
        # ###parse "verify xxx start","verify xxx end"
        # ###vif_name=xxx
        # ########################################################
        vif_name = ''
        c_append_flag = False            # #append to :total array
        write_flag = False
        novif_append_flag = False
        # ############################################################################
        # ###first judge write_flag
        # #if ture
        # #      then judge novif_append_flag
        # #          if ture:append to:novifArray
        # #          if flase:append to Array(store each uvc information)
        # #
        # #last at every verify end,set c_append_flag true
        # #  then append each uvc to (Array)
        # ############################################################################
        lines = file_in.readlines()
        # print(type(lines), lines)
        for s in lines:
            # print(s)
            if 'module' in s:
                if s.split()[0] == 'module':
                    model_name = s.split()[1]
                    # module_name = []
                    # model_name =
                    # insert model_name into module_name
                    self.module_name.append(model_name)
                    print(self.module_name)
            # print("111111111111111111111111111111111111111111111111111111")
            if 'verify start' in s:
                # print("verify start balabala")
                vip_name = s.split()[-1]
                print(vip_name)
                if a_num is 0:
                    a.append(vip_name)
                    print("verify start : a %s" % a)
                if a_num is 1:
                    b.append(vip_name)
                    print("verify start : b %s" % b)
                if a_num is 2:
                    c.append(vip_name)
                    print("verify start : c %s" % c)
                if a_num is 3:
                    d.append(vip_name)
                    print("verify start : d %s" % d)
                if a_num is 4:
                    e.append(vip_name)
                    print("verify start : e %s" % e)
                if a_num is 5:
                    f.append(vip_name)
                    print("verify start : f %s" % f)
                if a_num is 6:
                    g.append(vip_name)
                    print("verify start : g %s" % g)
                if a_num is 7:
                    h.append(vip_name)
                    print("verify start : h %s" % h)
                if a_num is 8:
                    # i.append(vip_name)
                    # print("verify start : i %s" % i)
                    v.append(vip_name)
                    print("verify start : v %s" % v)
                if a_num is 9:
                    j.append(vip_name)
                    print("verify start : j %s" % j)
                if a_num is 10:
                    k.append(vip_name)
                    print("verify start : k %s" % k)
                if a_num is 11:
                    # l.append(vip_name)
                    # print("verify start : l %s" % l)
                    w.append(vip_name)
                    print("verify start : w %s" % w)
                if a_num is 12:
                    m.append(vip_name)
                    print("verify start : m %s" % m)
                if a_num is 13:
                    n.append(vip_name)
                    print("verify start : n %s" % n)

            if 'verify end' in s:
                a_num += 1
                c_append_flag = True
                # print("verify end balabala")

            if 'novif start' in s:
                novif_append_flag = True
                # print("novif start balabala")

            if 'novif end' in s:
                novif_append_flag = False
                # print("novif end balabala")

            if 'input' in s:
                write_flag = True
            if 'output' in s:
                write_flag = True

            if write_flag is True:
                if novif_append_flag is True:
                    self.novifArray.append(s)
                else:
                    if a_num is 0:
                        a.append(s)
                        # print("novifArray start : a %s" % a)
                    if a_num is 1:
                        b.append(s)
                        # print("novifArray start : b %s" % b)
                    if a_num is 2:
                        c.append(s)
                        # print("novifArray start : c %s" % c)
                    if a_num is 3:
                        d.append(s)
                        # print("novifArray start : d %s" % d)
                    if a_num is 4:
                        e.append(s)
                        # print("novifArray start : e %s" % e)
                    if a_num is 5:
                        f.append(s)
                        # print("novifArray start : f %s" % f)
                    if a_num is 6:
                        g.append(s)
                        # print("novifArray start : g %s" % g)
                    if a_num is 7:
                        h.append(s)
                        # print("novifArray start : h %s" % h)
                    if a_num is 8:
                        # i.append(s)
                        # # print("novifArray start : i %s" % i)
                        v.append(s)
                        # print("novifArray start : v %s" % v)
                    if a_num is 9:
                        j.append(s)
                        # print("novifArray start : j %s" % j)
                    if a_num is 10:
                        k.append(s)
                        # print("novifArray start : k %s" % k)
                    if a_num is 11:
                        # l.append(s)
                        # # print("novifArray start : l %s" % l)
                        w.append(s)
                        # print("novifArray start : w %s" % w)
                    if a_num is 12:
                        m.append(s)
                        # print("novifArray start : m %s" % m)
                    if a_num is 13:
                        n.append(s)
                        # print("novifArray start : n %s" % n)
                write_flag = False

                if c_append_flag is True:
                    if a_num is 1:
                        self.InArray.append(a)
                        # print("InArray start : a %s" % a)
                    if a_num is 2:
                        self.InArray.append(b)
                        # print("InArray start : b %s" % b)
                    if a_num is 3:
                        self.InArray.append(c)
                        # print("InArray start : c %s" % c)
                    if a_num is 4:
                        self.InArray.append(d)
                        # print("InArray start : d %s" % d)
                    if a_num is 5:
                        self.InArray.append(e)
                        # print("InArray start : e %s" % e)
                    if a_num is 6:
                        self.InArray.append(f)
                        # print("InArray start : f %s" % f)
                    if a_num is 7:
                        self.InArray.append(g)
                        # print("InArray start : g %s" % g)
                    if a_num is 8:
                        self.InArray.append(h)
                        # print("InArray start : h %s" % h)
                    if a_num is 9:
                        # self.InArray.append(i)
                        # # print("InArray start : i %s" % i)
                        self.InArray.append(v)
                        # print("InArray start : v %s" % v)
                    if a_num is 10:
                        self.InArray.append(j)
                        # print("InArray start : j %s" % j)
                    if a_num is 11:
                        self.InArray.append(k)
                        # print("InArray start : k %s" % k)
                    if a_num is 12:
                        # elf.InArray.append(l)
                        # # print("InArray start : l %s" % l)
                        self.InArray.append(w)
                        # print("InArray start : w %s" % w)
                    if a_num is 12:
                        self.InArray.append(m)
                        # print("InArray start : m %s" % m)
                    if a_num is 14:
                        self.InArray.append(n)
                        # print("InArray start : n %s" % n)
                    c_append_flag = False

        file_in.close()

#    def usage():
#        msg="""read rtl top script,need input rtl file *.sv """
#        print(msg)


def main(Infile, InArray, novifArray, module_name):
    print("CaptureTbInfo.main")
    cap_tb_info = capture_tb_info(Infile, InArray, novifArray, module_name)
    cap_tb_info.capture_tbinfo()


# if __name__ == "__main__":
if __name__ == 'CaptureTbInfo':
    print("CaptureTbInfo")
    if len(sys.argv) == 0:
        sys.exit(1)
    arg_index = 1
    Infile = ''
    InArray = []
    novifArray = []
    module_name = []
    # print("hihihihihihihihihihihihih")
    # print(sys.argv)
    # print(sys.argv[0])
    # print(sys.argv[1])
    # print(sys.argv[2])
    # print(sys.argv[3])
    # print(sys.argv[4])
    # print(len(sys.argv))
    # print(arg_index)
    while arg_index < len(sys.argv):
        arg = sys.argv[arg_index]
        # ###if "*.sv" in arg:
        # ###    filename=arg
        if arg == '-infile':
            arg_index += 1
            Infile = sys.argv[arg_index]
        arg_index += 1
        # if arg=="-o":
        #    arg_index += 1
        #    Outfile=sys.argv[arg_index]
        #    print(arg_index)
        #    print(Outfile)
        #    arg_index
    main(Infile, InArray, novifArray, module_name)
    print("Show the InArray in CaptureTbInfo.py:")
    print(InArray)
    print('\n\n')
    print("Show the novifArray in CaptureTbInfo.py:")
    print(novifArray)
    print('\n\n')
    print("Show the module_name in CaptureTbInfo.py:")
    print(module_name)
    print('\n\n')
    print("Show the uvc and vip name in CaptureTbInfo.py:")
    for i in range(len(InArray)):
        if InArray[i][0][0:3] == 'ahb':
            ahb_info = InArray[i][0].split("#", 2)
            print(ahb_info)
