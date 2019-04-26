import requests
import re
import math
import json
import codecs
from lxml import etree
'''
{'cat1': '美体健康',
'cat2': '缓解疲劳',
'name': '\r\nKAO花王蒸汽眼膜眼罩去黑眼圈/舒缓疲劳 蒸汽贴\r\n',
'brand': 'KAO花王',
'price_53': '1567',
'price_54': '1688',
'price_55': '1729',
'price_56': '2078',
'price_57': '900',
'url': 'https://www.hommi.jp/cn/product/3223',
'comment': '319'
}
'''
class Hommi:
    def __init__(self):
        self.init()
        self.main()

    def init(self):
        self.site = 'https://www.hommi.jp'
        self.s = requests.Session()
        self.cookies = {
            'c-lang' : 'cn',
            'provinceId' : '13',
            'currency' : 'CNY',
            'shopId' : '53',
            'localName' : 'China',
            'c-position' : 'oversea'
        }
        self.s.cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        self.s.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
    def get_int(self, text_):
        return int(''.join(re.findall('\d',text_)))

    def get_etree(self, url):
        return etree.HTML(self.s.get(url).text)

    def goods_generator(self):
        category_tree = self.get_etree(self.site + '/cn/category')

        xpath_1 = '//*[@id="pjax-container"]/div[2]/div/div[2]/div/ul/li/ul/li[1]'
        xpath_2 = '//*[@class="p-pic"]/a/@href'
        #遍历顶级分类
        for li_item in category_tree.xpath(xpath_1):
            category_url = li_item.xpath('a')[0].attrib.get('href')
            category_text = li_item.xpath('a')[0].text
            category_count = self.get_int(category_text)
            print(category_text)
            print(category_count)
            page_count = math.ceil(category_count/20)
            print('page_count:' + str(page_count))
            #遍历分类所有页
            for page in range(page_count):
                category_url_2 = '{0}{1}{2}{3}'.format(self.site, category_url, '?page=', page + 1)
                category_tree_2 = self.get_etree(category_url_2)
                print('now:' + str(page))
                #遍历所有商品
                for page_url in category_tree_2.xpath(xpath_2):
                    #解析详情页
                    page_tree = self.get_etree(self.site + page_url)
                    detail_data = page_tree.xpath('//*[@id="detail-data"]')[0].text
                    detail_json = json.loads(detail_data)
                    
                    if 'specInfo' in detail_json:
                        #有规格
                        return_data = []
                        for x in range(0, len(detail_json['specInfo']), 2):
                            item_tree = self.get_etree(self.site + '/cn/product/' + detail_json['specInfo'][x])
                            yield self.page_parse_goods(item_tree, detail_json['specInfo'][x + 1])
                    else:
                        #无规格
                        yield self.page_parse_goods(page_tree, '')
                # break
            # break

    def page_parse_goods(self, page_tree, spec_info):
        return_dict = {}
        tmp = page_tree.xpath('//ul[@class="breadcrumb"]/li')
        return_dict['cat1'] = tmp[2].xpath('a')[0].text.strip()
        return_dict['cat2'] = tmp[3].xpath('a')[0].text.strip()
        return_dict['name'] = tmp[4].text.strip().replace('"', "'")
        return_dict['brand'] = page_tree.xpath('//*[@id="pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[2]/a')[0].text
        detail_json = json.loads(page_tree.xpath('//*[@id="detail-data"]')[0].text)

        for i in ['53','54','55','56','57']:
            if i in detail_json['prices']:
                return_dict['price_' + i] = detail_json['prices'][i]
            else:
                return_dict['price_' + i] = '0'
                
        return_dict['url'] = self.site + '/cn/product/' + str(detail_json['productId'])

        return_dict['comment'] = page_tree.xpath('//*[@id="pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/span/b')[0].text
        return_dict['spec_info'] = spec_info
        return return_dict

    #存储所有数据
    def save_csv(self, data_):
        list_ = [data_['cat1'],
        data_['cat2'],
        data_['name'],
        data_['spec_info'],
        data_['brand'],
        data_['price_53'],
        data_['price_54'],
        data_['price_55'],
        data_['price_56'],
        data_['price_57'],
        data_['url'],
        data_['comment']]

        f=codecs.open('hommi.csv', 'a', 'utf-8')
        f.write('"' + '","'.join(list_) + '"\n')
        f.close()

    def main(self):
        for item in self.goods_generator():
            self.save_csv(item)

if __name__ == '__main__':
    Hommi()