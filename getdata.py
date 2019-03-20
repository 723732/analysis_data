import sys, os, subprocess, re
import threading

def mkdir(dir_path):
    isExists = os.path.exists(dir_path)
    if not isExists:
      os.makedirs(dir_path)


def getcommitId_file(input_dir, output_path):
    # str = input_dir
    # output_path = str.split('\\')[-1]
    output_file = output_path + '\\commit_id.txt'
    # cmd = 'cd ' + input_dir +'&' +'git log --pretty=oneline > '+ output_file
    cmd = 'cd ' + input_dir +'&' +'git log --pretty=fotmat:"%h:%p:%s" > '+ output_file
    py_path = os.path.dirname(__file__)

    p = subprocess.Popen(cmd, shell = True, cwd = py_path)
    p.wait()

    return output_file


def analysis_changefile(changefile_path):
    i = 0
    filename = changefile_path.split('\\')[-1]
    path = re.sub(filename, '', changefile_path)
    with open(changefile_path, 'r', encoding='UTF-8') as file_object:
        lines = file_object.readlines()

    for line in lines:
        # print(line)
        if line.startswith('diff --'):
            file_name = line.split('/')[-1].split('.')[0] + '.txt'
            file_path = path + file_name
            with open(file_path, 'w', encoding='UTF-8') as file_object1:
                file_object1.write(line)
        else:
            with open(file_path, 'a', encoding='UTF-8') as file_object1:
                file_object1.write(line)
            if line.startswith('rename from'):
                i = i + 1
                path_from = line.split(' ')[-1]
                if i == 1:
                  with open(path + 'rename.txt', 'w', encoding='UTF-8') as file_object2:
                    file_object2.write(str(i) + ':' + path_from)
                else:
                  with open(path + 'rename.txt', 'a', encoding='UTF-8') as file_object2:
                    file_object2.write(str(i) + ':' + path_from)
            elif line.startswith('rename to'):
                path_to = line.split(' ')[-1]
                with open(path + 'rename.txt', 'a', encoding='UTF-8') as file_object2:
                    file_object2.write(str(i) + ':' + path_to)


def getcommit_id(commitId_file):
  lines = []
  with open(commitId_file) as file_object:
    #将各行存储在字典列表中
    for line in file_object:
      com_id = line.split(':')[1]
      parent_id = line.split(':')[2]
      explain = line.lstrip('fotmat:' + com_id + ':' + parent_id + ':')
      new_line = {'id': com_id, 'parent_id': parent_id, 'explain': explain}

      lines.append(new_line)
  
  return lines

  
def getchange_file(start_num, end_num, id_list, output_path):
  for index in range(start_num, end_num):
    #print(index,lines[index+1]['id'])
    parent = re.sub(' ', '-', id_list[index]['parent_id'])
    oldnew_path = output_path + '\\' + str(index+1) + '_' + parent + '_' + id_list[index]['id']

    mkdir(oldnew_path)
    
    py_path = os.path.dirname(__file__)
    if ' ' in id_list[index]['parent_id']:
      path1 = oldnew_path + '\\' + id_list[index]['parent_id'].split(' ')[0] + '_' + id_list[index]['id']
      path2 = oldnew_path + '\\' + id_list[index]['parent_id'].split(' ')[-1] + '_' + id_list[index]['id']
      mkdir(path1)
      mkdir(path2)
      output_file1 = path1 + '\\changefile.txt'
      output_file2 = path2 + '\\changefile.txt'
      cmd1 = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'].split(' ')[0] + ' ' + id_list[index]['id'] + ' > ' + output_file1
      subprocess.Popen(cmd1, shell = True, cwd = py_path)

      cmd2 = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'].split(' ')[-1] + ' ' + id_list[index]['id'] + ' > ' + output_file2
      subprocess.Popen(cmd2, shell = True, cwd = py_path)
    else:
      output_file = oldnew_path + '\\changefile.txt'
      cmd = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'] + ' ' + id_list[index]['id'] + ' > ' + output_file       
      subprocess.Popen(cmd, shell = True, cwd = py_path)
    

if __name__ == '__main__':

  # print ("文件夹名：",sys.argv[1])
  # input_dir = sys.argv[1]
  input_dir = 'E:\\test\\2_compile-testing'

  project_name = input_dir.split('\\')[-1]
  output_path = 'E:\\output\\' + project_name

  mkdir(output_path)

  print ("output_path：",output_path)
  commitId_file = getcommitId_file(input_dir, output_path)
  commitId_list = getcommit_id(commitId_file)

  # t1 = threading.Thread(target = getchange_file, args = [0, len(commitId_list)//2, commitId_list, output_path])
  # t2 = threading.Thread(target = getchange_file, args = [len(commitId_list)//2, len(commitId_list), commitId_list, output_path])
  # t1.start()
  # t2.start()

  # t1.join()
  # t2.join()
  getchange_file(0, len(commitId_list), commitId_list, output_path)

  changefile_list = []
  for root, dirs, files in os.walk(output_path):
    #print(files, len(files))
    if files:
      for file1 in files:
        if file1.startswith('changefile') and os.path.getsize(root + '\\' + file1) > 0:
          # analysis_changefile(root + '\\' + file1)
          new_changefile = root + '\\' + file1
          changefile_list.append(new_changefile)
  
  # print(changefile_list, len(changefile_list))

  for index in range(len(changefile_list)//2):
    # analysis_changefile(changefile_list[index])
    # analysis_changefile(changefile_list[index + len(changefile_list)//2])
    # t1 = threading.Thread(target = analysis_changefile, args = [changefile_list[index]])
    # t2 = threading.Thread(target = analysis_changefile, args = [changefile_list[index + len(changefile_list)//2]])
    # t1.start()
    # t2.start()

    # t1.join()
    # t2.join()
    print(index, len(changefile_list)//2, len(changefile_list))

  print(u'生成成功')

