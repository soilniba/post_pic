import json
import requests
import urllib.request


feishu_robot_test = '34006ae3-b50a-48a6-9871-eb2a1b43223c'
pic_url_test = "https://wx4.sinaimg.cn/mw690/0045ix6egy1gulw9owk3qj61ww2uoqv602.jpg"
pic_large_url_test = "https://wx4.sinaimg.cn/large/0045ix6egy1gulw9owk3qj61ww2uoqv602.jpg"

def get_token(app_id = "cli_a1c3790e21f8100c",app_secret = "YVXgZL2HnYi6gHm2NmxenfOTi60rfrQ3"):
    """获取应用token，需要用app_id和app_secret，主要是上传图片需要用到token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    Body = {
        "app_id":app_id,
        "app_secret":app_secret
    }
    r = requests.post(url, headers=headers, json=Body)
    return json.loads(r.text)['tenant_access_token']

def upload_image(image_url):
    # 上传图片
    image = urllib.request.urlopen(image_url)#.read()
    # image_url = '20210811_4669089379784439_7.jpg'
    # with open(image_url, 'rb') as f:
    #     image = f.read()

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
        return Exception("Call Api Error, errorCode is %s" % content["code"])

def send_alert(feishu_robot_key):
    feishu_msg = {"content": []}
    feishu_msg["title"] = '图文消息测试'
    feishu_msg["content"].append([
        {
            "tag": "text",
            "text": '文字部分啦'
        },
    ])
    feishu_msg["content"].append([
        {
            "tag": "img",
            "image_key": upload_image(pic_url_test),
            # "width": 300,
            # "height": 300
        },
    ])
    send_feishu_robot(feishu_robot_key, feishu_msg)

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

if __name__ == "__main__":
    send_alert(feishu_robot_test)
