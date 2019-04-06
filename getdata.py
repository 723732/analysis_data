import sys, os, subprocess, re
import threading
from multiprocessing import Pool
import mythread
import json

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
    edge = {}   
    node = changefile_path.split('\\')[-2]
    from_node = node.split('_')[-2]
    to_node = node.split('_')[-1]
    edge['from_node'] = from_node
    edge['to_node'] = to_node
    edge['change'] = []
    newchange = {'from_filename': '', 'to_filename': '', 'type': '', 'line_num': ''}

    # i = 0
    filename = changefile_path.split('\\')[-1]
    path = re.sub(filename, '', changefile_path)
    with open(changefile_path, 'r', encoding='UTF-8') as file_object:
        lines = file_object.readlines()

    for line in lines:
        # print(line)
        if line.startswith('diff --'):
            # file_name = line.split('/')[-1].split('.')[0] + '.txt'
            file_name = line.split('/')[-1]
            if '.' in file_name:
              file_name = file_name.split('.')[0] + '.txt'
            else:
              file_name = file_name.rstrip('\n') + '.txt'
            file_path = path + file_name
            with open(file_path, 'w', encoding='UTF-8') as file_object1:
                file_object1.write(line)
            
            if newchange['from_filename'] != '' or newchange['type'] != '' or newchange['line_num'] != '' or newchange['to_filename'] != '':
              edge['change'].append(newchange)
              newchange = {'from_filename': '', 'to_filename': '', 'type': '', 'line_num': ''}
        else:
            with open(file_path, 'a', encoding='UTF-8') as file_object1:
                file_object1.write(line)
            if line.startswith('---'):
              newchange['from_filename'] = line.split(' ')[-1].rstrip('\n')
            elif line.startswith('+++'):
              newchange['to_filename'] = line.split(' ')[-1].rstrip('\n')
            elif line.startswith('new') or line.startswith('rename from') or line.startswith('copy from') or line.startswith('deleted'):
              newchange['type'] = line.split(' ')[0]
              if line.startswith('rename from'):
                newchange['from_filename'] = line.split(' ')[-1].rstrip('\n')
            elif line.startswith('@@'):
              newchange['line_num'] = line
            elif line.startswith('rename to'):
              newchange['to_filename'] = line.split(' ')[-1].rstrip('\n')
            # if line.startswith('rename from'):
            #     i = i + 1
            #     path_from = line.split(' ')[-1]
            #     if i == 1:
            #       with open(path + 'rename.txt', 'w', encoding='UTF-8') as file_object2:
            #         file_object2.write(str(i) + ':' + path_from)
            #     else:
            #       with open(path + 'rename.txt', 'a', encoding='UTF-8') as file_object2:
            #         file_object2.write(str(i) + ':' + path_from)
            # elif line.startswith('rename to'):
            #     path_to = line.split(' ')[-1]
            #     with open(path + 'rename.txt', 'a', encoding='UTF-8') as file_object2:
            #         file_object2.write(str(i) + ':' + path_to)
    edge['change'].append(newchange)

    return edge


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
  changefile_list = []
  for index in range(start_num, end_num):
    #print(index,lines[index+1]['id'])
    parent = re.sub(' ', '-', id_list[index]['parent_id'])
    oldnew_path = output_path + '\\' + str(index+1) + '_' + parent + '_' + id_list[index]['id']

    mkdir(oldnew_path)
    
    py_path = os.path.dirname(__file__)
    if ' ' in id_list[index]['parent_id']:
      path1 = oldnew_path + '\\' + str(index+1) + '_' + id_list[index]['parent_id'].split(' ')[0] + '_' + id_list[index]['id']
      path2 = oldnew_path + '\\' + str(index+1) + '_' + id_list[index]['parent_id'].split(' ')[-1] + '_' + id_list[index]['id']
      mkdir(path1)
      mkdir(path2)
      output_file1 = path1 + '\\changefile.txt'
      changefile_list.append(output_file1)
      output_file2 = path2 + '\\changefile.txt'
      changefile_list.append(output_file2)
      cmd1 = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'].split(' ')[0] + ' ' + id_list[index]['id'] + ' > ' + output_file1
      subprocess.Popen(cmd1, shell = True, cwd = py_path)

      cmd2 = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'].split(' ')[-1] + ' ' + id_list[index]['id'] + ' > ' + output_file2
      subprocess.Popen(cmd2, shell = True, cwd = py_path)

    else:
      output_file = oldnew_path + '\\changefile.txt'
      changefile_list.append(output_file)
      cmd = 'cd ' + input_dir + '&' +'git diff ' + id_list[index]['parent_id'] + ' ' + id_list[index]['id'] + ' > ' + output_file            
      subprocess.Popen(cmd, shell = True, cwd = py_path)

  return changefile_list

if __name__ == '__main__':
  edge_json = {}
  edge_json['edge'] = []

  print ("文件夹名：",sys.argv[1])
  input_dir = sys.argv[1]
  # input_dir = 'E:\\test\\2_compile-testing'

  project_name = input_dir.split('\\')[-1]
  output_path = 'E:\\output\\' + project_name

  mkdir(output_path)

  print ("output_path：",output_path)
  commitId_file = getcommitId_file(input_dir, output_path)
  commitId_list = getcommit_id(commitId_file)

  changefile_list = getchange_file(0, len(commitId_list), commitId_list, output_path)
  print(u'生成filechange')

  # for index in range(len(changefile_list)//2):
  #   # analysis_changefile(changefile_list[index])
  #   # analysis_changefile(changefile_list[index + len(changefile_list)//2])
  #   # t1 = threading.Thread(target = analysis_changefile, args = [changefile_list[index]])
  #   # t2 = threading.Thread(target = analysis_changefile, args = [changefile_list[index + len(changefile_list)//2]])
  #   t1 = mythread.MyThread(analysis_changefile, args = [changefile_list[index]])
  #   t2 = mythread.MyThread(analysis_changefile, args = [changefile_list[index + len(changefile_list)//2]])
  #   t1.start()
  #   t2.start()

  #   t1.join()
  #   t2.join()
  #   edge_json['edge'].append(t1.get_result())
  #   edge_json['edge'].append(t2.get_result())

  th = []
  m = len(changefile_list)//2
  for num in range(0, 2):
    for index in range(num*m, (num+1)*m):
      t1 = mythread.MyThread(analysis_changefile, args = [changefile_list[index]])
      th.append(t1)
      t1.start()

    for t1 in th:
      t1.join()
      print(threading.active_count())
      edge_json['edge'].append(t1.get_result())
      # print(t1.get_result())

  with open(output_path +"\\edge.json", 'w', encoding='UTF-8') as file_object:
    json.dump(edge_json, file_object, indent=4)
  print(u'生成成功',len(changefile_list))

