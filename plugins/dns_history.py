import requests
from typing import Dict, Union, List
from utils.logger import log

DNS_HISTORY_URL = "https://api.securitytrails.com/v1/history/{}/dns/a"


async def plugin_dns_history(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> \
Dict[str, Union[str, List[str]]]:
    log.info(f"Starting DNS History lookup for {domain}...")

    try:
        api_key = api_credentials["security_trails"]["api_key"]
        headers = {
            "APIKEY": api_key,
        }

        response = requests.get(DNS_HISTORY_URL.format(domain), headers=headers, proxies=get_proxies(proxy_config))
        data = response.json()
        records = data["records"]
        ips = set()

        for record in records:
            for ip in record["values"]:
                ips.add(ip["ip"])

        return {"status": "success", "is_bypass": "true", "ip_addresses": list(ips)}
    except Exception as e:
        log.error(f"DNS History lookup error: {e}")
        return {"status": "error", "is_bypass": "true", "message": str(e)}


def get_proxies(proxy_config):
    if proxy_config["enable"]:
        return {
            "http": proxy_config["http"],
            "https": proxy_config["https"]
        }
    return None
