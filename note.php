<?php
date_default_timezone_set("Asia/Shanghai");

class noteApp{
    const __FILEHEAD__ = '4jrov9vido';
    const __PASS__ = ['1234'];
    
    private $appName = 'moozikNote';
    private $html_title = '单页笔记';
    private $html_head = '';
    private $html_body = '';
    public $noteArr = [];
    private $group = [];
    
    
    public function __construct(){
        $this->config();
        if($this->checkpasswd()){
            $this->noteData();
            $this->route();
        }else{
            $this->pageLogin();
        }
        $this->showPage();
    }
    function checkpasswd(){
        //登陆页面
        if(isset($_COOKIE['passwd']) && in_array($_COOKIE['passwd'],self::__PASS__)){
            return true;
        }else{
            return false;
        }
    }
    
    function config(){
        $head = "<link rel='shortcut icon' href='./note.ico'/>
        <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
        <style>
        .center_box{
            margin:auto;
            width:100%;
            height:100%;
            max-width:990px;
            max-height: 600px;
        }
        
        .main_title{
            padding: 5px;
            margin: 5px;
            color: #ffffff;;
            border: 1px solid;
            background-color: #5f5f5f;
            border-bottom: 0px;
            text-decoration: none;
            -webkit-border-radius: 7px;
            -moz-border-radius: 7px;
            border-radius: 7px;
        }
        .main_content{
            border: solid 1px;
            color: #000;
            margin: 5px;
            padding: 5px;
            background-color: #e6e6e6;
            -webkit-border-radius: 7px;
            -moz-border-radius: 7px;
            border-radius: 7px;
            /*height: 103px;*/
            overflow: hidden;
        }
        .main_content a{
            color: #00BCD4;
            text-decoration: none;
        }
        .main_content a:hover{
            color:coral;
        }
        
        .update_title{
            width: 80%;
            font-size:large;
            margin:2px;
        }
        .update_content{
            width: 100%;
            height: 465px;
            font-size:large;
        }
        .update_box{
            width: 100%;
            max-width: 700px;
        }
        
        .login_box input {
            /*height: 24%;*/
            /*width: 33%;*/
            min-height: 70px;
            min-width: 100px;
            font-size: -webkit-xxx-large;
            margin-top: 3px;
        }
        </style>
        <script>
        function uncompress(id, height, ele){
            document.getElementById('content_' + id).style='height:' +(height * 21)+ 'px';
            ele.style='display:none;';
        }
        function chkgroup(value){
            var group = document.getElementsByClassName('group_' + value);
            var group_all = document.getElementsByClassName('group_all');
            
            for(var i=0;i<group_all.length;i++){
                group_all[i].style = 'display:none;';
            }
            for(i=0;i<group.length;i++){
                group[i].style = '';
            }
        }
        </script>";

        /*<style>input{width: 20%;height: 20%;font-size: xx-large;margin:2px;}</style>*/
        $this->html('head',$head);
    }
    
    function showPage(){
        $this->html('head','<title>' . $this->html_title . ' - ' . $this->appName . '</title>');
        echo '<html>';
        echo '<head>' . $this->html('head') . '</head>';
        echo '<body><div class="center_box">' . $this->html('body') . '</div></body>';
        echo '</html>';
    }
    
    function route(){
        //接收修改POST
        if(!empty($_POST)){
            $this->actionUpdate();
            return;
        }
        //修改页面
        if(!empty($_GET['a']) && $_GET['a']=='update'){
            $this->pageUpdate();
            return;
        }
        //删除
        if(!empty($_GET['a']) && $_GET['a']=='delete' && !empty($_GET['id'])){
            $this->actionDelete();
            return;
        }
        //主页
        if(empty($_GET) && empty($_POST)){
            $this->pageList();
        }
    }
    
    function noteData($isRead = true){
        //读
        if($isRead){
            if(empty($this->noteArr)){
                if(!file_exists($this->filepath())){
                    return [];
                }else{
                    $this->noteArr = json_decode(file_get_contents($this->filepath()),1);
                }
                foreach($this->noteArr as &$item){
                    $item['content'] = base64_decode($item['content']);
                    if($item['group'] != '' && !in_array($item['group'],$this->group)){
                        $this->group[] = $item['group'];
                    }
                }
                arsort($this->noteArr);
            }
            return $this->noteArr;
        }else{
        //写
            foreach($this->noteArr as &$item){
                $item['content'] = base64_encode($item['content']);
                if(empty($item['group'])){
                    $item['group'] = '';
                }
            }
            file_put_contents($this->filepath(), json_encode($this->noteArr));
        }
    }
    
    function select(){
        return '<option value="all">全部</option><option value="default">未分类</option><option>' . implode('</option><option>', $this->group) . '</option>';
    }
    function filepath($passwd = ''){
        $passwd = $_COOKIE['passwd'];
        return self::__FILEHEAD__ . '_' . $passwd . '.json';
    }
    
