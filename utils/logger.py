import logging

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(funcName)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # 将日志输出到控制台
        logging.FileHandler("run.log", mode="a", encoding="utf-8")  # 将日志输出到文件
    ]
)

log = logging.getLogger(__name__)

# 如果需要在其他模块中使用此日志记录器，只需从该模块导入log对象即可