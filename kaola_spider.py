import requests
import json
import re
import os
import codecs
import time
from lxml import etree

s = requests.Session()
s.headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
def getgoodsbyxpath(url):
    html_data = s.get(url).text
    html_tree = etree.HTML(html_data)
    for item_tree in html_tree.xpath('//ul[@id="result"]/li'):
        yield {
            #价格
            'price':item_tree.xpath('div/div/p[@class="price"]/span/text()')[0],
            #tag
            'tag':'|'.join(item_tree.xpath('div/div/p[@class="saelsinfo"]/span/text()')),
            #名称
            'name':item_tree.xpath('div/a')[0].attrib.get('title'),
            #评论数量
            'comment':''.join(item_tree.xpath('div/div/p[@class="goodsinfo clearfix"]/a/text()')),
            #国家
            'country':''.join(item_tree.xpath('div/div/p[@class="goodsinfo clearfix"]/span/text()')),
            #商家
            'sp':''.join(item_tree.xpath('div/div/p[@class="selfflag"]/span/text()')),
            #url
            'url':item_tree.xpath('div/a')[0].attrib.get('href')
        }


#获取分类url
def geturl(a,b,page):
    return "https://www.kaola.com/category/{0}/{1}.html?pageNo={2}".format(a,b,page)

#存储所有数据
def save_csv(data,filename):
    writestr=''
    for i in data:
        writestr += '"' + '","'.join(i) + '"' + "\n"

    f=codecs.open(filename,'a','utf-8')
    f.write(writestr)
    f.close()
    
def formate_data(data, categoryName, categoryName_2, categoryName_3):
    #获取商品品牌
    brand = data['name']
    #过滤无关字符
    if brand.find('|') != -1:
        brand = brand.split('|')
        brand = brand[brand.__len__() - 1]
    if brand.find('｜') != -1:
        brand = brand.split('｜')
        brand = brand[brand.__len__() - 1]
    #去掉【】 分割
    brand = re.sub('【+.*?】+|\[+.*?\]+|\(+.*?\)+|（+.*?）+|“.*?”|"|「+.*?」+|《.*?》', ' ', brand).strip().split(' ')

    #如果分割空格之后只有一个数据，那么信息中没有品牌
    if brand.__len__() > 1:
        brand = brand[0].strip()
        if brand.__len__() > 20:
            brand = ''
    else:
        brand = ''
    
    return (
            #名称
            data['name'].strip(),
            #价格
            data['price'],
            #tag
            data['tag'],
            #国家
            data['country'],
            #商家
            data['sp'],
            #评论数量
            data['comment'],
            brand,			#品牌
            categoryName,	#一级分类
            categoryName_2,	#二级分类
            categoryName_3,	#三级分类
            #url
            "https://www.kaola.com" + data['url'],
    )

url = 'http://www.kaola.com/getFrontCategory.html'
r = requests.get(url)
category = r.json().get('frontCategoryList')
flag = False
#顶级分类
for i in category:
    
    #顶级分类名称
    categoryName = i['categoryName']
    #二级分类
    for o in i['childrenNodeList']:

        #二级分类名称
        categoryName_2 = o['categoryName']
        categoryId_2 = o['categoryId']
        
        #三级分类
        for p in o['childrenNodeList']:

            #三级分类名称
            categoryName_3 = p['categoryName']
            categoryId_3 = p['categoryId']
            print()
            print(categoryName, categoryName_2, categoryName_3)
            
            if flag:
                for l in range(1, 1000):
                    page_data = []
                    for goods_item in getgoodsbyxpath( geturl(categoryId_2, categoryId_3,l) ):
                        page_data.append(formate_data(goods_item, categoryName, categoryName_2, categoryName_3))
                    if page_data == []:
                        break
                    else:
                        print(l,end = ',')
                        save_csv(page_data, './kaola_180111_1129.csv')
                    # time.sleep(3)
            #半路开始判定
            if (categoryName == "服饰鞋包" and categoryName_2 == "女士箱包" and categoryName_3 == "手拿包"):
                flag = True
