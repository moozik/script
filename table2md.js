/*
将网页中的表格转为markdown格式
by:https://github.com/moozik
*/

window.table2md=(function(){
    var table2md=function(innerHTML=false, debug=false){
        var doc_table = document.getElementsByTagName('table');
        if(doc_table.length!==0)
        {
            for(var i=0;i<doc_table.length;i++)
            {
                clog('table ['+i+']','rgb(242, 107, 169)');
                table2md_one(i, innerHTML, debug);
            }
        }else{
            clog('找不到table','brown');
        }

        var text = '%ctable2md by:https://moozik.cn/\n' +
        '%c页面内获取所有表格:table2md([true=>use innerHTML,false=>use innerText], 是否开启debug[true,false])\n\n' + 
        'example:table2md() 文本数据\n' + 
        'example:table2md(1,0) html数据\n' + 
        'example:table2md(0,1) 文本数据,debug';
        console.log('\n'+text+' \n\n','font-size:16px;color:rgb(242, 107, 169);','font-size:15px;color:blue;');
    }

    var clog = function(str,color){
        console.log('\n%c'+str+'\n\n','font-size:15px;color:rgb(250, 250, 242);background:'+color+';padding:3px 0px;border-radius:3px 3px 3px 3px;');
    }
    var table2md_one = function(index=0, innerHTML=false, debug=false){

        var doc_table = document.getElementsByTagName('table');
        // if(doc_table.length===0)return '没有找到表格';
        // if(doc_table.length<=index)return '索引为"'+index+'"的表格不存在';
        //当前表格
        var table = doc_table[index];
        //table=>[thead|tbody]
        var table_type = ['thead','tbody'];
        //生成数组
        var table_arr=[];
        //数据对象
        var tbody,tbody_tr,tbody_tr_td;
        //临时变量
        var data,arr_i;
        //循环变量
        var a,b,c,d;
        //列数
        var column_length=0;

        //遍历可能的组合
        for(a=0; a<table_type.length; a++)
        {
            //[thead|tbody]不存在则跳出
            tbody = table.getElementsByTagName(table_type[a]);
            if(tbody.length === 0)
            {
                continue;
            }
            //遍历每一个[tbody|thead]
            for(b=0; b<tbody.length; b++)
            {
                tbody_tr = tbody[b].getElementsByTagName('tr');
                if(tbody_tr.length === 0)
                {
                    continue;
                }
                //遍历每一个tr
                for(c=0; c<tbody_tr.length; c++)
                {
                    //判定标签为[td|th]
                    tbody_tr_td = tbody_tr[c].getElementsByTagName('td');
                    if(tbody_tr_td.length === 0)
                    {
                        tbody_tr_td = tbody_tr[c].getElementsByTagName('th');
                        if(tbody_tr_td.length === 0)
                        {
                            continue;
                        }
                    }
                    //第一次匹配到非空[td|th]时确定列数
                    if(column_length === 0)
                    {
                        column_length = tbody_tr_td.length;
                    }
                    arr_i = table_arr.length;
                    table_arr[arr_i] =[];
                    //遍历每一个[td|th]
                    for(d=0; d<column_length; d++)
                    {
                        //是否debug
                        if(debug)
                        {
                            console.log(index,table_type[a],b,c,d,tbody_tr_td[d]);
                            console.log("document.getElementsByTagName('table')["+index+"].getElementsByTagName('"+table_type[a]+"')["+b+"].getElementsByTagName('tr')["+c+"].getElementsByTagName('"+tbody_tr_td[d].localName+"')["+d+"]");
                        }
                        //当前数据为空
                        if(typeof tbody_tr_td[d] === 'undefined')
                        {
                            data = '<empty>';
                        //表格嵌套判定
                        }else if(tbody_tr_td[d].getElementsByTagName('table').length !== 0)
                        {
                            data = '<is a table>';
                        }else
                        {
                            //innerHTML or innerText 获取方式
                            if(innerHTML)
                            {
                                data = tbody_tr_td[d].innerHTML;
                            }else
                            {
                                if(typeof tbody_tr_td[d].innerText === 'undefined')
                                {
                                    data = '';
                                }else
                                {
                                    data = tbody_tr_td[d].innerText;
                                }
                            }
                        }
                        table_arr[arr_i][d] = data.replace(/\|/g,'\\\|').replace(/\n/g,'');

                    }//tbody_tr_td end

                }//tbody_tr end

            }//tbody end
            
        }//table_type end

        console.log((function(t_arr){
            var output='| '+t_arr[0].join(' | ')+' |\n';
            var i;
            for(i=0;i<t_arr[0].length;i++)
            {
                output += '| :--- ';
            }
            output += '|\n';
            for(i=1;i<t_arr.length;i++)
            {
                output += '| ' + t_arr[i].join(' | ') + ' |\n';
            }
            return '\n'+output+'\n';
        })(table_arr));
    }
    return table2md;
});
window.table2md();