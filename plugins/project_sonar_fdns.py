import requests
from typing import Dict, Union, List
from utils.logger import log

SONAR_API_URL = "https://sonar.omnisint.io/all/{}"

async def plugin_project_sonar_fdns(domain: str, proxy_config: Dict[str, str], config: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:
    # 日志记录：开始使用 Project Sonar Forward DNS 插件查找IP
    log.info(f"begin to use Project Sonar Forward DNS deal with {domain}...")

    try:
        proxies = None
        if proxy_config["enable"]:
            proxies = {
                "http": proxy_config["http"],
                "https": proxy_config["https"]
            }

        response = requests.get(SONAR_API_URL.format(domain), proxies=proxies)
        data = response.text.split('\n')
        ips = []

        for entry in data:
            ip = entry.strip()
            if ip:
                ips.append(ip)

        return {"status": "success", "ip_addresses": ips}
    except Exception as e:
        # 日志记录：Project Sonar Forward DNS 插件出错
        log.error(f"Project Sonar Forward DNS error: {e}")
        return {"status": "error", "message": str(e)}
