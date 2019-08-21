修改backend.py  里面的backend_url 和 backend_token

（backend.py的代码也在这下面，自行复制）

然后将脚本放在某主机，每次用命令即可实现.....：
```
sudo rm -rf backend.py && sudo wget https://xxxx.com/backend.py && sudo python backend.py
```

在 /app/Controllers/Mod_Mu 添加代码：
```
    public function getIP()
    {
        global $ip;
        if (getenv("HTTP_CLIENT_IP"))
            $ip = getenv("HTTP_CLIENT_IP");
        else if(getenv("HTTP_X_FORWARDED_FOR"))
            $ip = getenv("HTTP_X_FORWARDED_FOR");
        else if(getenv("REMOTE_ADDR"))
            $ip = getenv("REMOTE_ADDR");
        else $ip = "Unknow";
        return $ip;
    }

    public function node($request, $response, $args)
    {

        $data_ss = Node::where(["node_ip"=>$this->getIP(),'sort'=>0])->first();
        $data_v2 = Node::where(["node_ip"=>$this->getIP(),'sort'=>11])->first();
        
        if($data_ss or $data_v2){
            $res = [
                "status"   =>  "success",
                "ss_id"   =>  $data_ss["id"] ? $data_ss["id"] : 0 ,
                "v2_id"   =>  $data_v2["id"] ? $data_v2["id"] : 0 ,
                "ip"   =>   $this->getIP()
            ];
        }else{
            $res = [
                "status"   =>  "error",
                "id"   =>  0,
                "ip"   =>  $this->getIP()
            ];
        }
        return $this->echoJson($response, $res);

    }
```
或者直接复制去覆盖整个文件：
```
<?php


namespace App\Controllers\Mod_Mu;

use App\Controllers\BaseController;
use App\Models\NodeInfoLog;
use App\Models\Node;
use App\Services\Config;

class NodeController extends BaseController
{
    public function info($request, $response, $args)
    {
        $node_id = $args['id'];
        if ($node_id == '0') {
            $node = Node::where('node_ip', $_SERVER['REMOTE_ADDR'])->first();
            $node_id = $node->id;
        }
        $load = $request->getParam('load');
        $uptime = $request->getParam('uptime');
        $log = new NodeInfoLog();
        $log->node_id = $node_id;
        $log->load = $load;
        $log->uptime = $uptime;
        $log->log_time = time();
        if (!$log->save()) {
            $res = [
                'ret' => 0,
                'data' => 'update failed',
            ];
            return $this->echoJson($response, $res);
        }
        $res = [
            'ret' => 1,
            'data' => 'ok',
        ];
        return $this->echoJson($response, $res);
    }

    public function get_info($request, $response, $args)
    {
        $node_id = $args['id'];
        if ($node_id == '0') {
            $node = Node::where('node_ip', $_SERVER['REMOTE_ADDR'])->first();
            $node_id = $node->id;
        }
        $node = Node::find($node_id);
        if ($node == null) {
            $res = [
                'ret' => 0
            ];
            return $this->echoJson($response, $res);
        }
        $res = [
            'ret' => 1,
            'data' => [
                'node_group' => $node->node_group,
                'node_class' => $node->node_class,
                'node_speedlimit' => $node->node_speedlimit,
                'traffic_rate' => $node->traffic_rate,
                'mu_only' => $node->mu_only,
                'sort' => $node->sort,
                'server' => $node->server,
                'type' => 'ss-panel-v3-mod_Uim'
            ],
        ];
        return $this->echoJson($response, $res);
    }

    public function get_all_info($request, $response, $args)
    {
        $nodes = Node::where('node_ip', '<>', null)->where(
            static function ($query) {
                $query->where('sort', '=', 0)
                    ->orWhere('sort', '=', 10)
                    ->orWhere('sort', '=', 12);
            }
        )->get();
        $res = [
            'ret' => 1,
            'data' => $nodes
        ];
        return $this->echoJson($response, $res);
    }

    public function getConfig($request, $response, $args)
    {
        $data = $request->getParsedBody();
        switch ($data['type']) {
            case ('database'):
                $db_config = Config::getDbConfig();
                $db_config['host'] = $this->getServerIP();
                $res = [
                    'ret' => 1,
                    'data' => $db_config,
                ];
                break;
            case ('webapi'):
                $webapiConfig = [];
                #todo
        }
        return $this->echoJson($response, $res);
    }

    private function getServerIP()
    {
        if (isset($_SERVER)) {
            if ($_SERVER['SERVER_ADDR']) {
                $serverIP = $_SERVER['SERVER_ADDR'];
            } else {
                $serverIP = $_SERVER['LOCAL_ADDR'];
            }
        } else {
            $serverIP = getenv('SERVER_ADDR');
        }
        return $serverIP;
    }


    public function getIP()
    {
        global $ip;
        if (getenv("HTTP_CLIENT_IP"))
            $ip = getenv("HTTP_CLIENT_IP");
        else if(getenv("HTTP_X_FORWARDED_FOR"))
            $ip = getenv("HTTP_X_FORWARDED_FOR");
        else if(getenv("REMOTE_ADDR"))
            $ip = getenv("REMOTE_ADDR");
        else $ip = "Unknow";
        return $ip;
    }

    public function node($request, $response, $args)
    {

        $data_ss = Node::where(["node_ip"=>$this->getIP(),'sort'=>0])->first();
        $data_v2 = Node::where(["node_ip"=>$this->getIP(),'sort'=>11])->first();
        
        if($data_ss or $data_v2){
            $res = [
                "status"   =>  "success",
                "ss_id"   =>  $data_ss["id"] ? $data_ss["id"] : 0 ,
                "v2_id"   =>  $data_v2["id"] ? $data_v2["id"] : 0 ,
                "ip"   =>   $this->getIP()
            ];
        }else{
            $res = [
                "status"   =>  "error",
                "id"   =>  0,
                "ip"   =>  $this->getIP()
            ];
        }
        return $this->echoJson($response, $res);

    }
}

```

backend.py 的代码：
```
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
```