    //主页展示
    function pageList(){
        $echo = '<div>
        <a href="?a=update" class="main_title">新笔记</a>
        <select onchange="chkgroup(this.value)" class="main_title">'.$this->select().'</select>
        <a href="javascript:document.cookie= \'passwd=9999;\';location.reload();" class="main_title">logout</a>
        </div>
        <hr>';
        foreach($this->noteData() as $noteItem){
            //替换地址
            $arr_search = array();
            $arr_replace = array();
            preg_match_all('/((ht|f)tps?):\/\/([\w\-]+(\.[\w\-]+)*\/)*[\w\-]+(\.[\w\-]+)*\/?(\?([\w\-\.,@?^=%&:\/~\+#]*)+)?(\r\n|$)/',$noteItem['content'],$res);
            foreach($res[0] as $uri){
                $uri = trim($uri);
                if(in_array($uri,$arr_search)){
                    continue;
                }
                $arr_search[] = $uri . "\r\n";
                $arr_replace[] = "<a href='$uri' target='_blank'>$uri</a>\r\n";
                // $noteItem['content'] = str_replace($uri, "<a href='$uri' target='_blank'>$uri</a>", $noteItem['content'], 1);
            }
            
            $noteItem['content'] = trim(str_replace($arr_search, $arr_replace, $noteItem['content'] . "\r\n"));
            
            //替换换行
            $noteItem['content'] = str_replace("\r\n", "<br>", $noteItem['content']);
            
            //高度调整
            $count = substr_count($noteItem['content'], "<br>") + 1;
            if($count > 10){
                $now_style = 'height:125px';
            }else{
                $now_style = null;
            }
            
            //contenteditable
            $echo .= "<div class='group_all group_" . ($noteItem['group']!=''?$noteItem['group']:'default') . "'><a href='?a=update&id={$noteItem['id']}' class='main_title'>{$noteItem['title']}</a>
            <span class='main_title'>{$noteItem['time']}</span><br>
            <div class='main_content' id='content_{$noteItem['id']}' style='".($now_style??'')."' >{$noteItem['content']}</div>";
            $echo .= $now_style ? "<a href='javascript:void(0);' onclick='uncompress({$noteItem['id']},{$count},this)' class='main_title'>▼</a><hr>" : '<hr>';
            $echo .= "</div>";
        }
        $this->html('body', $echo);
    }
    
    function actionDelete(){
        //接收删除GET
        unset($this->noteArr[$_GET['id']]);
        $this->noteData(false);
        header("location:" . $_SERVER['PHP_SELF']);
    }
    function pageLogin(){
        $html = "<div class='login_box'><input type='button' value='1' onclick='fun(this.value)'/>
        <input type='button' value='2' onclick='fun(this.value)'/>
        <input type='button' value='3' onclick='fun(this.value)'/><br>
        <input type='button' value='4' onclick='fun(this.value)'/>
        <input type='button' value='5' onclick='fun(this.value)'/>
        <input type='button' value='6' onclick='fun(this.value)'/><br>
        <input type='button' value='7' onclick='fun(this.value)'/>
        <input type='button' value='8' onclick='fun(this.value)'/>
        <input type='button' value='9' onclick='fun(this.value)'/><br>
        <input type='button' value='0' onclick='fun(this.value)'/>
        <input type='hidden' value='' id='pass'/>
        </div>
        <script>
        function fun(i){
            document.getElementById('pass').value += i;
            if(document.getElementById('pass').value.length == " . strlen(self::__PASS__[0]) . "){
                document.cookie = 'passwd='+document.getElementById('pass').value+';';
                location.reload();
            }
        }
        </script>
        ";
        $this->html('body', $html);
    }
    function pageUpdate(){
        $note_data = &$this->noteData();
        if(!empty($_GET['id']) && !empty($note_data[$_GET['id']])){
            $id = $_GET['id'];
            $title = $note_data[$id]['title'];
            $content = $note_data[$id]['content'];
            $time = $note_data[$id]['time'];
            $group = $note_data[$id]['group'];
        }else{
            $id='';
            $title = '';
            $content = '';
            $time = '';
            $group = '';
        }
        $html = "
        <form action='{$_SERVER['PHP_SELF']}' method='post'>
            <div class='update_box'>
                <input type='text' value='$title' name='title' placeholder='标题' class='update_title' />
                <input type='text' value='$group' name='group' placeholder='默认分类' class='update_title' />
                <input type='hidden' value='$id' name='id'/>
                <hr>
                <textarea name='content' placeholder='内容' class='update_content'>$content</textarea>
                <hr>
                <input type='submit' value='提交' /><br>
                {$time}<br>
                <a href=\"javascript:if(confirm('确实要删除吗?'))location='?a=delete&id=$id'\">删除</a>
            </div>
        </form>";
        $this->html('body',$html);
    }
    //接收修改POST
    function actionUpdate(){
        //print_r($_POST);
        if(empty($_POST['id'])){
            if(empty($this->noteArr)){
                $id = 1;
            }else{
                $max = 0;
                foreach($this->noteArr as $i){
                    if($i['id'] > $max){
                        $max = $i['id'];
                    }
                }
                $id = $max + 1;
            }
        }else{
            $id = $_POST['id'];
        }
        $this->noteArr[$id] = [
                'time' => date('Y-m-d H:i:s'),
                'id' => $id,
                'title' => $_POST['title'],
                'content' => $_POST['content'],
                'group' => $_POST['group'],
            ];
        $this->noteData(false);
        header("location:" . $_SERVER['PHP_SELF']);
    }
    
    function html($pos, $htmlData = null){
        if(empty($htmlData)){
            return $this->html_{$pos};
        }
        $this->html_{$pos} .= $htmlData;
    }
}

$app = new noteApp();
exit;
