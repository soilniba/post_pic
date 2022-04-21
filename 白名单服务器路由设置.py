import os, re
import ctypes, sys
import requests


remote_gateway = ''

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_sys_route(query_ip):
    sys_route_table = os.popen('route print ' + query_ip)  # 使用os.popen()获取程序输出
    all_route_lines = sys_route_table.readlines()  # 按行读取
    start_inx, end_inx = [inx for inx, line in enumerate(all_route_lines) if line == '\n']  # 使用\n分割出路由表的起始行和结束行
    ipv4_route_lines = all_route_lines[start_inx + 5:end_inx - 1]  # 所有ipv4路由字符串列表
    ipv4_route_split_inx = ipv4_route_lines.index('永久路由:\n')  # 以固定字符串分割ipv4的永久路由和活动路由
    ipv4_fix_route_lines = ipv4_route_lines[ipv4_route_split_inx + 2:]  # 永久路由字符串列表(已减去无用行)
    ipv4_act_route_lines = ipv4_route_lines[:ipv4_route_split_inx - 1]  # 活动路由字符串列表(已减去无用行)
    for line in ipv4_act_route_lines:
        route, mask, gateway, interface, metric = re.findall(r'\S+', line)  # 网络路由地址,掩码,网关,跃点数
        # print(route, mask, gateway, interface, metric)
        # print(gateway)
        return gateway
    return False

def SetRemoteGateIP(ip):
    os.system('route DELETE ' + ip)
    os.system('route ADD {} MASK 255.255.255.255 {}'.format(ip, remote_gateway))

# @REM 未验证地址
# @REM route DELETE 103.255.203.234
# @REM route ADD 103.255.203.234 MASK 255.255.255.255 %REMOTE_GATE%
# @REM route DELETE 180.167.212.114
# @REM route ADD 180.167.212.114 MASK 255.255.255.255 %REMOTE_GATE%
# @REM route DELETE 180.167.212.121
# @REM route ADD 180.167.212.121 MASK 255.255.255.255 %REMOTE_GATE%


HOST_PATH = 'c:\windows\system32\drivers\etc\HOSTS'
hosts_text = ''
def write_file(filepath, text):
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(text)
        f.close()

def read_file(filepath):
    f = open(filepath, "r", encoding='utf-8')
    return f.read()

def UpdateLine(ip, hostname):
    global hosts_text
    if hosts_text.find(hostname) > -1:
        hosts_text = re.sub('\n[^\n]*{}[^\n]*\n'.format(hostname), '\n{} {}\n'.format(ip, hostname), hosts_text)
    else:
        hosts_text = '{}\n{} {}'.format(hosts_text, ip, hostname)

# 192.168.21.2 dc2
# 192.168.21.12 dc4
# 192.168.21.156 code.aurogon.com
# 106.3.147.232 cms.gamebar.com
# 180.167.212.113 gjol-external-admin-xz.wangyuan.net
def UpdateHosts():
    global hosts_text
    hosts_text = read_file(HOST_PATH)
    hosts_text_old = hosts_text
    UpdateLine('192.168.21.156', 'code.aurogon.com')
    # UpdateLine('192.168.21.2', 'dc2')
    # UpdateLine('192.168.21.12', 'dc4')
    # UpdateLine('106.3.147.232', 'cms.gamebar.com')
    # UpdateLine('180.167.212.113', 'gjol-external-admin-xz.wangyuan.net')
    if hosts_text != hosts_text_old:
        print('HOSTS文件已更新')
        write_file(HOST_PATH, hosts_text)

def UpdateRoute():
    SetRemoteGateIP('103.255.202.185')      #日志服务器
    SetRemoteGateIP('103.255.202.216')      #ELK平台
    SetRemoteGateIP('121.5.97.164')         #网元服GM平台
    SetRemoteGateIP('210.242.203.135')      #台服GM平台
    SetRemoteGateIP('180.167.212.113')      #协作服GM平台
    SetRemoteGateIP('140.210.69.36')        #考勤
    SetRemoteGateIP('121.5.96.181')         #角色导入

def UpdateExtraInfo():
    response = requests.get('http://code.aurogon.com/pub/designer_tools/-/raw/master/OpenVPNTools/ExtraHosts.txt')
    if response.ok:
        global hosts_text
        hosts_text = read_file(HOST_PATH)
        hosts_text_old = hosts_text
        extra_hosts = response.text.split('\n')
        for line in extra_hosts:
            ip, hostname = line.split(' ')
            # print(ip, hostname)
            UpdateLine(ip, hostname)
        if hosts_text != hosts_text_old:
            write_file(HOST_PATH, hosts_text)
            print('额外HOSTS文件已更新')

    response = requests.get('http://code.aurogon.com/pub/designer_tools/-/raw/master/OpenVPNTools/ExtraRouteIP.txt')
    if response.ok:
        extra_route_ip = response.text.splitlines()
        for line in extra_route_ip:
            ip, desc = line.split(' ')
            SetRemoteGateIP(ip)



def main():
    global remote_gateway
    remote_gateway = get_sys_route('192.168.21.0')
    if not remote_gateway:
        print('获取远程网关失败，请确认已连接OpenVPN')
    else:
        UpdateRoute()
    UpdateHosts()
    UpdateExtraInfo()

    # os.system('pause')

if __name__ == "__main__":
    if is_admin():
        # Code of your program here
        main()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)