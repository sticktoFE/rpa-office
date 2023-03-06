import subprocess
piplist = subprocess.run('../py37/python-3.7.6.amd64/Scripts/pip list --outdated -i https://pypi.tuna.tsinghua.edu.cn/simple',universal_newlines=True,stdout=subprocess.PIPE)    # 更改为阿里云的源 https://mirrors.aliyun.com/pypi/simple/
if piplist.returncode != 0:
    print('获取更新列表失败，请重新运行！')
    exit(0)
else:
    if len(piplist.stdout) == 0:
        print('所有的库都是最新的，无需更新。')
        exit(0)
    else:
        g_list = piplist.stdout.split('\n')
        #print(g_list)
        past_list = []
        for i in g_list[2:]:
            print('过期的库有：\n', i)
            past_list.append(i.split(' ')[0])
        # print(past_list)
        fail_list = []
        for i in past_list:
            try:
                print(f'------开始更新库：{i}……')
                update = subprocess.run(f'../py37/python-3.7.6.amd64/Scripts/pip install --upgrade {i} -i https://pypi.tuna.tsinghua.edu.cn/simple --use-feature=2020-resolver --user',universal_newlines=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                if update.returncode == 0:
                    print(f'{i}:已更新完成!')
                else:
                    print(f'{i}:更新失败：{update.stderr}')
                    fail_list.append(i)
            except Exception:
                #更新不成功就删了
                delete = subprocess.run(f'../py37/python-3.7.6.amd64/Scripts/pip uninstall {i} -y',universal_newlines=True,stdout=subprocess.PIPE)
                print(f'删除{update.returncode}')
                pass
        if len(fail_list) == 0:
            print('所有库已全部更新')
        else:
            print('以下库更新失败，请重新运行程序，或手动更新。\n', fail_list)