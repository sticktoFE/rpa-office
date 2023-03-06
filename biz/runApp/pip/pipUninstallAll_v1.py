import re
from pip._internal.utils.misc import get_installed_distributions
from subprocess import call

for dist in get_installed_distributions():
	if  re.match('keras',dist.project_name,flags=re.I):
		print("-------------uninstall for:",dist.project_name)
		call("pip uninstall  -y " + dist.project_name) #--no-cache-dir