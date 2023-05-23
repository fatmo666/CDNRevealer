import http.client
from utils.logger import log
from urllib.parse import urlparse

def compare_responses(ip, domain, is_https=False):
    try:
        # 解析输入的域名
        url = urlparse(domain)
        # 获取域名
        domain_name = url.netloc if url.netloc else domain

        # 根据是否为 HTTPS 协议选择连接类
        connection_class = http.client.HTTPSConnection if is_https else http.client.HTTPConnection

        # 用 IP 建立连接
        connection_ip = connection_class(ip, timeout=5)
        connection_ip.putrequest("GET", url.path)
        connection_ip.putheader("Host", domain_name)
        connection_ip.endheaders()
        # 获取 IP 的响应和内容
        response_ip = connection_ip.getresponse()
        content_ip = response_ip.read()

        # 用域名建立连接
        connection_domain = connection_class(domain_name, timeout=5)
        connection_domain.request("GET", url.path)
        # 获取域名的响应和内容
        response_domain = connection_domain.getresponse()
        content_domain = response_domain.read()

        # 比较 IP 和域名请求的内容是否相同
        return content_ip == content_domain
    except Exception as e:
        # 如果发生异常，打印错误信息并返回 False
        log.error(f"Error comparing responses: {e}")
        return False