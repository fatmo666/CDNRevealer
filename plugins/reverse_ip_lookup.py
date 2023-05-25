import requests
from typing import Dict, Union, List
from utils.logger import log

REVERSE_IP_LOOKUP_URL = "https://api.bing.com/api/v7.0/IP?"


async def plugin_reverse_ip_lookup(domain: str, proxy_config: Dict[str, str],
                                   api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    log.info(f"Starting Reverse IP Lookup for {domain}...")

    try:
        api_key = api_credentials["bing"]["api_key"]
        params = {
            "q": domain,
            "subscription-key": api_key
        }

        response = requests.get(REVERSE_IP_LOOKUP_URL, params=params, proxies=get_proxies(proxy_config))
        data = response.json()
        ips = [entry["ip"] for entry in data["results"]]

        return {"status": "success", "is_bypass": "true", "ip_addresses": ips}
    except Exception as e:
        log.error(f"Reverse IP Lookup error: {e}")
        return {"status": "error", "is_bypass": "true", "message": str(e)}


def get_proxies(proxy_config):
    if proxy_config["enable"]:
        return {
            "http": proxy_config["http"],
            "https": proxy_config["https"]
        }
    return None
