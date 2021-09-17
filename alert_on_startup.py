import json
import requests
import socket

feishu_robot_private = '1d3780d7-07b2-4e03-9d55-1fd0e73478c2'

def send_alert(wx_robot_key=False, feishu_robot_key=False):
    markdown_msg = ''
    feishu_msg = {"content": []}
    feishu_msg["title"] = '🚨{}'.format(socket.gethostname())
    feishu_msg["content"].append([
        {
            "tag": "text",
            "text": '🖥🔌电脑重启啦！！'
        },
    ])
    feishu_msg["content"].append([
        {
            "tag": "at",
            "user_id": "all",
		},
        # 
        
    ])

    if wx_robot_key != False:
        send_wx_robot(wx_robot_key, markdown_msg)
    if feishu_robot_key != False:
        send_feishu_robot(feishu_robot_key, feishu_msg)

def send_wx_robot(robot_url, markdown_msg):
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps({
        "msgtype": "markdown", 
        "markdown": { "content": markdown_msg },
    })
    response = requests.post('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + robot_url, headers=headers, data=data)

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


if __name__ == "__main__":
    send_alert(False, feishu_robot_private)