import itertools

'''
http://www.qlcoder.com/task/7566
https://moozik.cn/archives/425/
'''

class laowang:
    def __init__(self):
        #老王可以选择货物的重量
        self.goods = [509,838,924,650,604,793,564,651,697,649,747,787,701,605,644]
        #老王的车可以放置的最大重量
        self.max_weight = 5000
        
        #动态规划
        self.fun2()
        #排列组合
        self.fun1()

        
    def fun1(self):
        print('排列组合')
        self.count = 0
        result2 = 0
        #排列组合寻找选择结果
        for i in range(len(self.goods)):
            for x in itertools.combinations(self.goods,i):
                self.count += 1
                if sum(x) > result2 and sum(x)<=self.max_weight:
                    result2 = sum(x)
                    result_list = x
        print(result2,result_list,self.count)
    def fun2(self):
        print('动态规划')
        self.count = 0
        #计算可以带走的最大的重量
        result = self.getmax(self.max_weight, len(self.goods) - 1)
        print(result,'getmax() count:',self.count)
        self.count = 0
        # 排列组合寻找选择结果
        for i in range(len(self.goods)):
            for x in itertools.combinations(self.goods,i):
                self.count += 1
                if sum(x) == result:
                    print(x,'-'.join([str(self.goods.index(o)+1) for o in x]),'for count:',self.count)
                    
    def getmax(self, last_weight, item):
        self.count += 1
        #如果当前只剩下一个（边界）
        if item == 0:
            #剩余重量大于当前货物重量，返回当前货物重量
            if last_weight >= self.goods[item]:
                return self.goods[item]
            else:
                return 0
        #方案a：如果剩余重量大于当前货物重量，那么带走，不大于，那么planA为0
        if last_weight > self.goods[item]:
            plan_a = self.getmax(last_weight - self.goods[item], item - 1) + self.goods[item]
        else:
            #由于无法带走当前货物，所以与planB等价，防止重复搜索，planA=0
            plan_a = 0
            
        #方案b：放弃当前货物，直接到下一个货物
        plan_b = self.getmax(last_weight, item - 1)
 
        #挑选重量更高的方案，返回
        if plan_a > plan_b:
            return plan_a
        else:
            return plan_b
 
if __name__ == '__main__':
    laowang()