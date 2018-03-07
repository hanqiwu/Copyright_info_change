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
                            findstr = re.findall(r'(\d\d\d\d)', line)
                            print(findstr)
                            if findstr[0] < str(year):
                                line = re.sub(r'\d\d\d\d', findstr[0]+'-'+str(year), line)
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
                                                    else:
                                                        i = re.sub(r'\d+\W\d+\W\d+', str(date), i)
                                                        mocified_cr_content.append(i)                    # only retain one change log and change the time.
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
                os.remove(newdir)  # replace the old file with modified on.
                os.rename("%s.bak" % newdir, newdir)
    print("All file modified is:")
    print(modified_file)
    print("Total num is : %d" % len(modified_file))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvtc:i:", ["version", "help"])
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
            usage()
            sys.exit()
        elif op == "-t":
            modify_cl_i(argv[1], argv[2])
        else:
            usage()
            sys.exit()

    logging.info("Checking is done.")


if __name__ == "__main__":
    main(sys.argv[1:])
 #   modify_cl_i('2018-2-10', 'test')