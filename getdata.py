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
        cmd = 'cd ' + input_dir + '&' +'git diff ' + lines[index]['parent_id'] + ' ' + lines[index]['id'] + ' --name-only > ' + output_file
        py_path = os.path.dirname(__file__)
        p = subprocess.Popen(cmd, shell = True, cwd = py_path)
        p.wait()

        if os.path.exists(output_file):
          if os.path.getsize(output_file) > 0:
            with open(output_file) as file_object1:
              for line1 in file_object1:
                #每一行都是发生改变文件的具体路径
                output_file1 = oldnew_path + '\\' + line1.split('/')[-1].split('.')[0] + '.txt'
                cmd1 = 'cd ' + input_dir + '&' + 'git diff ' + lines[index]['parent_id'] + ' ' + lines[index]['id'] + ' -- ' + line1.rstrip() + ' > ' + output_file1
                # print(cmd1)
                py_path =  os.path.dirname(__file__)
                p = subprocess.Popen(cmd1, shell = True, cwd = py_path)
                # p.wait()
    

if __name__ == '__main__':

  print ("文件夹名：",sys.argv[1])
  input_dir = sys.argv[1]
  # input_dir = 'E:\python_work\\test\\3_logstash-logback-encoder'

  output_path = mkdir(input_dir)

  print ("output_path：",output_path)
  commit_id = getcommit_id(input_dir, output_path)

  getchange_file(input_dir, commit_id)
  print(u'生成成功')

