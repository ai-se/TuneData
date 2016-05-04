from __future__ import print_function, division
import pdb
import sys
from os.path import join,isfile
from os import listdir


def combine(path="../result/20160309"):
    '''
    :param path: a str path, which denotes all the results from HPC including all tuning goals
    :return: dic of paths of those saved files, key is the goal, and value is the src
    '''
    files = [ join(path,i)for i in listdir(path) if isfile(join(path,i)) and ".DS" not in i]
    to_files = {}
    saved_files= {}
    for each in files:
        goal = each[each.rindex("_")+1:]
        content = open(each,"rb")
        to_files[goal] = to_files.get(goal,[])+content.readlines()
        content.close()
    for key, val in to_files.iteritems():
        file_to_save = path[path.rindex("/")+1:]+"_all_"+key
        f = open(file_to_save,"w")
        f.write("".join(val))
        f.close()
        saved_files[key]=file_to_save
    return saved_files

if __name__ == "__main__":
    print(combine())