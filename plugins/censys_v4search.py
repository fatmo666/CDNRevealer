import asyncio
from typing import Dict, Union, List
from censys.search import CensysHosts
from utils.logger import log

async def plugin_censys_v4search(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    """
    插件：使用Censys查找域名对应的IP地址

    :param domain: 要查询的域名
    :param proxy_config: 代理配置，本插件不使用代理
    :return: 插件执行结果，包含状态和IP地址列表
    """
    log.info(f"Starting censys query for {domain}")

    # 从配置文件中获取 Censys API ID 和 Secret
    censys_api_id = api_credentials["censys"].get("api_id")
    censys_api_secret = api_credentials["censys"].get("api_secret")

    # 如果没有找到 API 凭据，记录错误并返回
    if not censys_api_id or not censys_api_secret:
        log.error("Censys API ID or Secret not found in config file.")
        return {"status": "error", "message": "Censys API credentials not found."}

    # 实例化 CensysIPv4 对象
    censys_ipv4 = CensysHosts(api_id=censys_api_id, api_secret=censys_api_secret)

    # 查询目标域名的 IPv4 地址
    try:
        search_results = censys_ipv4.search(f"{domain}")
    except Exception as e:
        log.error(f"Error in Censys search: {e}")
        return {"status": "error", "message": f"Error in Censys search: {e}"}

    # 提取 IPv4 地址
    ip_addresses = [result_key["ip"] for result_name, result_key in search_results.view_all()]

    return {"status": "success", "ip_addresses": ip_addresses}
