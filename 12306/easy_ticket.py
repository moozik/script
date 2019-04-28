import requests
import binascii
import os,sys,re,json,time,logging
from station import station
from prettytable import PrettyTable

class Ticket:
    def __init__(self, station):
        #新建catch目录
        if os.path.exists(sys.path[0] + '\\catch') == False:
            os.mkdir(sys.path[0] + '\\catch')
        #搜索条件列表
        self.config = []
        #创建会话对象
        self.s = requests.Session()
        self.sleep_sec = 20
        #超时时间
        self.s.timeout = 20
        #展示表格
        self.tableColumn = {
            'type':'类型',
            'train_id':'车次',
            'search_start':'出发站',
            'search_end':'到达站',
            'time_setout':'出发',
            'time_arrived':'到达',
            'time_travel':'历时',
            'have_ticket':'有票',
            'wuzuo':'无座',
            'yingzuo':'硬座',
            'yingwo':'硬卧',
            'ruanwo':'软卧',
            '2dengzuo':'二等座',
            # '1dengzuo':'一等座',
            # 'shangwu':'商务座'
        }
        #日志
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename=sys.path[0] + '\\ycy.log', level=logging.INFO, format=LOG_FORMAT)
    
    def main(self):
        while True:
            #遍历所有配置项
            for configItem in self.config:
                trainList = []
                trainListOther = []
                halfTichet = {}
                #遍历每一车次
                for trainItem in self.apiTrain(configItem['param']):
                    #判断是否合法
                    if False == self.filterTrain(configItem, trainItem):
                        continue
                    trainItem['type'] = '直达'
                    trainList.append(trainItem)
                print('== 直达车次 {0} {1}->{2} =='.format(
                    configItem['param']['train_date'],
                    station.id2name(configItem['param']['from_station']),
                    station.id2name(configItem['param']['to_station'])))
                self.printTable(trainList)
                print()
                
                #遍历结果集
                # print('查询途径站：')
                for trainItem in trainList:
                    #获取途经站
                    for stationTmp in self.queryByTrainNo(trainItem, configItem):
                        key = '{}_{}_{}'.format(
                            station.name2id(trainItem['search_start']),
                            station.name2id(stationTmp['station_name']),
                            configItem['param']['train_date']
                        )
                        if key not in halfTichet:
                            halfTichet[key] = {}
                        halfTichet[key][trainItem['train_id']] = stationTmp
                    # print(halfTichet)
                    '''
                    #展示车次以及途经车站
                    print(trainItem['train_id']+':',','.join(
                        [
                            x['station_name']
                            for x in [
                                halfTichet[key][trainItem['train_id']]
                                for key in halfTichet
                                if trainItem['train_id'] in halfTichet[key]
                            ]
                        ]
                    ))
                    '''
                #遍历halfTichet，获取半途车票
                # print('apiTrain')
                print('== 补票车次 {0} {1}->{2} =='.format(
                    configItem['param']['train_date'],
                    station.id2name(configItem['param']['from_station']),
                    station.id2name(configItem['param']['to_station'])))
                for key in halfTichet:
                    # print(list(halfTichet[key].values()))
                    # print(list(halfTichet[key].values())[0]['station_name'])
                    param = key.split('_')
                    for trainItem in self.apiTrain({
                            'from_station':param[0],
                            'to_station':param[1],
                            'train_date':param[2],
                            'purpose_codes':'ADULT'
                        }):
                        #过滤车次
                        if trainItem['train_id'] not in halfTichet[key]:
                            continue
                        trainItem['type'] = '补票' if halfTichet[key][trainItem['train_id']]['isEnabled'] else '多买'
                        trainListOther.append(trainItem)
                self.printTable(trainListOther)
                print()
            exit()
            #延时重启
            time.sleep(self.sleep_sec)

    def printTable(self, trainList):
        self.table = PrettyTable(list(self.tableColumn.values()))
        self.table.reversesort = False
        self.table.sortby = '车次'
        self.table.clear_rows()

        for trainItem in trainList:
            trainItem['have_ticket'] = '没票' if trainItem['have_ticket']=='N' else '有'
            trainTmp = []
            for column in self.tableColumn:
                trainTmp.append(trainItem[column])
            self.table.add_row(trainTmp)
        print(self.table)
    
    def addsearch(self, param, pregFilter, timeFilter):
        config = {
            'param':param,
            'filter':pregFilter,
            'time_filter':timeFilter
        }
        logging.info(config)
        self.config.append(config)

    def generateUrl(self, param):
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes={purpose_codes}".format(
            train_date = param['train_date'],
            from_station = param['from_station'],
            to_station = param['to_station'],
            purpose_codes = param['purpose_codes']
        )
        return url

    #请求12306获取数据，返回列表
    def apiTrain(self, param):
        time.sleep(1.5)
        url = self.generateUrl(param)
        logging.info(url)
        response = self.s.get(url)
        ret = []
        if response.status_code != 200:
            exit('网络错误,status_code:' + response.status_code)
        if response.text[:1] != '{':
            exit(url+"\n"+response.text[:20])
        for item in response.json().get('data').get('result'):
            ret.append(self.paramatTrain(item))
        return ret
    '''
    {
    "start_station_name": "北京西",
    "arrive_time": "----",
    "station_train_code": "Z53",
    "station_name": "北京西",
    "train_class_name": "直特",
    "service_type": "1",
    "start_time": "21:16",
    "stopover_time": "----",
    "end_station_name": "昆明",
    "station_no": "01",
    "isEnabled": true
    },
    {
    "arrive_time": "22:29",
    "station_name": "保定",
    "start_time": "22:33",
    "stopover_time": "4分钟",
    "station_no": "02",
    "isEnabled": true
    },
    '''
    #获取途径站
    def queryByTrainNo(self, trainItem, config):
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={train_no}&from_station_telecode={from_station}&to_station_telecode={to_station}&depart_date={train_date}".format(
            train_date = config['param']['train_date'],
            from_station = station.name2id(trainItem['search_start']),
            to_station = station.name2id(trainItem['search_end']),
            train_no = trainItem['train_no']
        )
        logging.info(url)
        #判断是否有缓存
        crc32Code = binascii.crc32(url.encode('utf-8'))
        catchPath = sys.path[0] + '\\catch\\' + str(crc32Code)
        if os.path.exists(catchPath):
            with open(catchPath,'r') as f:
                retData = f.read()
            retData = json.loads(retData)
        else:
            response = self.s.get(url)
            if response.status_code != 200:
                logging.error('status_code:' + response.status_code + "\nurl:" + url)
                exit()

            if response.text[:1] != '{':
                logging.error('page error:' + url)
                exit()
            retData = response.json().get('data').get('data')
            with open(catchPath,'w') as f:
                f.write(json.dumps(retData))
            time.sleep(1.5)
        ret = []
        for key in range(len(retData)):
            item = retData[key]
            #跳过非途经站
            if item['isEnabled'] == False:
                continue
            #跳过始发站
            if item['station_name'] == trainItem['search_start']:
                if key > 0:
                    ret.append(retData[key-1])
                continue
            #跳过终点站
            if item['station_name'] == trainItem['search_end']:
                if key < len(retData) - 1:
                    ret.append(retData[key+1])
                break
            ret.append(item)
        return ret

    def filterTrain(self, config, item):
        #遍历正则过滤
        for colName in config['filter']:
            if config['filter'][colName] != []:
                #任何一项匹配
                flag = False
                for preg in config['filter'][colName]:
                    if re.match(preg, item[colName]):
                        flag = True
                        break
                if not flag:
                    return False

        #发车时间过滤
        if 'time_setout_min' in config['time_filter']:
            if config['time_filter']['time_setout_min'] > item['time_setout']:
                return False
        if 'time_setout_max' in config['time_filter']:
            if config['time_filter']['time_setout_max'] < item['time_setout']:
                return False
        #到达时间过滤
        if 'time_arrived_min' in config['time_filter']:
            if config['time_filter']['time_arrived_min'] > item['time_arrived']:
                return False
        if 'time_arrived_max' in config['time_filter']:
            if config['time_filter']['time_arrived_max'] < item['time_arrived']:
                return False
        #如果可购买，打开浏览器提醒买票
        '''
        if item['have_ticket'] == 'Y':
            note = '{}/{}/{}/{}'.paramat(
                    config['param']['train_date'],
                    item['search_start'],
                    item['search_end'],
                    item['train_id']
                )
            os.system('explorer https://kyfw.12306.cn/otn/leftTicket/init#' + note)
        '''
        return True

    def paramatTrain(self, train):
        info = train.split('|')
        return {
            'xcode1' : info[0],
            'state' : info[1], # 状态 预定
            'train_no' : info[2],# 车次
            'train_id' : info[3], # 车次 T3037
            'train_start' : station.id2name(info[4]), # 列车始发站
            'train_end' : station.id2name(info[5]), # 列车终点站
            'search_start' : station.id2name(info[6]), # 购买起点站
            'search_end' : station.id2name(info[7]), # 购买到达站
            'time_setout' : info[8], # 出发时间
            'time_arrived' : info[9], # 到达时间
            'time_travel' : info[10], # 历经时间
            'have_ticket' : info[11], # 是否可购买 Y
            'xcode3' : info[12], # 
            'train_begin_date' : info[13], # 车次发车日期
            'xcode4' : info[14], # 
            'xcode5' : info[15], # 
            'train_sort_begin' : info[16], # 站序排列起始
            'train_sort_end' : info[17], # 站序排列结束
            'xcode6' : info[18], # 
            'xcode7' : info[19], # 
            'xcode8' : info[20], # 
            'xcode9' : info[21], # 
            'xcode10' : info[22], # 
            'ruanwo' : info[23], # 软卧数量
            'xcode11' : info[24], # 
            'xcode12' : info[25], # 
            'wuzuo' : info[26], # 无座数量
            'xcode13' : info[27], # 
            'yingwo' : info[28], # 硬卧数量
            'yingzuo' : info[29], # 硬座数量
            '2dengzuo' : info[30], # 二等座
            '1dengzuo' : info[31], # 一等座
            'shangwu' : info[32], # 商务座
            'xcode14' : info[33], # 
            'xcode15' : info[34], # 
            'xcode16' : info[35], # 
            'exchange' : info[36] # 可兑换 [1,0]
        }

