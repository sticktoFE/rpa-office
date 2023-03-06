import subprocess
import os,re,sys
def alter(file,old_str,new_str):
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(re.sub(old_str,new_str,line))
            #print(new_str)
    os.remove(file)
    os.rename("%s.bak" % file, file)

curDir = os.getcwd().replace("\\","/")
print(curDir)
print(sys.executable)
piplist = subprocess.run('jupyter kernelspec list',universal_newlines=True,stdout=subprocess.PIPE)    # 更改为阿里云的源 https://mirrors.aliyun.com/pypi/simple/
if piplist.returncode != 0:
    print('获取更新列表失败，请重新运行！')
    exit(0)
else:
    if len(piplist.stdout) == 0:
        print('所有的库都是最新的，无需更新。')
        exit(0)
    else:
        #Available kernels:\n  python3    E:\\Miniconda3\\envs\\dl\\share\\jupyter\\kernels\\python3\n
        g_list = piplist.stdout.split('\n')
        print(g_list)
        past_list = []
        for i in g_list[1:]:
            #print('jupyer kernel.json目录为：\n', i)
            i = i.strip()
            if len(i)>0:
                #print(f'xxxx--{i}--')
                past_list.append(i.split()[1])
        #print('jieg',past_list)
        fail_list = []
        for path in past_list:
            print(f'------开始替换：{path}……')
            file1 = path+ 	"\\kernel.json"
            oldStr = r"\"(\w{1}:/|\w{1}:\\).*"
            newStr = "\""+sys.executable+"\""
            print(oldStr)
            print(newStr)
            alter(file1, oldStr, newStr)