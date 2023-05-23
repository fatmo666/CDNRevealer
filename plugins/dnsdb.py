import requests
from typing import Dict, Union, List
from utils.logger import log

DNSDB_URL = "https://api.dnsdb.info/lookup/rrset/name/*.{}/A"

async def plugin_dnsdb(domain: str, proxy_config: Dict[str, str], api_credentials: Dict[str, Dict[str, str]]) -> Dict[str, Union[str, List[str]]]:
    log.info(f"Starting DNSDB query for {domain}...")

    try:
        api_key = api_credentials["dnsdb"]["api_key"]
        headers = {
            "Accept": "application/json",
            "X-API-Key": api_key
        }

        response = requests.get(DNSDB_URL.format(domain), headers=headers, proxies=get_proxies(proxy_config))
        data = response.json()
        ips = []

        for entry in data:
            if "rdata" in entry:
                ips.extend(entry["rdata"])

        return {"status": "success", "ip_addresses": ips}
    except Exception as e:
        log.error(f"DNSDB query error: {e}")
        return {"status": "error", "message": str(e)}

def get_proxies(proxy_config):
    if proxy_config["enable"]:
        return {
            "http": proxy_config["http"],
            "https": proxy_config["https"]
        }
    return None
