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


def modify_cr_i(year,dir):
    midified_file = []
    for maindir, subdir, file_name_list in os.walk(dir):
        for filename in file_name_list:
            # print(filename)
            newdir = os.path.join(maindir, filename)
            if os.path.splitext(filename)[1] == ".c" or os.path.splitext(filename)[1] == ".h":
                print(newdir)
                with open(newdir, "r", encoding="utf-8") as f1, open("%s.bak" % newdir, "w", encoding="utf-8") as f2:
                    for num, line in enumerate(f1):
                        if re.match(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d-\d\d\d\d', line):
                            print(line)
                            line = re.sub(r'\d\d\d\d-\d\d\d\d', str(year), line)
                            f2.write(line)
                            midified_file.append(newdir)
                        elif re.match(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d\s+$', line):
                            print(line)
                            line = re.sub(r'\d\d\d\d', str(year), line)
                            f2.write(line)
                            midified_file.append(newdir)
                        else:
                            f2.write(line)
                os.remove(newdir)                            # replace the old file with modified on.
                os.rename("%s.bak" % newdir, newdir)
            else:
                continue
    print("All file modified is:")
    print(midified_file)
    print("Total num is : %d" % len(midified_file))


def modify_cr(year, dirname):
    midified_file = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            # print(filename)
            newdir = os.path.join(maindir, filename)
            if os.path.splitext(filename)[1] == ".c" or os.path.splitext(filename)[1] == ".h":
                print(newdir)
                with open(newdir, "r", encoding="utf-8") as f1, open("%s.bak" % newdir, "w", encoding="utf-8") as f2:
                    for num, line in enumerate(f1):
                        if re.match(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d-\d\d\d\d', line):
                            print(line)
                            line = re.sub(r'-\d\d\d\d', '-'+str(year), line)
                            f2.write(line)
                            midified_file.append(newdir)
                        elif re.match(r'^\s*\*+\s+Copyright\sFUJITSU\sLIMITED\s*\d\d\d\d', line):
                            print(line)
                            findstr = re.findall(r'(\d\d\d\d)', line)
                            print(findstr)
                            if findstr[0] < str(year):
                                line = re.sub(r'\d\d\d\d', findstr[0]+'-'+str(year), line)
                                f2.write(line)
                                midified_file.append(newdir)
                            else:
                                f2.write(line)
                        else:
                            f2.write(line)
                os.remove(newdir)                           # replace the old file with modified on.
                os.rename("%s.bak" % newdir, newdir)
            else:
                continue
    print("All file modified is:")
    print(midified_file)
    print("Total num is : %d" % len(midified_file))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvc:i:", ["version", "help"])
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
        else:
            usage()
            sys.exit()

    logging.info("Checking is done.")


if __name__ == "__main__":
    main(sys.argv[1:])