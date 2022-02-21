import os
import json
import time
import random
import csv
import requests
import urllib.request
from time import sleep

wx_robot_babala = 'f76655fa-c62c-40a6-9675-a922d874b038'
feishu_robot_test = '34006ae3-b50a-48a6-9871-eb2a1b43223c'
feishu_robot_babala = 'd992f480-4203-4a37-a00c-e9a1532869c9'
feishu_robot_xiaozhushou = 'bba8c0f3-8f75-4eb8-869b-4fdb8112eef6'
feishu_app_id = "cli_a1c3790e21f8100c"
feishu_app_secret = "YVXgZL2HnYi6gHm2NmxenfOTi60rfrQ3"

def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e: # 不是半角字符就返回原来的字符
        return uchar 
    if inside_code == 0x0020: # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)

def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([B2Q(uchar) for uchar in str(ustring)])

tHourEmojiList = { 1: '🕐', 2: '🕑', 3: '🕒', 4: '🕓', 5: '🕔', 6: '🕕', 7: '🕖', 8: '🕗', 9: '🕘', 10: '🕙', 11: '🕚', 12: '🕛', }
def GetHourEmoji(hh):
    hh = int(hh)
    if hh > 12:
        hh = hh - 12
    return tHourEmojiList[hh]


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

ad_key_list = {
    '三星',
    '华为',
    '测评',
    '潮流玩具',
    '潮玩娱乐',
    '公司宗旨',
    '品牌',
    'vivo',
    '小米',
    '全网预定',
    '敬请期待',
    '上新',
    '售价',
    '预定',
    '商品',
    '贩售',
    '低价',
    '免单',
    # 'Q版',
    '盲盒',
    '玩具',
    '安利模玩手办',
}

ban_user_id_list = {
    3355469752,
}

def has_ad_key(text):
    for ad in ad_key_list:
        if ad in text:
            return True
    return False

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
            if '源用户id' in row and row['源用户id'] != None:
                data_info['源用户id'] = row['源用户id']
            if '源微博bid' in row and row['源微博bid'] != None:
                data_info['源微博bid'] = row['源微博bid']
            if '正文' in row:
                data_info['正文'] = row['正文']
                # if not has_ad_key(row['正文']) and len(row['原始图片url'].split(',')) > 1 and len(data_info['正文']) > 250 and len(data_info['正文']) < 3000:
                #     print('', len(data_info['正文']), data_info['正文'])
                #     weibo_url = 'https://weibo.com/{}/{}'.format('1876856920', bid)
                #     print(weibo_url)
            if '源微博正文' in row and row['源微博正文'] != None:
                data_info['源微博正文'] = row['源微博正文']
                # if not has_ad_key(row['源微博正文']) and len(row['源微博原始图片url'].split(',')) > 1 and len(data_info['源微博正文']) > 250 and len(data_info['源微博正文']) < 3000:
                #     print('', len(data_info['源微博正文']), data_info['源微博正文'])
                #     weibo_url = 'https://weibo.com/{}/{}'.format(row['源用户id'], row['源微博bid'])
                #     print(weibo_url)
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
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_url
    # response = requests.post(url, headers=headers, data=data)

