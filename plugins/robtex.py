import requests
from typing import Dict, Union, List
from utils.logger import log

ROBTEX_URL = "https://freeapi.robtex.com/ipquery/{}"

async def plugin_robtex(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    log.info(f"Starting Robtex IP query for {domain}...")

    try:
        response = requests.get(ROBTEX_URL.format(domain), proxies=get_proxies(proxy_config))
        data = response.json()
        ips = []

        if "pas" in data:
            for entry in data["pas"]:
                if "o" in entry:
                    ips.append(entry["o"])

        return {"status": "success", "ip_addresses": ips}
    except Exception as e:
        log.error(f"Robtex IP query error: {e}")
        return {"status": "error", "message": str(e)}

def get_proxies(proxy_config):
    if proxy_config["enable"]:
        return {
            "http": proxy_config["http"],
            "https": proxy_config["https"]
        }
    return None
