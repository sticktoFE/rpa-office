import re
import subprocess
from pathlib import Path


def nuitka_export():
    # print(__loader__)
    # --windows-disable-console 打的包可以输出日志
    python_path = r"D:\leichui\Miniconda3\envs\rpa\python.exe"
    cmd = (
        f"{python_path} -m nuitka --standalone --mingw64 --show-progress "
        "--include-qt-plugins=sensible,styles --plugin-enable=pyside6 "
        "--follow-import-to=biz.monitor_oa,myutils "
        "--include-package=mytools.general_spider.general_spider,"
        "mytools.general_spider.general_spider.spiders,scrapy,fake_useragent "
        "--nofollow-import-to=tkinter,pil,numpy,scipy,matplotlib,pandas,xlwings,"
        "openpyxl,pyautogui,email,requests,docx,openssl,paddle,paddleocr,schedule,"
        "fitz,pyput,unittest,Ipython,jedi,win32gui,win32con,pygments,pip,mss,asyncio,"
        "blib2to3,lib2to3,idna,cryptography,hyperlink,attr,wrapt,selenium,click,jinja2,"
        "configparser,dateutil "
        "--output-dir=output --windows-icon-from-ico=./rpa.ico --jobs=10 ./biz/monitor_oa/mainw.py"
    )
    # cmd_list = cmd.split()
    print(cmd)
    completedProcess = subprocess.Popen(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        # encoding="utf8",
        # cwd=ip_pool,
    )
    # 程序执行中
    while completedProcess.poll() is None:
        line = completedProcess.stdout.readline().strip()
        # result = re.search(r"PSAS 1:", line)
        if line:
            #   pout = "".join(line)
            #   output = pout.decode("cp936").encode("utf-8")
            # print(f"源系统显示密度：{result.group(1)}")

            print(f"-------------------------Subprogram output: [{line}]")
    # 程序执行完毕，0为正常退出
    if completedProcess.returncode == 0:
        result = re.search(r"(\w+): (\d+)", completedProcess.stdout.readline())
        if result:
            print(f"源系统显示密度：{result.group(2)}")
        print("-------------------------Subprogram success")
        return True
    else:
        print(
            f"-------------------------Subprogram failed:{completedProcess.stderr.readlines()}"
        )
        return False


def copyfile():
    import shutil

    # 拷贝源文件夹中的所有文件和子文件夹到目标文件夹
    src_folder = r".\output\packages"
    dst_folder = r".\output\mainw.dist"
    shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)


def zipfile_7zip():
    # 7zip安装路径
    seven_zip = r"D:\Program Files\7-Zip\7z.exe"
    # 要压缩的文件夹路径
    folder_path = r".\output\mainw.dist"
    # 压缩后的文件名前缀
    output_filename = r".\output\rpa"
    # 删掉旧的压缩文件
    for file_path in Path(".\output").glob("rpa.7z.*"):
        file_path.unlink()
    # 压缩级别（0为无压缩，9为最高压缩率）
    compression_level = 5
    # 分割大小（单位为字节，45MB = 45 * 1024 * 1024字节）
    split_size = 45 * 1024 * 1024
    # 使用7zip进行压缩和分割
    subprocess.run(
        [
            seven_zip,
            "a",
            "-v" + str(split_size),
            "-mx" + str(compression_level),
            output_filename,
            folder_path,
        ]
    )


if __name__ == "__main__":
    if nuitka_export():
        copyfile()
        zipfile_7zip()
