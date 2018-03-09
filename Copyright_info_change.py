# -*- coding: utf-8 -*-
import sys,getopt
import re
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def usage():
    print("test")


def version():
    print(1.01)


def modify_cr_i(year, dir):
    modified_file = []
    for maindir, subdir, file_name_list in os.walk(dir):
        for filename in file_name_list:
            # print(filename)
            newdir = os.path.join(maindir, filename)
            if os.path.splitext(filename)[1] == ".c" or os.path.splitext(filename)[1] == ".h":
                print(newdir)
                with open(newdir, "r", encoding="utf-8") as f1, open("%s.bak" % newdir, "w", encoding="utf-8") as f2:
                    for num, line in enumerate(f1):
                        if re.search(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d-\d\d\d\d', line):
                            print(line)
                            line = re.sub(r'\d\d\d\d-\d\d\d\d', str(year), line)
                            f2.write(line)
                            modified_file.append(newdir)
                        elif re.search(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d\s+$', line):
                            print(line)
                            line = re.sub(r'\d\d\d\d', str(year), line)
                            f2.write(line)
                            modified_file.append(newdir)
                        else:
                            f2.write(line)
                os.remove(newdir)                            # replace the old file with modified on.
                os.rename("%s.bak" % newdir, newdir)
            else:
                continue
    print("All file modified is:")
    print(modified_file)
    print("Total num is : %d" % len(modified_file))


def modify_cr(year, dirname):
    modified_file = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            # print(filename)
            newdir = os.path.join(maindir, filename)
            if os.path.splitext(filename)[1] == ".c" or os.path.splitext(filename)[1] == ".h":
                print(newdir)
                with open(newdir, "r", encoding="utf-8") as f1, open("%s.bak" % newdir, "w", encoding="utf-8") as f2:
                    for num, line in enumerate(f1):
                        if re.search(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d-\d\d\d\d', line):
                            print(line)
                            line = re.sub(r'-\d\d\d\d', '-'+str(year), line)
                            f2.write(line)
                            modified_file.append(newdir)
                        elif re.search(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d', line):
                            print(line)
                            findstr = re.search(r'(\d\d\d\d)', line)
                            print(findstr)
                            if findstr[0] < str(year):
                                line = re.sub(r'\d\d\d\d', findstr+'-'+str(year), line)
                                f2.write(line)
                                modified_file.append(newdir)
                            else:
                                f2.write(line)
                        else:
                            f2.write(line)
                os.remove(newdir)                           # replace the old file with modified on.
                os.rename("%s.bak" % newdir, newdir)
            else:
                continue
    print("All file modified is:")
    print(modified_file)
    print("Total num is : %d" % len(modified_file))


def modify_cl_i(date, dirname):
    modified_file = []

    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            cr_content = []
            mocified_cr_content = []
            find_cr = 0
            cl_flag = 0
            log_num = 0
            modified_flag = 0
            # print(filename)
            newdir = os.path.join(maindir, filename)
            if os.path.splitext(filename)[1] == ".c" or os.path.splitext(filename)[1] == ".h":
                print(newdir)
                with open(newdir, "r", encoding="utf-8") as f1, open("%s.bak" % newdir, "w", encoding="utf-8") as f2:
                    for num, line in enumerate(f1):
                        if modified_flag == 0:
                            if re.search(r'/\*\*\*\*\*+', line) and find_cr == 0:
                                find_cr = 1
                                cr_content.append(line)
                                continue
                            if find_cr == 1:
                                if re.search(r'\*\s+Date\s+Who\s+What', line) and cl_flag == 0:
                                    cl_flag = 1
                                    cr_content.append(line)
                                    continue
                                if cl_flag == 1:
                                    if re.search(r'\*\s+\d+\W\d+\W\d+', line):
                                        cr_content.append(line)
                                        log_num += 1
                                        continue
                                    else:
                                        if re.search(r'\s*\*\*\*\*\*+', line):
                                            find_cr = 0
                                            cl_flag = 0
                                            cr_content.append(line)
                                            # print("CR content is:")
                                            # for i in cr_content:
                                            #     print(i)

                                            for i in cr_content:
                                                if re.search(r'\*\s+Date\s+Who\s+What', i):
                                                    cl_flag = 1
                                                    mocified_cr_content.append(i)
                                                    continue
                                                if cl_flag == 1:
                                                    if re.search(r'\*\s+\d+\W\d+\W\d+', i) and log_num > 1:
                                                        log_num -= 1
                                                        continue
                                                    elif log_num == 1:
                                                        i = re.sub(r'\d+\W\d+\W\d+', str(date), i)
                                                        findstr = re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+)(.*)', i)
                                                        temp = list(findstr[0])
                                                        temp[2] = 'Create\n'
                                                        i = temp[0] + temp[1] + temp[2]
                                                        mocified_cr_content.append(i)                    # only retain one change log and change the time.
                                                        log_num -= 1
                                                    else:
                                                        mocified_cr_content.append(i)
                                                else:
                                                    mocified_cr_content.append(i)
                                            for i in mocified_cr_content:
                                                f2.write(i)
                                            modified_flag = 1
                                            # print("Modified CR content is:")
                                            # for i in mocified_cr_content:
                                            #     print(i)
                                        else:
                                            cr_content[-1] = cr_content[-1] + line  # one change log has mutiple line.
                                            continue
                                else:
                                    cr_content.append(line)
                            else:
                                f2.write(line)
                        else:
                            f2.write(line)
                    modified_file.append(newdir)
                # os.remove(newdir)  # replace the old file with modified on.
                # os.rename("%s.bak" % newdir, newdir)
    print("All file modified is:")
    print(modified_file)
    print("Total num is : %d" % len(modified_file))


def modify_cl(date, str, hash1, hash2, repo):

    modified_file = []
    folder1 = 'lastrelease\\'
    folder2 = 'newrelease\\'
    checked_path = ['FLI/Source/FLI/SC/BasePort/phy_kernel', 'FLI/Source/FLI/SC/BasePort/test/P2_test']
    filelist = []
    start_path = os.path.abspath('.') + '\\'

    if os.path.exists(folder1):
        os.system('rd/s/q %s' % folder1)
        os.system('mkdir %s' % folder1)
    else:
        os.system('mkdir %s' % folder1)

    if os.path.exists(folder2):
        os.system('rd/s/q %s' % folder2)
        os.system('mkdir %s' % folder2)
    else:
        os.system('mkdir %s' % folder2)

    os.system('git clone %s %s ' %(repo, folder1))
    os.system('git clone %s %s ' %(repo, folder2))

    os.chdir(folder1)
    os.system('git checkout -f %s' % hash1)

    os.chdir(start_path+folder2)
    os.system('git checkout -f %s' % hash2)

    os.system('git config diff.renameLimit 99999')

    os.system('git diff %s %s  --name-only  >..\\filelist.txt ' % (hash1, hash2))

    os.chdir(start_path)

    with open('filelist.txt', "r", encoding="utf-8") as file:
        for num, line in enumerate(file):
            for i in checked_path:
                if i in line:
                    if os.path.splitext(i)[1] == ".c" or os.path.splitext(i)[1] == ".h":
                        filelist.append(line)
                        break
                else:
                    continue

    for num, i in enumerate(filelist):
        filelist[num] = i.replace('/', '\\')

    for i in filelist:
        if os.path.exists(folder1+i):
            folder1_cr = []      #save the copyright content of last release file
            folder2_cr = []      #save the copyright content of new release file
            modified_cr = []     #save the modified copyright content of new release file
            log_num1 = 0         #save change log num
            log_num2 = 0
            find_cr1 = 0         #find copyright content or not. Judge whether save the content.
            find_cr2 = 0
            cl_flag1 = 0         #find change log or not. Judge whether need to hanlde the line with special logic.
            cl_flag2 = 0
            modified_flag2 = 0    #Whehter the copyright modification is done.
            special_list = []

            with open(folder1+i, "r", encoding="utf-8") as file1:      #fetch the copyright content from last release file.
                for num, line in enumerate(file1):
                    if re.search(r'/\*\*\*\*\*+', line) and find_cr1 == 0:
                        find_cr = 1
                        folder1_cr.append(line)
                        continue
                    if find_cr == 1:
                        if re.search(r'\*\s+Date\s+Who\s+What', line) and cl_flag1 == 0:
                            cl_flag = 1
                            folder1_cr.append(line)
                            continue
                        if cl_flag1 == 1:
                            if re.search(r'\*\s+\d+\W\d+\W\d+', line):
                                folder1_cr.append(line)
                                log_num1 += 1
                            else:
                                if re.search(r'\s*\*\*\*\*\*+', line):
                                    find_cr1 = 0
                                    cl_flag1 = 0
                                    folder1_cr.append(line)
                                    break
                                else:
                                    folder1_cr[-1] = folder1_cr[-1] + line  # one change log has multiple line.
                        else:
                            folder1_cr.append(line)

            # Beginning to modify new release copyright content.
            with open(folder2 + i, "r", encoding="utf-8") as f1, open("%s.bak" % folder2 + i, "w", encoding="utf-8") as f2:
                for num, line in enumerate(f1):
                    if modified_flag2 == 0:
                        if re.search(r'/\*\*\*\*\*+', line) and find_cr2 == 0:
                            find_cr2 = 1
                            folder2_cr.append(line)
                            continue
                        if find_cr2 == 1:
                            if re.search(r'\*\s+Date\s+Who\s+What', line) and cl_flag2 == 0:
                                cl_flag2 = 1
                                folder2_cr.append(line)
                                continue
                            if cl_flag2 == 1:
                                if re.search(r'\*\s+\d+\W\d+\W\d+', line):
                                    folder2_cr.append(line)
                                    log_num2 += 1
                                else:
                                    if re.search(r'\s*\*\*\*\*\*+', line):      # Find the last line of copyright, begin to handle content.
                                        find_cr1 = 0
                                        cl_flag1 = 0
                                        folder2_cr.append(line)
                                        f1list = list((re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+.*)', folder1_cr[-2]))[0])
                                        f2list = list((re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+.*)', folder2_cr[-2]))[0])
                                        f2list_1 = list((re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+.*)', folder2_cr[-3]))[0])
                                        if f1list[1] == f2list[1]:
                                            tstr = re.sub(r'\d+\W\d+\W\d+', str(date), folder1_cr[-2])
                                            findstr = re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+)(.*)', tstr)
                                            teml = list(findstr[0])
                                            teml[2] = str+'\n'
                                            folder1_cr.insert(-2, teml[0] + teml[1] + teml[2])
                                            for cr in folder1_cr:
                                                f2.write(cr)
                                                modified_flag2 = 1
                                                modified_file.append(i)
                                        elif f1list[1] == f2list_1[1]:
                                            tstr = re.sub(r'\d+\W\d+\W\d+', str(date), folder2_cr[-3])
                                            folder1_cr.insert(-2, tstr)
                                            for cr in folder1_cr:
                                                f2.write(cr)
                                                modified_flag2 = 1
                                                modified_file.append(i)
                                        else:
                                            special_list.append(i)




                                    else:
                                        folder2_cr[-1] = folder2_cr[-1] + line  # one change log has multiple line.
                            else:
                                folder2_cr.append(line)

                    else:
                        f2.write(line)

            os.remove(folder2 + i)  # replace the old file with modified on.
            os.rename("%s.bak" % folder2 + i, folder2 + i)


        else:      #New file should be handled as first release.
            cr_content = []
            mocified_cr_content = []
            log_num = 0
            find_cr = 0
            modified_flag = 0
            with open(folder2+i, "r", encoding="utf-8") as f1, open("%s.bak" % folder2+i, "w", encoding="utf-8") as f2:
                for num, line in enumerate(f1):
                    if modified_flag == 0:
                        if re.search(r'/\*\*\*\*\*+', line) and find_cr == 0:
                            find_cr = 1
                            cr_content.append(line)
                            continue
                        if find_cr == 1:
                            if re.search(r'\*\s+Date\s+Who\s+What', line) and cl_flag == 0:
                                cl_flag = 1
                                cr_content.append(line)
                                continue
                            if cl_flag == 1:
                                if re.search(r'\*\s+\d+\W\d+\W\d+', line):
                                    cr_content.append(line)
                                    log_num += 1
                                    continue
                                else:
                                    if re.search(r'\s*\*\*\*\*\*+', line):
                                        find_cr = 0                       #reset the flags
                                        cl_flag = 0
                                        cr_content.append(line)
                                        # print("CR content is:")
                                        # for i in cr_content:
                                        #     print(i)

                                        for i in cr_content:
                                            if re.search(r'\*\s+Date\s+Who\s+What', i):
                                                cl_flag = 1
                                                mocified_cr_content.append(i)
                                                continue
                                            if cl_flag == 1:
                                                if re.search(r'\*\s+\d+\W\d+\W\d+', i) and log_num > 1:
                                                    log_num -= 1
                                                    continue
                                                elif log_num == 1:
                                                    i = re.sub(r'\d+\W\d+\W\d+', str(date), i)
                                                    findstr = re.findall(r'(^\s*\*\s+\S+\s+)(\S+\s+)(.*)', i)
                                                    temp = list(findstr[0])
                                                    temp[2] = 'Create\n'
                                                    i = temp[0] + temp[1] + temp[2]
                                                    mocified_cr_content.append(
                                                        i)  # only retain one change log and change the time.
                                                    log_num -= 1
                                                else:
                                                    mocified_cr_content.append(i)
                                            else:
                                                mocified_cr_content.append(i)
                                        for i in mocified_cr_content:
                                            f2.write(i)
                                        modified_flag = 1
                                        # print("Modified CR content is:")
                                        # for i in mocified_cr_content:
                                        #     print(i)
                                    else:
                                        cr_content[-1] = cr_content[-1] + line  # one change log has multiple line.
                                        continue
                            else:
                                cr_content.append(line)
                        else:
                            f2.write(line)
                    else:
                        f2.write(line)
                modified_file.append(i)
                os.remove(folder2+i)  # replace the old file with modified on.
                os.rename("%s.bak" % folder2+i, folder2+i)

    print("All file modified is:")
    print(modified_file)
    print("Total num is : %d" % len(modified_file))
    print("Need to modify manually is:")
    print(special_list)
    print("Total num is : %d" % len(special_list))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvlcim", ["version", "help"])
    except getopt.GetoptError:
        print("for help use --help or -h")
        sys.exit(2)
    if args == [] and opts == []:
        usage()
        sys.exit()

    for op, value in opts:
        if op == "-h" or op == "--help":
            usage()
            sys.exit()
        elif op == "--version" or op == "-v":
            version()
            sys.exit()
        elif op == "-c":
            modify_cr(argv[1], argv[2])
        elif op == "-i":
            modify_cr_i(argv[1], argv[2])
        elif op == "-l":
            modify_cl_i(argv[1], argv[2])
        elif op == "-m":
            modify_cl(argv[1], argv[2], argv[3], argv[4], argv[5])
        else:
            usage()
            sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
 #   modify_cl_i('2018-2-10', 'test')
 #   modify_cl('2018-2-10', 'second release', 'abdced', 'agdsed', 'http://12345')