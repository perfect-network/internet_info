# -*- coding:UTF-8 -*-

backend_url = "https://www.baidu.com/" #机场网址  如：https://www.baidu.com/
backend_token = 'token' #你的 mukey

def run_cmd(cmd):
    try:
        import subprocess
    except ImportError:
        _, result_f, error_f = os.popen3(cmd)
    else:
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_f, error_f = process.stdout, process.stderr

    errors = error_f.read()
    if errors:  pass
    result_str = result_f.read().strip()
    if result_f:   result_f.close()
    if error_f:    error_f.close()

    return result_str

def install():
    base = run_cmd('rpm -qa|grep "docker"')
    if not "docker" in base:
        print("Docker 尚未安装 即将开始安装")
        docker = run_cmd('docker version > /dev/null || curl -fsSL get.docker.com | bash')
        # print(docker)
        print("Docker 安装成功")
        docker = run_cmd('docker restart')
        print("Docker 重启成功")
    base = run_cmd('rpm -qa|grep "libpipeline"')
    if not "libpipeline" in base:
        print("Libpip 尚未安装 即将开始安装")
        docker = run_cmd('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py')
        docker = run_cmd('python get-pip.py')
        print("Libpip 安装成功")

def get_node_id():
    id = requests.get(backend_url  + "/mod_mu/nodes/info?key=" + backend_token)
    id = id.content
    arr = json.loads(id)
    return arr


def start_ssr(id):
    common = "sudo docker run -d --name=ssrmu -e NODE_ID=" + str(id) + " -e API_INTERFACE=modwebapi -e WEBAPI_URL="+ backend_url +" -e WEBAPI_TOKEN="+ backend_token +" --network=host --log-opt max-size=50m --log-opt max-file=3 --restart=always fanvinga/docker-ssrmu"
    docker = run_cmd(common)
    print("Ssrmu  运行成功")
    print("Docker Id:" + docker)

def start_v2ray(id):
    common = 'docker run -d --name=v2ray -e speedtest=0  -e api_port=2333 -e PANELTYPE=0 -e usemysql=0 -e downWithPanel=0 -e node_id=' + str(id) + ' -e sspanel_url='+ backend_url +' -e key='+ backend_token +' --log-opt max-size=10m --log-opt max-file=5 --net=host -p 51201:51201/tcp -p 51201:51201/udp --restart=always --memory="300m"  --memory-swap="1g" rico93/v2ray_v3:go_pay'
    docker = run_cmd(common)
    print("V2ray  运行成功")
    print("Docker Id:" + docker)

def start():
    arr = get_node_id()
    if arr['ret']==0:
        print("IP未获得授权 或 mukey错误")
    elif arr['status']=="success":
        if arr['ss_id']!=0:
            print("当前SS节点ID：" + str(arr['ss_id']))
            start_ssr(arr['ss_id'])
        if arr['v2_id'] != 0:
            print("当前V2节点ID：" + str(arr['v2_id']))
            start_v2ray(arr['v2_id'])
    else:
        print("IP未获得授权 或 mukey错误")

#如果pip未被安装，则安装！！！

def pip():
    base = run_cmd('pip -V')
    if not "site-packages" in base:
        pips = run_cmd("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
        print("下载 pip 成功")
        pips = run_cmd("python get-pip.py")
        print("安装 pip 成功")
        pips = run_cmd("pip install requests")
        print("安装 依赖 成功")
 
def times():
    pips = run_cmd('echo "0 3 * * * root python /root/backend.py" >> /etc/crontab')

def stop():
    docker = run_cmd('docker stop $(docker ps -a -q)')
    print("Ssrmu  停止成功")
    docker = run_cmd('docker  rm $(docker ps -a -q)')
    print("Ssrmu  删除成功")

def docker_restart():
    docker = run_cmd('systemctl stop firewalld.service')
    docker = run_cmd('systemctl disable firewalld.service')
    docker = run_cmd('service docker restart')
    print("Docker 重启成功")

pip()
import sys,os,requests,json
import warnings
warnings.filterwarnings('ignore')
sys1 = sys.argv
if len(sys1)==2 and sys1[1]=="stop":
    docker_restart()
    stop()
else:
    install()
    docker_restart()
    stop()
    start()
    print('运行完毕\n')