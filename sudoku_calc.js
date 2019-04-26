//递归函数
function calc_sudoku(t_arr,y=0,x=0)
{
    //临界停止判定
    if(y==8 && x==8)
    {
        if(t_arr[y][x]!=0)
        {
            return t_arr;
        }
        else
        {
            var cal = calc_one(t_arr,y,x);
            for(var i in cal)
            {
                if(cal[i]!=null)
                {
                    t_arr[y][x] = cal[i];
                    return t_arr;
                }
            }
            return false;
        }
    }
    //换行时更新xy的值
    if(x==9)
    {
        y++;
        x=0;
    }
    //当前不为0时继续递归
    if(t_arr[y][x]!=0)
    {
        return calc_sudoku(t_arr,y,x+1)
    }else
    {
        //当前为0，遍历所有可能情况
        var cal = calc_one(t_arr,y,x);
        var now_list = new Array();
        for(var i in cal)
        {
            if(cal[i]!=null)
            {
                for(var o=0;o<9;o++)
                    now_list[o] = t_arr[o].slice();
                now_list[y][x] = cal[i];

                var re = calc_sudoku(now_list,y,x+1);
                if(typeof re=='object')
                    return re;
            }
        }
        return false;
    }
}

//列出所有可能性
function calc_one(y_arr,y,x)
{
    tmp = [null,1,2,3,4,5,6,7,8,9];
    for(var i=0;i<9;i++)
    {
        //按行排除
        tmp[y_arr[y][i]] = null;
        //按列排除
        tmp[y_arr[i][x]] = null;
        //按小宫格排除
        tmp[y_arr[parseInt(y/3)*3+parseInt(i/3)][parseInt(x/3)*3+(i%3)]] = null;
    }
    return tmp;
}