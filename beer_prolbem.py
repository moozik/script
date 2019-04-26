'''
https://moozik.cn/archives/256/
'''

class beer_problem:
    def __init__(self):
        self.beer={
            'now':0,
            'count':0,
            'price':2
        }
        self.botcap={
            'now':0,
            'exchange':4
        }
        self.bottle={
            'now':0,
            'exchange':2
        }
        self.money=10
        self.mainloop()
        self.result()
    def mainloop(self):
        if self.money==0\
        and self.botcap['now']<self.botcap['exchange']\
        and self.bottle['now']<self.bottle['exchange']:
            return
        #购买啤酒
        if self.money>=self.beer['price']:
            self.beer['now']=int(self.money/self.beer['price'])
            self.beer['count']=self.beer['now']
            print('购买啤酒',self.beer['now'])
            self.money=0
            self.exchange()

        #兑换啤酒
        if self.botcap['now']>=self.botcap['exchange']:
            tmp=int(self.botcap['now']/self.botcap['exchange'])
            self.beer['now']+=tmp
            self.beer['count']+=tmp
            self.botcap['now']-=tmp*self.botcap['exchange']
            print('使用{0}个瓶盖兑换{1}瓶啤酒，还剩{2}个瓶盖'.format(tmp*self.botcap['exchange'],tmp,self.botcap['now']))
            self.exchange()
        #兑换啤酒
        if self.bottle['now']>=self.bottle['exchange']:
            tmp=int(self.bottle['now']/self.bottle['exchange'])
            self.beer['now']+=tmp
            self.beer['count']+=tmp
            self.bottle['now']-=tmp*self.bottle['exchange']
            print('使用{0}个空瓶兑换{1}瓶啤酒，还剩{2}个空瓶'.format(tmp*self.bottle['exchange'],tmp,self.bottle['now']))
            self.exchange()
        print()
        self.mainloop()
    
    def exchange(self):
        if self.beer['now']!=0:
            self.botcap['now']+=self.beer['now']
            self.bottle['now']+=self.beer['now']
            print('喝掉{0}瓶啤酒，获得{0}个瓶盖{0}个空瓶.'.format(self.beer['now']),'现在共有{0}个瓶盖{1}个空瓶.'.format(self.botcap['now'],self.bottle['now']))
            self.beer['now']=0

    def result(self):
        print('剩余瓶盖{0},剩余空瓶{1},共喝了{2}瓶酒'.format(self.botcap['now'],self.bottle['now'],self.beer['count']))

if __name__=='__main__':
    beer_problem()