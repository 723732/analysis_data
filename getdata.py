import sys, os, subprocess, re

def mkdir(input_dir):
    str = input_dir
    project_name = str.split('\\')[-1]
    output_path = 'E:\output\\' + project_name

    isExists = os.path.exists(output_path)

    if not isExists:
      os.makedirs(output_path)


    return output_path


def getcommit_id(input_dir, output_path):
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
    path = re.sub('changefile.txt', '', changefile_path)
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

  
def getchange_file(input_dir, commit_id):
    lines = []

    with open(commit_id) as file_object:
      #将各行存储在字典列表中
      for line in file_object:
        com_id = line.split(':')[1]
        parent_id = line.split(':')[2]
        explain = line.lstrip('fotmat:' + com_id + ':' + parent_id + ':')
        new_line = {'id': com_id, 'parent_id': parent_id, 'explain': explain}

        lines.append(new_line)

      for index in range(len(lines)-1):
        #print(index,lines[index+1]['id'])
        parent = re.sub(' ', '-', lines[index]['parent_id'])
        oldnew_path = commit_id.rstrip('\commit_id.txt') + '\\' + str(index+1) + '_' + parent + '_' + lines[index]['id']
        isExists = os.path.exists(oldnew_path)

        if not isExists:
          os.makedirs(oldnew_path)
        
        output_file = oldnew_path + '\\changefile.txt'
        cmd = 'cd ' + input_dir + '&' +'git diff ' + lines[index]['parent_id'] + ' ' + lines[index]['id'] + ' > ' + output_file
        py_path = os.path.dirname(__file__)
        subprocess.Popen(cmd, shell = True, cwd = py_path)
    

if __name__ == '__main__':

  print ("文件夹名：",sys.argv[1])
  input_dir = sys.argv[1]
  # input_dir = 'E:\\test\\2_compile-testing'

  output_path = mkdir(input_dir)

  print ("output_path：",output_path)
  commit_id = getcommit_id(input_dir, output_path)

  getchange_file(input_dir, commit_id)

  for root, dirs, files in os.walk(output_path):
    #print(files, len(files))
    if files:
      for file1 in files:
        if file1.startswith('changefile'):
          analysis_changefile(root + '\\changefile.txt')

  print(u'生成成功')

