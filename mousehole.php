<?php
/*
放到可访问google的php环境中，就可以简单使用google了
图标出不来，看着怪怪的，能用就好
*/

class MouseHole{
    private $default_host = 'https://www.google.com';
    private $param_name = 'url';
    private $param_special = 'special_site';
    private $param_static = 'static_res';
    private $white_list = array(
            'url',
            'special_site',
        );
    private $special_site = array(
        );
    
    function __construct(){
        $this->HTTP_ACCEPT_LANGUAGE = $_SERVER['HTTP_ACCEPT_LANGUAGE'];
        $this->HTTP_USER_AGENT = $_SERVER['HTTP_USER_AGENT'];
        
        $this->get = $_GET;
        $this->post = $_POST;
        
        $this->self_name = $_SERVER['PHP_SELF'];
    }
    
    /*
	显示错误
    */
    function showError($errorMessage, $data = []){
    	echo 'errorMessage:' . $errorMessage . "<br />errorData:";
    	print_r($data);
    	exit;
    }

    /*
    验证host正确性
    */
    function checkRequest(){
        /*
        - check:get post 中至少有一个有host
        - 获得url
        */
        
        $url = '';
        if(!empty($this->get[$this->param_name])){
            $url = $this->get[$this->param_name];
        }else if(!empty($this->post[$this->param_name])){
            $url = $this->post[$this->param_name];
        }else{
        	//$this->showError('没找到'.$this->param_name.'参数.',array_merge($this->get, $this->post));
        	
            //展示常用网站
            $showList = array(
                'https://www.google.com',
                );
            foreach($showList as $item){
                echo sprintf("<a href='?%s=%s'>%s</a><br><br>",
                    $this->param_name, $item, $item);
            }
            
            echo sprintf("<form action='%s'><input name='%s' type='search' value='%s' /> <input type='submit' value='打开'></form>",
                $this->self_name, $this->param_name, $this->default_host);
            
            echo "<a href='?self_code=1'>查看源代码</a><br><br>";
            
            exit;
        }
        $url = urldecode($url);
        
        //检查url
        if(preg_match("/^(https?:\/\/)?[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+(:\d+)?(\/.*)?$/", $url)){
            if(!preg_match("/^https?:\/\//", $url)){
                $url = 'https://' . $url;
            }
        }else{
            $this->showError('url不合法', array($url));
        }
        
        $paramStr = '';
        //拼接额外get参数
        foreach($this->get as $k => $v){
            if(in_array($k,$this->white_list)){
                continue;
            }
            $paramStr .= '&' . $k . '=' . urlencode($v);
        }
        if(strpos($url, '?') > 0){
            $url .= $paramStr;
        }else{
            $url .= '?' . substr($paramStr,1);
        }
        
        preg_match_all("/^https?:\/\/[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+(:\d+)?/", $url, $res);
        $this->requestSite = $res[0][0];

        if(in_array($this->requestSite,$this->special_site)){
            $this->IS_site_special = true;
        }else{
            $this->IS_site_special = false;
        }
        return $url;
    }
    
    function staticUrl(&$html){
        $arr_find = array();
        $arr_replace = array();
        
        preg_match_all('/<script.*?src="([^"]+)".*?><\/script>/', $html, $scriptList);
        preg_match_all('/<link.*?href="([^"]+)".*?>/', $html, $scriptList2);

        foreach(array_merge($scriptList[1], $scriptList2[1]) as $k => $scriptUrl){
            //跳过完整链接
            if(preg_match("/^(https?|\/\/)/", $scriptUrl)){
                continue;
            }
            if($this->IS_site_special){
                //替换
                $arr_find[] = $scriptUrl;
                $arr_replace[] = $this->self_name . '?' . $this->param_static . '=' . $this->requestSite . $scriptUrl;
                
            }else{
                //替换
                $arr_find[] = $scriptUrl;
                $arr_replace[] = $this->requestSite . $scriptUrl;
            }
        }
        $html = str_replace($arr_find, $arr_replace, $html);
    }
    
