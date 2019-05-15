import shutil
import os


def collectFile(rootDir, copyfile_path):
    with open(rootDir + '\\varient_null.txt') as file_object:
        lines = file_object.readlines()

    s = set()
    for line in lines:
        subject_name = line.split('\\')[-4]
        sversion1 = line.split('\\')[-3].split('-vs-')[0]
        sversion2 = line.split('\\')[-3].split('-vs-')[1]
        part2 = line.split('\\')[-2].replace('_', '\\')
        partpath = part2.replace('\\' + part2.split('\\')[-1], '.java')
        java_file = partpath.split('\\')[-1]
        java_name = java_file.split('.')[0]
        notest_java = partpath.replace('Test', '')
        notestjava_file = notest_java.split('\\')[-1]
        notestjava_name = notestjava_file.split('.')[0]     
        path1 = subject_name + '\\' + sversion1 + '\\' + 'test\\' + partpath
        path2 = subject_name + '\\' + sversion2 + '\\' + 'test\\' + partpath
        path3 = subject_name + '\\' + sversion1 + '\\' + 'src\\' + notest_java
        path4 = subject_name + '\\' + sversion1 + '\\' + 'src\\' + notest_java
        
        if path1 not in s:
            shutil.copy(copyfile_path + path1, rootDir)
            os.rename(rootDir + '\\' + java_file, rootDir + '\\' + java_name + 'new.java')
        if path2 not in s:
            shutil.copy(copyfile_path + path2, rootDir)
        if path3 not in s and os.path.exists(copyfile_path + path3):
            shutil.copy(copyfile_path + path3, rootDir)
            os.rename(rootDir + '\\' + notestjava_file, rootDir + '\\' + notestjava_name + 'new.java')
        if path4 not in s and os.path.exists(copyfile_path + path4):
            shutil.copy(copyfile_path + path4, rootDir)

        s.add(path1)
        s.add(path2)
        s.add(path3)
        s.add(path4)


path = 'C:\\Users\\Y_sun\\Desktop\\2019\\experiment-data\\test-repair1\\varient_fail'
path1= "C:\\Users\\Y_sun\\Desktop\\2019\\experiment-data\\repair-subjects\\"
collectFile(path, path1)