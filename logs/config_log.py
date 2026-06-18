import logging



logger = logging.getLogger('intelligence-mysql')

logger.setLevel(logging.INFO)

formatter =logging.Formatter(fmt= "%(asctime)s | %(levelname)s | %(message)s",datefmt="%y-%m-%d %H:%M:%S")


FileHandler = logging.FileHandler("logs/app.log","a",encoding="utf-8")
FileHandler.setFormatter(formatter)

streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)

logger.addHandler(FileHandler)
logger.addHandler(streamhandler)