def get_token(app_id = feishu_app_id, app_secret = feishu_app_secret):
    """获取应用token，需要用app_id和app_secret，主要是上传图片需要用到token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    Body = {
        "app_id":app_id,
        "app_secret":app_secret
    }
    r = requests.post(url, headers=headers, json=Body)
    return json.loads(r.text)['tenant_access_token']

def upload_feishu_image(image_url, err_num = 0):
    # 上传图片
    image = urllib.request.urlopen(image_url)#.read()
    resp = requests.post(
        url='https://open.feishu.cn/open-apis/image/v4/put/',
        headers={
            'Authorization': "Bearer " + get_token(),
        },
        files={
            "image": image
        },
        data={
            "image_type": "message"
        },
        stream=True)
    resp.raise_for_status()
    content = resp.json()
    if content.get("code") == 0:
        return content['data']['image_key']
    else:
        print(Exception("Call Api Error, errorCode is %s" % content["code"]))
        err_num += 1
        if err_num <= 10:
            sleep(1)
            return upload_feishu_image(image_url, err_num)
        else:
            return False

def send_feishu_robot(feishu_robot_key, feishu_msg):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": feishu_msg
            }
        }
    })
    response = requests.post('https://open.feishu.cn/open-apis/bot/v2/hook/' + feishu_robot_key, headers=headers, data=data)
    print('飞书消息已发送')

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
    if '源用户id' in data_info and data_info['源用户id'] != None:
        user_id = data_info['源用户id']
    if has_ad_key(weibo_text):
        return post_csv(json_name, user_id, robot_url)
    if user_id in ban_user_id_list:
        return post_csv(json_name, user_id, robot_url)
    if len(weibo_text) > 250:
        return post_csv(json_name, user_id, robot_url)
    if len(pic_table) <= 1:
        return post_csv(json_name, user_id, robot_url)
    # if 'post_time' in data_info and (data_info['post_time'] - time.time()) < 4 * 7 * 24 * 60 * 60:  # 上次发布时间小于一个月
    #     return post_csv(json_name, user_id, robot_url)
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
    cut_text = weibo_text[0:25]
    content_text = "已经{}点了，{}号鼓励师想对您说：\n[{}...]({})".format(hh, user_id, cut_text, weibo_url)
    feishu_msg = {"content": []}
    feishu_msg["title"] = "{}{}点了，来杯特仑苏吧：".format(GetHourEmoji(hh), hh, user_id)
    feishu_msg_links = []
    feishu_upload_image_url = random_pic_url
    if feishu_upload_image_url.find('large') != -1:
        # 上传图片替换成缩略图地址
        feishu_upload_image_url = feishu_upload_image_url.replace('/large/', '/mw690/')
    feishu_image_key = upload_feishu_image(random_pic_url)
    feishu_msg["content"].append([
        {
            "tag": "img",
            "image_key": feishu_image_key,
        }
    ])
    feishu_msg["content"].append(feishu_msg_links)
    feishu_msg_links.append(
        {
            "tag": "a",
            "text": cut_text,
            "href": weibo_url,
        },
    )

    pic_index = 1
    for pic_url in pic_table:
        pic_text = pic_index
        if pic_url == random_pic_url:
            content_text += ' \[**{}**\]'.format(pic_text)
            pic_text = stringQ2B(pic_text)
        else:
            content_text += ' \[[{}]({})\]'.format(pic_text, pic_url)
        feishu_msg_links.append({
            "tag": "a",
            "text": ' [{}]'.format(pic_text),
            "href": pic_url,
        })
        pic_index += 1
    data = json.dumps({
        "msgtype": "markdown", 
        "markdown": {
            "content": content_text
        }
    })
    send_wx_robot(robot_url, data)

    # 发送到飞书机器人
    if feishu_image_key != False:
        send_feishu_robot(feishu_robot_xiaozhushou, feishu_msg)
    global post_index
    post_index += 1

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
    # get_csv_file('CSV北电中戏的美女们', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\北电中戏的美女们\\3283836867.csv')
    # get_csv_file('CSVKookong_', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\Kookong_\\2480712160.csv')
    # get_csv_file('CSV藏弓U', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\藏弓U\\5652393418.csv')
    # get_csv_file('CSV几度星霜_Jeral', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\几度星霜_Jeral\\2250601564.csv')
    # get_csv_file('CSV摄影写真博主', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\摄影写真博主\\5900744122.csv')
    get_csv_file('CSV蛋壳-安利协会', 'C:\\Users\\wangr\\weibo-crawler_retweet\\weibo\\蛋壳-安利协会\\1876856920.csv')
    # get_csv_file('CSV鸡腿子瘦了但她膨胀了', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\鸡腿子瘦了但她膨胀了\\2126877340.csv')
    # get_csv_file('CSV山海观雾', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\山海观雾\\5115987302.csv')
    # get_csv_file('CSV鞠婧祎', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\鞠婧祎\\3669102477.csv')
    # get_csv_file('CSV小甜甜甜T', 'C:\\Users\\wangr\\weibo-crawler\\weibo\\小甜甜甜T\\5161703950.csv')


    # post_csv('CSV鸡腿子瘦了但她膨胀了', '2126877340', wx_robot_babala)
    # post_csv('CSV借图', '5102556735', wx_robot_babala)
    # post_csv('CSV街拍疯狂', '6336987096', wx_robot_babala)
    # post_csv('CSV小甜甜甜T', '5161703950', wx_robot_babala)
    # post_csv('CSV鞠婧祎', '5161703950', wx_robot_babala)
    # post_csv('CSV山海观雾', '5115987302', wx_robot_babala)

    
    # post_csv('CSVKookong_', '2480712160', wx_robot_babala)
    # post_csv('CSV藏弓U', '5652393418', wx_robot_babala)
    # post_csv('CSV几度星霜_Jeral', '2250601564', wx_robot_babala)
    # post_csv('CSV北电中戏的美女们', '3283836867', wx_robot_babala)
    # post_csv('CSV摄影写真博主', '5900744122', wx_robot_babala)
    # post_csv('CSV蛋壳-安利协会', '1876856920', wx_robot_babala)
    # post_csv('CSV蛋壳-安利协会', '1876856920', wx_robot_babala)
    post_csv('CSV蛋壳-安利协会', '1876856920', wx_robot_babala)
    post_csv('CSV蛋壳-安利协会', '1876856920', wx_robot_babala)
    post_csv('CSV蛋壳-安利协会', '1876856920', wx_robot_babala)

if __name__ == "__main__":
    main()
