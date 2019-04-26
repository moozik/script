
'''
不回头迷宫路线计算
'''
class maze:

    
    def __init__(self, maze_arr):
        self.direction = {
            2:'↓',
            4:'←',
            8:'↑',
            6:'→',
            7:'⊙',
            9:'囍',
            0:'∷',
            1:'■',
        }
        
        self.start_pos = 0, 0
        self.step_count = 0
        self.calc_count = 0
        self.str2int(maze_arr)
        #print('id self.maze_arr',id(self.maze_arr))
        ret = self.main_loop(self.maze_arr[:], self.start_pos, 1)
        print('递归数量：',self.calc_count)
        print(ret)
        if ret[0]:
            #ret[1][self.start_pos[0]][self.start_pos[1]] = 7
            self.show(ret[1])

    def main_loop(self, arr, pos, step_num):
        self.calc_count += 1
        fun_arr = arr[:]

        #递归点
        if self.step_count == step_num:
            fun_arr[pos[0]][pos[1]] = 9
            return (True, fun_arr)
        
        #判断是否有解
        ret = self.step_map(fun_arr, pos)
        if len(ret) == 0:
            return (False,)

        #遍历方向
        for item in ret:
            #print(' '*step_num*4, '='*10)
            fun_arr = arr[:]
            #赋值当前点的方向
            fun_arr[pos[0]][pos[1]] = item[1]
            ret2 = self.main_loop(fun_arr, item[0], step_num + 1)
            if ret2[0]:
                return ret2
        fun_arr[pos[0]][pos[1]] = 1
        return (False,fun_arr)
    
    def step_map(self, arr, pos):
        ret = []
        #8 上
        if pos[0] != 0 and arr[pos[0]-1][pos[1]] == 1:
            ret.append(((pos[0]-1,pos[1]),8))
        #6 右
        if len(arr[0]) > pos[1]+1 and arr[pos[0]][pos[1]+1] == 1:
            ret.append(((pos[0],pos[1]+1),6))
        #2 下
        if len(arr) > pos[0]+1 and arr[pos[0]+1][pos[1]] == 1:
            ret.append(((pos[0]+1,pos[1]),2))
        #4 左
        if pos[1] != 0 and arr[pos[0]][pos[1]-1] == 1:
            ret.append(((pos[0],pos[1]-1),4))
        return ret

    def show(self, arr):
        result = ''
        for i_arr in arr:
            for pos in i_arr:
                result += self.direction[pos]
            result += '\n'
        print(result,'\n')
    
    def str2int(self, maze):
        count_start = 0
        self.count_1 = 0
        maze = [x.ljust(len(maze[0]),'1')[:len(maze[0])] for x in maze]
        self.maze_arr = [[int(y) for y in x] for x in maze]
        maze_show = ''
        for i in range(0,len(self.maze_arr)):
            for o in range(0,len(self.maze_arr[0])):
                if self.maze_arr[i][o] == 1:
                    self.step_count += 1
                    maze_show += self.direction[1] #可以走的路
                
                if self.maze_arr[i][o] == 0:
                    maze_show += self.direction[0] #墙
                
                if self.maze_arr[i][o] == 7:
                    self.step_count += 1
                    self.start_pos = i, o
                    maze_show += self.direction[7] #起点
                
            maze_show += "\n"
        print(maze_show)

'''
'''
if __name__ == '__main__':
    print('最强连一连计算器')
    print('使用说明：0代表墙壁，1代表可以走的路，7代表起始点')
    print('')
    while True:
        print('-*'*30)
        input_arr = []
        i=0
        while True:
            i+=1
            text_in = input('第{}行:'.format(i))
            if text_in == '':
                break
            input_arr.append(text_in)
        if len(input_arr) == 0:
            maze(['111','011','011','711',])
        else:
            maze(input_arr)