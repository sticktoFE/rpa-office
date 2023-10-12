# -*- encoding=utf8 -*-
__author__ = "loube"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/XPL0220327004608?cap_method=MINICAP&touch_method=MAXTOUCH&",])


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)