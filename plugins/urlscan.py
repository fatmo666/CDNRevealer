import requests
from typing import Dict, Union, List
from utils.logger import log

URLSCAN_URL = "https://urlscan.io/api/v1/search/?q=domain:{}"

async def plugin_urlscan(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    log.info(f"Starting Urlscan.io query for {domain}...")

    try:
        api_key = api_credentials["urlscan"]["api_key"]
        headers = {
            "API-Key": api_key
        }

        response = requests.get(URLSCAN_URL.format(domain), headers=headers, proxies=get_proxies(proxy_config))
        data = response.json()
        ips = []

        for result in data.get("results", []):
            ip = result.get("page", {}).get("ip", "")
            if ip:
                ips.append(ip)

        return {"status": "success", "is_bypass": "true", "ip_addresses": ips}
    except Exception as e:
        log.error(f"Urlscan.io query error: {e}")
        return {"status": "error", "is_bypass": "true", "message": str(e)}

def get_proxies(proxy_config):
    if proxy_config["enable"]:
        return {
            "http": proxy_config["http"],
            "https": proxy_config["https"]
        }
    return None
