import json

import requests
from Dict.ip import ip_api

def get_ip_range_from_column_1(response):
    return eval(response.text)

def get_ip_range_from_google_cloud_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['prefixes']:
            ip_prefix = item['ipv4Prefix']
            ip_ranges.append(ip_prefix)
    except:
        pass

    return ip_ranges

def get_ip_range_from_google_cloud_2(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['prefixes']:
            ip_prefix = item['ipv4Prefix']
            ip_ranges.append(ip_prefix)
    except:
        pass

    return ip_ranges

def get_ip_range_from_amazon_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['prefixes']:
            ip_prefix = item['ip_prefix']
            ip_ranges.append(ip_prefix)
    except:
        pass

    return ip_ranges

def get_ip_range_from_arvancloud_1(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_bing_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['prefixes']:
            ip_prefix = item['ipv4Prefix']
            ip_ranges.append(ip_prefix)
    except:
        pass

    return ip_ranges

def get_ip_range_from_cachefly_1(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_cloudflare_1(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_cloudflare_2(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_cloudfront_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict.items():
            ip_ranges = list(set(ip_ranges + item[1]))
    except:
        pass

    return ip_ranges

def get_ip_range_from_digitalocean_1(response):
    ip_ranges = response.text.split('\n')
    ip_ranges = [item.split(',')[0] for item in ip_ranges]

    return ip_ranges

def get_ip_range_from_fastly_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict.items():
            ip_ranges = list(set(ip_ranges + item[1]))
    except:
        pass

    return ip_ranges

def get_ip_range_from_maxcdn_1(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_microsoft_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['values']:
            ip_prefix = item['properties']['addressPrefixes']
            ip_ranges = list(set(ip_ranges + ip_prefix))
    except:
        pass

    return ip_ranges

def get_ip_range_from_microsoft_2(response):
    import xml.etree.ElementTree as ET
    ip_ranges = []
    try:
        root = ET.fromstring(response.text)
        for region in root.iter('Region'):
            for iprange in region.iter('IpRange'):
                ip_subnet = iprange.get('Subnet')
                ip_ranges.append(ip_subnet)
    except:
        pass

    return ip_ranges

def get_ip_range_from_oracle_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict['regions']:
            for itemm in item['cidrs']:
                ip_ranges.append(itemm['cidr'])
    except:
        pass

    return ip_ranges

def get_ip_range_from_alibaba_cloud_1(response):
    """
    待补充
    :param response:
    :return:
    """
    return []

def get_ip_range_from_tencent_cloud_1(response):
    """
    待补充
    :param response:
    :return:
    """
    return []

def get_ip_range_from_unknown_1(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_unknown_2(response):
    ip_ranges = response.text.split('\n')

    return ip_ranges

def get_ip_range_from_opensource_api_1(response):
    ip_ranges = []
    try:
        json_dict = json.loads(response.text)
        for item in json_dict.items():
            ip_ranges = list(set(list(ip_ranges + item[1])))
    except:
        pass

    return ip_ranges

def main():
    # 初始化一个空字典
    ip_ranges = {}

    # 遍历 ip_api 字典中的每个 API
    for api_name, api_urls in ip_api.items():

        # 初始化一个空列表，用于存储提取的 IP 段
        ip_list = []
        ip_ranges[api_name] = []
        count = 0

        # 循环遍历 API 列表中的每个 URL
        for api_url in api_urls:
            count += 1
            response = requests.get(api_url)

            # 判断响应是否成功
            if response.status_code == 200:
                # 根据 API 名称来调用相应的提取函数
                # 如果没有对应的函数，那么跳过这个 API
                try:
                    func_name = f'get_ip_range_from_{api_name.lower().replace(" ", "_")}_{str(count)}'
                    func = globals()[func_name]
                except KeyError:
                    continue

                # 调用提取函数获取 IP 段
                ip_list = func(response)

                # 将提取到的 IP 段添加到总字典中
                ip_ranges[api_name] = list(set(ip_ranges[api_name] + ip_list))

    # 打印结果
    print(ip_ranges)

if __name__ == '__main__':
    main()