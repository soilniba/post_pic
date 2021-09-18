import json
import requests
import socket
from subprocess import run, PIPE
from time import sleep

feishu_robot_private = '1d3780d7-07b2-4e03-9d55-1fd0e73478c2'

def send_alert(feishu_robot_key):
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
    # 先检查能否联网
    for i in range(1, 5 * 60 + 1):
        # 尝试5分钟
        domain = 'open.feishu.cn'
        r = run('ping {}'.format(domain),
                stdout=PIPE,
                stderr=PIPE,
                stdin=PIPE,
                shell=True)
        if r.returncode:
            print('第{}次尝试，{}连接失败'.format(i, domain))
        else:
            print('{}连接正常'.format(domain))
            send_alert(feishu_robot_private)
            break
        sleep(1)
