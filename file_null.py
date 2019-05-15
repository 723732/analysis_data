import os


def findFile_null(rootDir):
    # 获取空文件，即文件大小为0
    f1 = open(rootDir + '\\varient_null.txt', 'w')
    for dirpath, dirname, filenames in os.walk(rootDir):
        for filename in filenames:
            if filename == "candidates-list.txt":
                path = os.path.join(dirpath, filename)
                size = os.path.getsize(path)
                if size == 0:
                    f1.write(path + '\n')
    f1.close()


findFile_null("C:\\Users\\Y_sun\\Desktop\\2019\\experiment-data\\test-repair1")