    function genHtml(){
        //检查链接
        $this->requestUrl = $this->checkRequest();
        //请求html
        $html = $this->holeGet($this->requestUrl, $this->post);
        //修复script link标签地址
        $this->staticUrl($html);
        
        //拼接footjs用于修复页面中的links form表单
        return $html . $this->footJs();
    }
    
    function catchRes(){
        
    }
    function execute(){
        if(!empty($this->get[$this->param_special])){
            // return $this->catchRes();
        }else if(!empty($this->get[$this->param_static])){
            return $this->holeGet($this->get[$this->param_static]);
        }else if(!empty($this->get['self_code'])){
            show_source(__FILE__);
        }else{
            return $this->genHtml();
        }
    }
    
    function holeGet($url, $post_data=array())
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        $header = array(
            'Accept-Language: ' . $this->HTTP_ACCEPT_LANGUAGE,
            'User-agent: ' . $this->HTTP_USER_AGENT,
            
        ); //设置一个你的浏览器agent的header
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_USERAGENT, $this->HTTP_USER_AGENT);
        //跟随302跳转
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        if(!empty($post_data)){
            //设置post方式提交
            curl_setopt($curl, CURLOPT_POST, 1);
            curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
        }
        $res = curl_exec($ch);
        // $rescode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        return $res;
    }
    
    function footJs(){
        return
<<<EOF
        <script>
        //https://www.baidu.com:80
        var Req_Site = "$this->requestSite";
        var Main_Site = window.location.protocol + '//' + window.location.host;
        var Main_Url = window.location.href.match(/[^?]*/)[0];
        Main_Url = Main_Site + '$this->self_name';
        var i,o;
        var Req_Url,Str_Param;
        var Reg_Path = /^(https?:)?\/\/[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)+(\/.*)/;
        var Reg_Param = /(\?|&)([^&\?=]+=[^&\?=]+)/g;
        var Reg_Filename = /\/[^\?]*/;
        //将a链接中省略域名的链接修复
        for(i = 0; i < document.links.length; i++){
            //排除空链接
            if(document.links[i].href.match(/^javascript:/i)){
                continue;
            }
            //排除非当前站的链接（针对google还有导航站）
            if(document.links[i].href.search(Req_Site) == -1 && document.links[i].href.search(Main_Site) == -1){
                continue;
            }
            //获取路径部分
        	Req_Path = document.links[i].href.match(Reg_Path)[3];
            console.log('i='+i,Req_Path);
            
            //拆分路径中的路径和参数
            Req_Filename = Req_Path.match(Reg_Filename)[0];
            Req_Param = Req_Path.match(Reg_Param);
            Str_Param = '';
            if(Req_Param != null){
                for(o=0;o<Req_Param.length;o++){
                    if(Req_Param[o].substr(1,3)=='url')continue;
                    Str_Param += '&' + Req_Param[o].substr(1);
                }
            }
            console.log(Req_Path, Str_Param);
            
        	//链接路径部分和域名部分
        	Req_Url = encodeURIComponent(Req_Site + Req_Filename);
        	console.log('Req_Url:' + Req_Url);
        	//拼接上本页面链接
            document.links[i].href = Main_Url +'?url=' + Req_Url + '&' + Str_Param.substr(1);
        }

        for(i = 0; i < document.forms.length; i++){
            //排除跳转到其他站的表单
            if(document.forms[i].action.search(Req_Site) == -1 && document.forms[i].action.search(Main_Site) == -1){
                consinue;
            }
        	Req_Path = document.forms[i].action.match(Reg_Path)[3];
        	Req_Url = encodeURIComponent(Req_Site + Req_Path);
            document.forms[i].action = Main_Url +'?url=' + Req_Url;
            document.forms[i].innerHTML += '<input type="hidden" name="url" value="' + Req_Url + '" />';
        }
        //console.log('url:','$this->requestUrl');
        
        </script>
EOF;
    }
}
//echo json_encode($_SERVER);exit;
$obj = new MouseHole();
echo $obj->execute();


exit;