# -*- encoding=utf8 -*-
__author__ = "UNITY_105"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

auto_setup(__file__)

init_device("Android")
# install("D:\\Downloads\\Callbreak_11th.apk")
start_app("best.bulbsmash.cash")

def run_poco_test():
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    sleep(5.0)
    poco("Sign in")

    stop_app("best.bulbsmash.cash")
