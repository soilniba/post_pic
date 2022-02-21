from asyncio.windows_events import NULL
from bs4 import BeautifulSoup
import urllib
import json
import time
import datetime
import requests
import os
import re
Cookie = 'st_key_id=17; 754756835_FRSVideoUploadTip=1; bdshare_firstime=1600245916888; rpln_guide=1; BIDUPSID=84C7449E836FE3937135A47C8CD76546; PSTM=1604319790; delPer=0; BDRCVFR[FhauBQh29_R]=mbxnW11j9Dfmh7GuZR8mvqV; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; video_bubble754756835=1; IS_NEW_USER=a5de5c0a6da4c727b33b4c45; TIEBAUID=b745cc17f93e8f26f3e2762f; __yjs_duid=1_1eb23730503726fe943ad198bd6be1831619589886208; USER_JUMP=-1; BAIDUID=322351133F66AF2B2BD85900A7E0F221:FG=1; BAIDUID_BFESS=322351133F66AF2B2BD85900A7E0F221:FG=1; BDRCVFR[en5Q-dJqX6n]=mbxnW11j9Dfmh7GuZR8mvqV; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1624863529; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1624890882; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[tox4WRQ4-Km]=mk3SLVN4HKm; BDRCVFR[CLK3Lyfkr9D]=mk3SLVN4HKm; wise_device=0; st_sign=c55b0e1b; st_data=501d711533b2f96069758bff106503900ecca60a080dc9597e54069feb78c9f02725c67d10ce133c98afd0d7b4ebb3d2b36fffdbbf22ad5f1d476ba2ab086d71cb0a45b512d3209f255d5cfb81c1e27f3eb34cc0807e7ce24b707a748fb83f85f398ed0d135b7ed653efed5e75fd230eff29f98ec6e765a8ff25faec1a51cb6a; liveTvBubbleClosed=1; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDUSS=I3fkdGeEJoM0pmS2tKc283fkdxN25LbVQzaHBad1RSUVpEMnp-RmZ1eVJ6cFZoSVFBQUFBJCQAAAAAAAAAAAEAAADjrPwsx--z5sTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJFBbmGRQW5hcl; BDUSS_BFESS=I3fkdGeEJoM0pmS2tKc283fkdxN25LbVQzaHBad1RSUVpEMnp-RmZ1eVJ6cFZoSVFBQUFBJCQAAAAAAAAAAAEAAADjrPwsx--z5sTWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJFBbmGRQW5hcl; STOKEN=379cf75631691338d59e45cdb36a9d0f51e64479cea10f766624e850cfd6dfa8; H_WISE_SIDS=110085_127969_164870_174441_179345_184716_185240_185268_186841_186897_187090_187282_187828_188333_188453_189325_189337_189732_189755_190248_190474_190616_190790_191068_191253_191369_191431_191501_191735_191810_192207_192237_192386_192407_192957_193283_193378_193560_193754_194085_194359_194512_194520_194583_195174_195189_195343_195401_195478_195537_195540_195552_195592_195679_196045_196050_196230_196251_196276_196427_196467_196518_196753_196834_196837_196940_197209_197222_197241_197313_197582_197662_197698_197710_197783_197819_197891_198074_198181_198189_198269_198327_198429_198511_198648_198877_198914_198997_199176_199233; BAIDU_WISE_UID=wapp_1640697288337_196; tb_as_data=23386fdb0a8406f34cb29f29bf9cbb17262772a0bb397b486840f6b902fcbb44cb94f9eae4ceb282b6fa6c57c19240bdf26899454bd5e43dff7ea2318c3762152b8691f0d801c64ad6322523de0f3812304696299f7b7ec55ac9a1de6e140165; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaScale=1.3; ariaStatus=false; ZD_ENTRY=google'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {
    'User-Agent': user_agent, 
    'Connection': 'keep-alive',
    'Cookie': Cookie,
}

def getAll(file_name = 'xianyuyouhuashuo_menu.json'):
    json_all = load_json(file_name)
    for n in range(76, 1 - 1, -1):
        thread_list = getList(n)
        if thread_list:
            getPage(thread_list, n, json_all)
            print("----第{}页读取完毕----".format(n))
    write_json(file_name, json_all)

def get_pic_file(url, file_patch):
    file_patch = 'food_images_big/{}'.format(file_patch)
    if not os.path.exists(file_patch):
        dir_path = os.path.split(file_patch)[0]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print('makedirs', file_patch, dir_path)
        # url = urllib.parse.quote(url, safe='/:?=&')
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        try:
            with open(file_patch, "wb") as code:
                code.write(response.read())
                # print('下载图片成功', file_patch)
        except Exception as e:
                print('下载图片失败', file_patch)

def write_json(file_name, json_all):
    str_json = json.dumps(json_all, indent=2, ensure_ascii=False)
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

def get_html(url):
        url = urllib.parse.quote(url, safe='/:?=&')
        request = urllib.request.Request(url, headers = headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print('python 返回 URL:{} 数据成功'.format(url))
        return html

def getList(n=1):  # 获取单页JSON数据
    url = "https://jx3.xoyo.com/press/index.html?page={}".format(n)
    HtmlContent = get_html(url) 
    soup = BeautifulSoup(HtmlContent, "lxml")
    thread_list = soup.select_one('.article_list>ul')
    # print(thread_list)
    return thread_list

def getPage(thread_list, page_num, json_all):
    li_num = 1
    li_list = thread_list.select('a')
    compile = re.compile('\w+-\d+-(\d+)-\d.html', re.I)
    for li in reversed(li_list):
        title = li.attrs['title']
        if title.find('咸鱼有话说') != -1:
            href = li.attrs['href']
            match = compile.search(href)
            href_tid = match.group(1)
            # print(title, href, match, match.group(1))
            if href_tid in json_all:
                data_info = json_all[href_tid]
            else:
                data_info = {}
                data_info['href_tid'] = href_tid
                data_info['title'] = title
                data_info['href'] = href
                data_info['page_num'] = page_num
                data_info['li_num'] = li_num
                json_all[href_tid] = data_info
        # src = urllib.parse.quote(src)
        # src = src.replace('https%3A//', 'https://')
        # src = src.replace('-320x320', '')
        # alt = li.attrs['alt']
        # alt = re.sub('chinasichuanfood.com', '', alt, flags=re.IGNORECASE)
        # alt = alt.replace('|', '').replace('\\', '_').replace('/', '_').replace('  ', ' ').strip().replace(' ', '_')
        # alt = '{}.{}_{}.jpg'.format(page_num, li_num, alt)
        # print(src)
        # print(alt)
        # get_pic_file(src, alt)
        li_num += 1


def main():
    getAll()

if __name__ == "__main__":
    main()
