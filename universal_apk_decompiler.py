import urllib.request
import zipfile
import shutil
import os.path
from os import path
import subprocess
import stat

TOOLS_PATH = "./tools/"
TMP_PATH = "./tmp/"
APK_OUT_PATH = "./apk_out/"

crf_version = "0.148"
crf_file = "cfr-"+crf_version+".jar"
crf_url = "https://github.com/leibnitz27/cfr/releases/download/"+crf_version+"/"+crf_file

fernflower_version = "384"
fernflower_file = "fernflower-"+fernflower_version+".jar"
fernflower_url = "http://files.minecraftforge.net/maven/net/minecraftforge/fernflower/384/"+fernflower_file

apktool_version = "2.4.1"
apktool_file = "apktool_"+apktool_version+".jar"
apktool_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/"+ apktool_file

jadx_version = "1.1.0"
jadx_file = "jadx-"+jadx_version+".zip"
jadx_file2 = "jadx/bin/jadx"
jadx_url = "https://github.com/skylot/jadx/releases/download/v"+jadx_version+"/"+jadx_file

procyon_version = "0.5.36"
procyon_file = "procyon-decompiler-"+procyon_version+".jar"
procyon_url = "https://bitbucket.org/mstrobel/procyon/downloads/"+procyon_file

baksmali_version = "2.3.4"
baksmali_file = "baksmali-"+baksmali_version+".jar"
baksmali_url = "https://bitbucket.org/JesusFreke/smali/downloads/"+baksmali_file

def download_tool(name, url_tool):
    print('Beginning file download ...', url_tool)
    urllib.request.urlretrieve(url_tool, TOOLS_PATH+name)


def unzip(file, to):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(TOOLS_PATH+to)


def download_all_tools():
    if not path.exists(TOOLS_PATH):
        os.mkdir(TOOLS_PATH)
    # dex tools
    # download crf
    if not path.exists(TOOLS_PATH+crf_file):
        download_tool(crf_file, crf_url)

    if not path.exists(TOOLS_PATH+fernflower_file):
        # download fernflower
        download_tool(fernflower_file, fernflower_url)

    if not path.exists(TOOLS_PATH+procyon_file):
        # download procyon
        download_tool(procyon_file, procyon_url)

    # apk
    # download apktool
    if not path.exists(TOOLS_PATH+apktool_file):
        download_tool(apktool_file, apktool_url)

    # jadx
    if not path.exists(TOOLS_PATH+jadx_file):
        download_tool(jadx_file, jadx_url)
        shutil.rmtree(TOOLS_PATH+"jadx", ignore_errors=True)
        unzip(TOOLS_PATH + jadx_file, "jadx")
        st = os.stat(TOOLS_PATH+jadx_file2)
        os.chmod(TOOLS_PATH+jadx_file2, st.st_mode | stat.S_IEXEC)

    #androguard
    subprocess.call(['pip', 'install', '-U', 'androguard'])

    # baksmali
    # download apktool
    if not path.exists(TOOLS_PATH+baksmali_file):
        download_tool(baksmali_file, baksmali_url)
        st = os.stat(TOOLS_PATH+baksmali_file)
        os.chmod(TOOLS_PATH+baksmali_file, st.st_mode | stat.S_IEXEC)


def dex_to_jar(file_apk):
    if not path.exists(TMP_PATH):
        os.mkdir(TMP_PATH)
    # tools to dex2jar
    subprocess.call(["./lib/enjarify/enjarify.sh",file_apk,'-o',TMP_PATH+"apk.jar"])


def decompile_apk(file_apk):
    # APK TOOL
    #apktool d ls.apk -o ls -f
    apk_path = file_apk
    if not path.exists(APK_OUT_PATH+"apktool"):
        os.mkdir(APK_OUT_PATH+"apktool")
    subprocess.call(['java', '-jar', TOOLS_PATH+apktool_file, '-f', 'd' ,apk_path,'-o',APK_OUT_PATH+"apktool"])

    #jadx
    if not path.exists(APK_OUT_PATH+"jadx"):
        os.mkdir(APK_OUT_PATH+"jadx")
    subprocess.call([TOOLS_PATH+jadx_file2, apk_path,'-d',APK_OUT_PATH+"jadx"])

    #baksmali
    if not path.exists(APK_OUT_PATH+"baksmali"):
        os.mkdir(APK_OUT_PATH+"baksmali")
    subprocess.call(['java', '-jar', TOOLS_PATH+baksmali_file, 'disassemble',apk_path,'-o',APK_OUT_PATH+"baksmali"])

    if not path.exists(APK_OUT_PATH+"androguard"):
        os.mkdir(APK_OUT_PATH+"androguard")
    subprocess.call(['androguard', 'decompile', '-i', apk_path, '-o', APK_OUT_PATH+"androguard"])


def decompile_jar(file_apk):
    dex_to_jar(file_apk)
    # crf
    jar_path = TMP_PATH+"apk.jar"

    if not path.exists(APK_OUT_PATH+"crf"):
        os.mkdir(APK_OUT_PATH+"crf")
    subprocess.call(['java', '-jar', TOOLS_PATH+crf_file, jar_path,'--outputdir',APK_OUT_PATH+"crf"])

    # procyon
    #java -jar procyon.jar -jar myJar.jar -o out
    if not path.exists(APK_OUT_PATH+"procyon"):
        os.mkdir(APK_OUT_PATH+"procyon")
    subprocess.call(['java', '-jar', TOOLS_PATH+procyon_file, '-jar', jar_path,'-o',APK_OUT_PATH+"procyon"])

    #fernflower
    #java -jar fernflower.jar -hes=0 -hdc=0 c:\Temp\binary\ -e=c:\Java\rt.jar c:\Temp\source\
    if not path.exists(APK_OUT_PATH+"fernflower"):
        os.mkdir(APK_OUT_PATH+"fernflower")
    subprocess.call(['java', '-jar', TOOLS_PATH+fernflower_file, jar_path, APK_OUT_PATH+"fernflower"])


def main():
    download_all_tools()
    if not path.exists(APK_OUT_PATH):
        os.mkdir(APK_OUT_PATH)
    decompile_apk("./apk.apk")
    decompile_jar("./apk.apk")


if __name__== "__main__":
    main()