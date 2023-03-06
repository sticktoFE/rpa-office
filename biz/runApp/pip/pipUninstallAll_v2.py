import subprocess
import re

toDelPackage = 'keras'
ret = subprocess.run('../py37/python-3.7.6.amd64/Scripts/pip freeze',universal_newlines=True,stdout=subprocess.PIPE)
if ret.returncode != 0:
    print('获取包列表失败，请重新运行！')
    exit(0)
else:
	#print(ret.stdout)
	past_list = ret.stdout.split('\n')
	#print(past_list[9])
	fail_list = []
	for i in past_list:
		try:
			if  re.match(toDelPackage,i,flags=re.I):
				print(f'------开始清理库：{i}……')
				delete = subprocess.run(f'../py37/python-3.7.6.amd64/Scripts/pip uninstall -y {i}',universal_newlines=True,stdout=subprocess.PIPE)
				if delete.returncode == 0:
						print(f'{i}:删除完成!')
				else:
					print(f'{i}:删除失败：{delete.stdout}')
					fail_list.append(i)
		except Exception:
			pass
	if len(fail_list) == 0:
		print('库已清理完成')
	else:
		print('以下库清理失败，请重新运行程序，或手动清理。\n', fail_list)

	