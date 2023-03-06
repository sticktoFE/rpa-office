from subprocess import getstatusoutput
g = getstatusoutput('pip list --outdated -i https://pypi.tuna.tsinghua.edu.cn/simple')    # 更改为阿里云的源 https://mirrors.aliyun.com/pypi/simple/
if g[0] != 0:
    print('获取更新列表失败，请重新运行！')
    exit(0)
else:
    if len(g[1]) == 0:
        print('所有的库都是最新的，无需更新。')
        exit(0)
    else:
        print('过期的库有：\n', g[1])
        past_list = []
        g_list = g[1].split('\n')
        #print(g_list)
        for i in g_list[2:]:
            past_list.append(i.split(' ')[0])
        # print(past_list)

        fail_list = []
        for i in past_list:
            try:
                print(f'------开始更新库：{i}……')
                update = getstatusoutput(f'pip install --upgrade {i} -i https://pypi.tuna.tsinghua.edu.cn/simple --use-feature=2020-resolver --user')
                if update[0] == 0:
                    print(f'{i}:已更新完成!')
                else:
                    print(f'{i}:更新失败：{update[1]}')
                    fail_list.append(i)
                    #更新不成功就删了
                    delete = getstatusoutput(f'pip uninstall {i} -y')
                    print(f'删除{delete[0]}')
            except Exception:
                pass
        if len(fail_list) == 0:
            print('所有库已全部更新')
        else:
            print('以下库更新失败，请重新运行程序，或手动更新。\n', fail_list)