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
