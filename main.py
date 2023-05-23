import argparse
import asyncio
from utils.logger import log
import os
import yaml
from plugins import discover_plugins
from utils.compare_responses import compare_responses
import sys

# 如果是Windows则修改事件循环策略，兼容不同系统
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# 定义命令行参数解析
def get_args():
    parser = argparse.ArgumentParser(description="CDN Bypass Tool")
    parser.add_argument("-d", "--domain", type=str, required=True, help="Target domain")
    parser.add_argument("-p", "--plugin", type=str, default=None, help="Specify a plugin to use (default: all)")
    parser.add_argument("-c", "--config", type=str, default="config.yaml", help="Specify the config file (default: config.yaml)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file format (csv, json, html, text)")

    return parser.parse_args()

# 定义保存输出结果到文件
def save_output(domain, data, file_format):
    import json
    import csv

    filename = f"{domain}.{file_format}"

    if file_format == "json":
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=4)
    elif file_format == "csv":
        with open(filename, "w", newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["IP"])
            for ip in data:
                writer.writerow([ip])
    elif file_format == "html":
        with open(filename, "w") as outfile:
            outfile.write("<html><head><title>Results</title></head><body><table border='1'><tr><th>IP</th></tr>")
            for ip in data:
                outfile.write(f"<tr><td>{ip}</td></tr>")
            outfile.write("</table></body></html>")
    elif file_format == "text":
        with open(filename, "w") as outfile:
            for ip in data:
                outfile.write(f"{ip}\n")
    else:
        log.info("Invalid output format")

    log.info(f"Results saved in {filename}")

async def main(args):
    log.info("Starting the CDN Bypass Tool")

    domain = args.domain
    plugin_name = args.plugin
    config_path = args.config

    # 读取配置文件
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    proxy_config = config["proxy"]
    api_credentials = config["api_credentials"]

    # 自动发现插件
    PLUGIN_LIST = discover_plugins()

    tasks = []
    verified_ips = []

    # 根据指定的插件名创建任务
    if plugin_name and plugin_name != "all":
        plugin_names = plugin_name.split(',')
        for p_name in plugin_names:
            plugin = PLUGIN_LIST.get(p_name.strip())
            if plugin:
                tasks.append(plugin(domain, proxy_config, api_credentials))
            else:
                log.info(f"Plugin {p_name} not found.")
    else:
        # 如果未指定插件名或指定为 all，则使用所有插件
        for plugin in PLUGIN_LIST.values():
            tasks.append(plugin(domain, proxy_config, api_credentials))

    # 并发运行所有任务
    results = await asyncio.gather(*tasks)

    # 遍历结果，验证 IP 地址
    for result in results:
        if result["status"] == "success":
            ips = result.get("ip_addresses", [])
            for ip in ips:
                is_https = True if domain.startswith("https://") else False
                if compare_responses(ip, domain, is_https):
                    verified_ips.append(ip)

    log.info(f"Domain {domain}, Verified IPs: {verified_ips}")

    # 如果指定了输出格式，将结果保存到相应格式的文件中
    if args.output:
        save_output(domain, verified_ips, args.output)

if __name__ == "__main__":

    args = get_args()
    asyncio.run(main(args))
