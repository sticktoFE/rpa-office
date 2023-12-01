import os
import time
from adb import ADBCMD


def zhangyu99(android):
    """
    这个函数就是傻瓜式的一步一步模拟人对手机进行操作
    """

    def shua15s(x, y, i):
        print("正在点击", x, y, "第", i, "次")
        time.sleep(0.5)
        android.click(x, y)
        time.sleep(2)
        android.swipe_up()
        time.sleep(6)
        android.swipe_up()
        time.sleep(5)
        android.swipe_down()
        time.sleep(5)
        android.back()

    [shua15s(0x387, 0x4BC, i) for i in range(1)]
    [shua15s(0x379, 0x578, i) for i in range(8)]
    [shua15s(0x376, 0x63E, i) for i in range(3)]
    [shua15s(0x362, 0x6E6, i) for i in range(5)]
    [shua15s(0x375, 0x79B, i) for i in range(25)]


def xiaban():
    adb = ADBCMD()
    adb.click_home()
    adb.stop_app("com.zyb.yuanxin")
    adb.start_app("com.zyb.yuanxin/com.zyb.ZYBLoadingActivity")
    time.sleep(5)
    adb.click(1489, 1672)
    time.sleep(1)
    adb.click(1099, 723)
    time.sleep(1)
    adb.click(1468, 900)
    adb.stop_app("com.zyb.yuanxin")
    adb.click_power()


if __name__ == "__main__":
    # android = ADBCMD()  # 获得一个ADB命令实例
    # android.click_home()
    # # zhangyu99(android)#执行对聚划算99养章鱼活动的脚本
    # android.start_app("com.zyb.yuanxin/com.zyb.ZYBLoadingActivity")
    # time.sleep(5)
    # android.swipe_up()
    # subprocess.run("adb shell getevent",shell=True)
    # subprocess.run("adb shell screencap -p | sed 's/\r$//' > screen.png",shell=True)

    # apps, error = adb.shell_command("pm list packages")
    # for app in apps:
    #     path, error = adb.shell_command("pm path {}".format(app.split(":")[1]))
    #     print(("{}: {}".format(app, path)))
    # xiaban()
    import subprocess

    # 有锁且息屏
    def is_screen_off() -> bool:
        output = subprocess.check_output(
            ["adb", "shell", "dumpsys", "window", "policy"]
        )
        output = output.decode("utf-8")
        # 检查输出中是否包含 "mHoldingWakeLockSuspendBlocker=false" 表示息屏
        # 和 "mUserActivitySummary=INACTIVE" 表示锁屏
        return (
            "KeyguardServiceDelegate" in output
            and "showing=true" in output
            and "screenState=SCREEN_STATE_OFF" in output
        )

    # 唤醒手机屏幕
    def wake_screen():
        subprocess.call(["adb", "shell", "input", "keyevent", "224"])

    # 解锁屏幕
    def unlock_screen():
        subprocess.call(["adb", "shell", "input", "keyevent", "82"])

    if is_screen_off():
        wake_screen()
        unlock_screen()
    # print(is_screen_on())
    import adbutils

    def is_screen_lock(id):
        # ----------------------
        # 检测屏幕是否被锁，不同于屏幕点亮, 判断亮屏请使用 adbutils.is_screen_on
        # ----------------------
        try:
            command = "adb -s " + id + " shell dumpsys window policy"
            result = os.popen(command)
            lines = result.readlines()
            loc_flag = 0
            for i in range(len(lines)):
                if "KeyguardServiceDelegate".strip() in lines[i]:
                    loc_flag = i + 1
            if "showing=true" in lines[loc_flag] and loc_flag != 0:
                return True
            else:
                return False
        except Exception as e:
            print("获取手机lock状态异常", e)
            return False

    print(is_screen_lock("R52TC00LB3K"))
    # print(is_screen_off())
