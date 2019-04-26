'''
https://moozik.cn/archives/104/

使用任意一种麻将的表示方法，使用python判断是否胡牌

河北麻将
万(1-9)
条(10-18)
筒(19-27)
东    西    南    北    中    发    白
28    29    30    31    32    33    34
34*4=136

14张牌
胡牌
[28,28,28,29,29,29,30,30,30,31,31,31,32,32]

把杠考虑为三张一样的
不考虑十三幺七小对

递归：
进入函数的数组，判断长度
如果长度为2：
    判断两张是否相同：
        相同-》胡牌
        不相同-》不胡牌
如果长度不为2：
    使用首张牌组成一组牌，递归除去这组牌剩余的其他所有牌型牌，返回返回值
'''
#判断胡牌
def calc_(list_):
    #剩下三张牌
    if list_.__len__()==3:
        #三张牌相同
        if list_.count(list_[0])==3:
            print_(list_,'刻，真')
            return True
        #是顺子
        elif list_[0]+list_[2]==list_[1]*2 and list_[0]<=25:
            print_(list_,'顺，真')
            return True
        #不相同，不顺子，返回假
        else:
            print_(list_,'非刻顺，假')
            return False
    #剩下两张牌
    elif list_.__len__()==2:
        #两张牌相同即为将，返回真，否则返回假
        if list_.count(list_[0])==2:
            print_(list_,'将，真')
            return True
        else:
            print_(list_,'非将，假')
            return False
    #剩下的牌数大于3
    else:
        #这里只需要考虑到所有情况就可以了，不需要else判断
        if list_.count(list_[0])==3:
            #首张牌相同有三张,去掉前三章剩下的作为列表递归，判断返回值
            print_(list_,'刻')
            if calc_(list_[3:]):
                return True
        if list_.__len__()%3==2 and list_.count(list_[0])==2:
            #判断是否已有将，若没有那么尝试前两张做将
            print_(list_,'将')
            if calc_(list_[2:]):
                return True
        if list_.count(list_[0]+1)>=1 and list_.count(list_[0]+2)>=1 and list_[0]<=25:
            #那么判断是否可组成顺子
            print_(list_,'顺')
            if calc_(list_[3:]):
                return True
        #不是三张相同的，不是将，不是顺，那么首张牌不能组成任何牌，返回假
        print_(list_,'last')
        return False
def print_(list__,str__):
    print('剩余'+str(list__.__len__())+':'+str__)
    print(list__)
if __name__=='__main__':
    hu=[28,28,28,29,29,29,30,30,30,31,31,31,32,32]
    hu=[1,1,1,2,3,4,5,6,7,8,9,9,9,8]
    # hu=[1,1,2,3,4,5,6,7,7,8,9,30,30,30]
    # hu=[1,1,1,2,3,3,4,5,5,6,7,7,8,9]
    hu.sort()
    # for i in range(1,100):
        # calc_(hu)
    if calc_(hu):
        print('恭喜胡牌')
    else:
        print('还没胡牌')