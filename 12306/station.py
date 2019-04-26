import sys
class station:
    def __init__(self):
        with open(sys.path[0] + '\\station_names.dat','r') as file:
            station_names = file.read()
        #print(station_names)
        #station_names = station_names.decode('gbk')
        self.station_list = {}
        for item in [x for x in station_names.split('@') if len(x) != 0 ]:
            tmp = item.split('|')
            self.station_list[tmp[2]] = tmp
        del station_names

    def id2name(self, id):
        return self.station_list[id][1]
    def name2id(self, name):
        for item in self.station_list.values():
            if item[1] == name:
                return item[2]
        return 'BJP'
if __name__ == '__main__':
    #print(sys.path)
    sta = station()
    print(sta.name2id('邢台'))
    print(sta.id2name('BJP'))