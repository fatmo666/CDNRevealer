import aiodns
import asyncio
from typing import Dict, List, Union
from utils.logger import log

async def async_dns_lookup(domain: str) -> List[str]:
    resolver = aiodns.DNSResolver()
    try:
        results = await resolver.query(domain, 'A')
        return [result.host for result in results]
    except aiodns.error.DNSError as e:
        log.error(f"DNS解析错误，域名：{domain}, 错误信息：{e}")
        return []

async def plugin_dns_resolve(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    """
    插件：使用DNS解析查找域名对应的IP地址

    :param domain: 要查询的域名
    :param proxy_config: 代理配置，本插件不使用代理
    :return: 插件执行结果，包含状态和IP地址列表
    """

    log.info(f"Starting DNS resolve for {domain}")

    dns_servers = ["8.8.8.8", "8.8.4.4"]  # 使用Google DNS服务器
    ip_addresses = []

    # 异步处理DNS查询
    for dns_server in dns_servers:
        log.info(f"Use DNS server {dns_server} to resolve")
        resolver = aiodns.DNSResolver(nameservers=[dns_server])
        try:
            results = await resolver.query(domain, 'A')
            ip_addresses.extend([result.host for result in results])
        except aiodns.error.DNSError as e:
            log.error(f"DNS resolve fail，domain：{domain}, DNS server：{dns_server}, err msg：{e}")

    ip_addresses = list(set(ip_addresses))  # 去除重复的IP地址
    log.info(f"Plugin 'dns_resolve' get the ip address：{ip_addresses}")

    return {"status": "success" if ip_addresses else "failed", "ip_addresses": ip_addresses}
