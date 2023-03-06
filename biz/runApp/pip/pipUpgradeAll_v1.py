import pip
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call

for dist in get_installed_distributions():
	print("-------------Updating for:",dist.project_name)
	call("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade " + dist.project_name+" --use-feature=2020-resolver ", shell=True) #--no-cache-dir