if __name__ == '__main__':
    station = station()
    ticket = Ticket(station)

    ticket.addsearch({
        'train_date':'2019-04-30',              #乘车日期
        'from_station':station.name2id('北京'), #起始站
        'to_station':station.name2id('邢台'),   #到达站
        'purpose_codes':'ADULT'                 #成人票
    },{
        #正则匹配，有至少一项匹配就展示
        # 'train_id':['Z53','K819'],
        #'time_setout':[],
        #'time_arrived':[],
        #'have_ticket':['Y','N'],
        #'wuzuo':[],
        #'yingzuo':[],
        #'2dengzuo':[],
    },{
        #发车时间和到达时间的区间
        'time_setout_min':'19:00',
        'time_setout_max':'23:59',
        # 'time_arrived_min':'00:00',
        # 'time_arrived_max':'23:59'
    })

    #回北京车票

    ticket.addsearch({
        'train_date':'2019-05-04',              #乘车日期
        'from_station':station.name2id('邢台'), #起始站
        'to_station':station.name2id('北京'),   #到达站
        'purpose_codes':'ADULT'                 #成人票
    },{
        # 'search_start':[],
        # 'state':[],
        #'train_id':[],
        #'time_setout':[],
        #'time_arrived':[],
        #'have_ticket':['Y','N'],
        #'wuzuo':[],
        #'yingzuo':[],
        #'2dengzuo':[],
    },{
        'time_setout_min':'12:00',
        # 'time_setout_max':'19:19',
        'time_arrived_max':'21:00',
        # 'time_arrived_max':''
    })

    ticket.main()