import os, re, json
import tempfile
from pathlib import Path

last_network_gateway = ''

# def get_local_gate():
#     wmi_obj = wmi.WMI()
#     wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
#     wmi_out = wmi_obj.query( wmi_sql )
#     for dev in wmi_out:
#         if dev.DefaultIPGateway:
#             global last_local_gateway
#             if last_local_gateway != '':
#                 print('检测到多个网关地址，无法识别：', last_local_gateway, dev.DefaultIPGateway[0])
#                 return False
#             last_local_gateway = dev.DefaultIPGateway[0]
#             # print("IPv4Address:", dev.IPAddress[0], "DefaultIPGateway:", dev.DefaultIPGateway[0])
#             print("检测到本地网卡网关：", dev.DefaultIPGateway[0])
#     return last_local_gateway

# def get_network_gateway():
#     ipconfig_table = os.popen('ipconfig')  # 使用os.popen()获取程序输出
#     all_lines = ipconfig_table.readlines()  # 按行读取
#     for line in all_lines:
#         if line.find('默认网关') != -1:
#             gateway = re.findall('\d+\.\d+\.\d+\.\d+', line)
#             if gateway:
#                 global last_network_gateway
#                 if last_network_gateway != '':
#                     print('检测到多个网关地址，无法识别：', last_network_gateway, gateway[0])
#                     return False
#                 last_network_gateway = gateway[0]
#                 print("检测到本地网卡网关：", gateway[0])
#     return last_network_gateway

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

def GetDirPath():
    dir_path = os.path.abspath(os.path.dirname(__file__)) + '\\'
    return dir_path
filename = Path(__file__).stem
json_file_path = tempfile.gettempdir() + '\\' + filename + '.json'

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

def reset_network():
    print('获取本地网关失败，正在重置本地网卡\n若重置失败，请在网络连接中，将本地网卡（或所有网卡）禁用再启用进行手动重置')
    os.system('route DELETE 0.0.0.0')
    os.system('ipconfig /release')
    os.system('ipconfig /renew')
    print('已重置本地网关，当前默认网关为', get_sys_route('0.0.0.0'))

def main():
    # network_gateway = get_network_gateway()
    local_now_gateway = get_sys_route('0.0.0.0')
    if not local_now_gateway:
        reset_network()
    else:
        remote_gateway = get_sys_route('192.168.21.0')
        if not remote_gateway:
            print('获取远程网关失败，请确认已连接OpenVPN')
        else:
            json_info = load_json(json_file_path)
            if local_now_gateway == remote_gateway:
                local_gateway = json_info['local_gateway']
                if not local_gateway or local_gateway == remote_gateway:
                    reset_network()
                else:
                    os.system('route DELETE 0.0.0.0')
                    os.system('route ADD 0.0.0.0 MASK 0.0.0.0 ' + local_gateway)
                    print('已切换到本地远程分流模式，当前默认网关为', get_sys_route('0.0.0.0'))
            # elif local_now_gateway == network_gateway:
            elif local_now_gateway != remote_gateway:
                # 记录本地网关地址
                json_info['local_gateway'] = local_now_gateway
                json_info['remote_gateway'] = remote_gateway
                write_json(json_file_path, json_info)
                os.system('route DELETE 0.0.0.0')
                os.system('route ADD 0.0.0.0 MASK 0.0.0.0 ' + remote_gateway)
                print('已切换到全局模式，当前默认网关为', get_sys_route('0.0.0.0'))
    os.system('pause')


if __name__ == "__main__":
    main()
