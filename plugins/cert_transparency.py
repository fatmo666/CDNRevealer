import requests
from typing import Dict, Union, List
from utils.logger import log
from utils.is_ipv4_address import is_ipv4_address

CT_URL = "https://crt.sh/?q={}&output=json"

async def plugin_cert_transparency(domain: str, proxy_config: Dict[str, str], config: Dict[str, str]) -> Dict[str, Union[str, List[str]]]:
    # 日志记录：开始使用 Certificate Transparency 插件查找IP
    log.info(f"begin to use Certificate Transparency deal with {domain}...")

    try:
        proxies = None
        if proxy_config["enable"]:
            proxies = {
                "http": proxy_config["http"],
                "https": proxy_config["https"]
            }

        response = requests.get(CT_URL.format(domain), proxies=proxies)
        data = response.json()
        ips = []

        for entry in data:
            ip = entry.get("name_value", "").strip()
            if ip and is_ipv4_address(ip):
                ips.append(ip)

        return {"status": "success", "is_bypass": "true", "ip_addresses": ips}
    except Exception as e:
        # 日志记录：Certificate Transparency插件出错
        log.error(f"Certificate Transparency error: {e}")
        return {"status": "error", "is_bypass": "true", "message": str(e)}
