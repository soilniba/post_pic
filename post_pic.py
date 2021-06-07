import os
import json
import time
import random
import csv
import requests

robot_babala = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f76655fa-c62c-40a6-9675-a922d874b038'

# def walk_pic_dir(dir_path):
#     listdir = os.walk(dir_path)
#     for root, dirs, files in listdir:
#         print(root)
#         for file in files:
#             if root == dir_path:
#                 print(root + file)
#             else:
#                 print(root + os.sep + file)
#         for dirName in dirs:
#             print(root + dirName)

def list_pic_dir(json_name, dir_path):
    file_name = '{}.json'.format(json_name)
    json_table = load_json(file_name)

    listdir = os.listdir(dir_path)
    for name in listdir: 
        # print(dir_path + os.sep + name)
        pic_path = dir_path + os.sep + name
        if pic_path in json_table:
            data_info = json_table[pic_path]
            if not 'pic_path' in data_info:
                data_info['pic_path'] = pic_path
        else:
            data_info = {}
            data_info['pic_path'] = pic_path
            json_table[pic_path] = data_info
    print('[{}]目录列表获取完毕'.format(json_name))
    write_json(file_name, json_table)
    return json_table

def write_json(file_name, json_table):
    str_json = json.dumps(json_table, indent=2, ensure_ascii=False)
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(str_json)
        f.close()

def load_json(file_name):
    try:
        f = open(file_name, "r", encoding='utf-8')
    except IOError:
        return {}
    else:
        return json.load(f)

def post_pic(json_table):
    pic_path = random.choice(list(json_table))
    data_info = json_table[pic_path]
    print(pic_path, data_info['pic_path'])

def get_csv_file(json_name, file_path):
    with open(file_path, encoding='utf-8')as f:
        f_csv = csv.DictReader(f)
        file_name = '{}.json'.format(json_name)
        json_table = load_json(file_name)
        for row in f_csv:
            # print(row['\ufeffid'], row['bid'], row['正文'], row['原始图片url'])
            bid = row['bid']
            if bid in json_table:
                data_info = json_table[bid]
            else:
                data_info = {}
                json_table[bid] = data_info
            data_info['bid'] = bid
            if '源微博bid' in row and row['源微博bid'] != None:
                data_info['源微博bid'] = row['源微博bid']
            if '正文' in row:
                data_info['正文'] = row['正文']
            if '源微博正文' in row and row['源微博正文'] != None:
                data_info['源微博正文'] = row['源微博正文']
            if '原始图片url' in row:
                data_info['原始图片url'] = row['原始图片url'].split(',')
            if '源微博原始图片url' in row and row['源微博原始图片url'] != None:
                data_info['源微博原始图片url'] = row['源微博原始图片url'].split(',')
        print('[{}]CSV获取完毕'.format(json_name))
        write_json(file_name, json_table)
        return json_table

def send_wx_robot(robot_url, data):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(robot_url, headers=headers, data=data)

post_index = 1
def post_csv(json_name, user_id, robot_url):
    file_name = '{}.json'.format(json_name)
    json_table = load_json(file_name)
    random_bid = random.choice(list(json_table))
    data_info = json_table[random_bid]
    pic_table = data_info['原始图片url']
    weibo_text = data_info['正文']
    if '源微博原始图片url' in data_info and data_info['源微博原始图片url'] != None:
        pic_table = data_info['源微博原始图片url']
    if '源微博正文' in data_info and data_info['源微博正文'] != None:
        weibo_text = data_info['源微博正文']
    if '源微博bid' in data_info and data_info['源微博bid'] != None:
        random_bid = data_info['源微博bid']
    if len(pic_table) > 2:
        random_pic_url = random.choice(list(pic_table))
        weibo_url = 'https://weibo.com/{}/{}'.format(user_id, random_bid)
        data_info['post_time'] = time.time()
        file_name = '{}.json'.format(json_name)
        write_json(file_name, json_table)
        print(random_bid, weibo_text, random_pic_url, weibo_url)
        # 图文
        data = json.dumps({
            "msgtype": "news", 
            "news": {
                "articles": [
                    {
                        "title" : weibo_text,
                        "description" : '点击查看大图',
                        "url" : random_pic_url,
                        "picurl" : random_pic_url
                    }
                ]
            },
        })
        send_wx_robot(robot_url, data)
        # 微博链接
        hh = time.strftime("%H", time.localtime(time.time()))
        data = json.dumps({
            "msgtype": "markdown", 
            "markdown": {
                "content": "已经{}点了，{}号鼓励师想对您说：[{}]({})".format(hh, user_id, weibo_text, weibo_url)
            }
        })
        send_wx_robot(robot_url, data)
        global post_index
        post_index += 1
    else:
        post_csv(json_name, user_id, robot_url)

def post_test(json_name, user_id, robot_url):
    file_name = '{}.json'.format(json_name)
    json_table = load_json(file_name)
    random_bid = 'K9bUrEGn2'
    data_info = json_table[random_bid]
    pic_table = data_info['原始图片url']
    random_pic_url = random.choice(list(pic_table))
    weibo_url = 'https://weibo.com/{}/{}'.format(user_id, random_bid)
    data_info['post_time'] = time.time()
    file_name = '{}.json'.format(json_name)
    write_json(file_name, json_table)
    # print(random_bid, data_info['正文'], random_pic_url, weibo_url)
    print(random_pic_url, len(pic_table))


        
def main():
    # json_table = list_pic_dir('File北电中戏的美女们', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\北电中戏的美女们\\img\\原创微博图片')
    # post_pic(json_table)


    # get_csv_file('CSV街拍疯狂', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\街拍疯狂\\6336987096.csv')
    # get_csv_file('CSV借图', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\借图\\5102556735.csv')
    get_csv_file('CSV北电中戏的美女们', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\北电中戏的美女们\\3283836867.csv')
    get_csv_file('CSVKookong_', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\Kookong_\\2480712160.csv')
    get_csv_file('CSV藏弓U', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\藏弓U\\5652393418.csv')
    get_csv_file('CSV几度星霜_Jeral', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\几度星霜_Jeral\\2250601564.csv')
    get_csv_file('CSV摄影写真博主', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\摄影写真博主\\5900744122.csv')
    # get_csv_file('CSV鸡腿子瘦了但她膨胀了', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\鸡腿子瘦了但她膨胀了\\2126877340.csv')
    # get_csv_file('CSV山海观雾', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\山海观雾\\5115987302.csv')
    # get_csv_file('CSV鞠婧祎', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\鞠婧祎\\3669102477.csv')
    # get_csv_file('CSV小甜甜甜T', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\小甜甜甜T\\5161703950.csv')


    # post_csv('CSV鸡腿子瘦了但她膨胀了', '2126877340', robot_babala)
    # post_csv('CSV借图', '5102556735', robot_babala)
    # post_csv('CSV街拍疯狂', '6336987096', robot_babala)
    # post_csv('CSV小甜甜甜T', '5161703950', robot_babala)
    # post_csv('CSV鞠婧祎', '5161703950', robot_babala)
    # post_csv('CSV山海观雾', '5115987302', robot_babala)

    
    post_csv('CSVKookong_', '2480712160', robot_babala)
    post_csv('CSV藏弓U', '5652393418', robot_babala)
    post_csv('CSV几度星霜_Jeral', '2250601564', robot_babala)
    post_csv('CSV摄影写真博主', '5900744122', robot_babala)
    post_csv('CSV北电中戏的美女们', '3283836867', robot_babala)

if __name__ == "__main__":
    main()
