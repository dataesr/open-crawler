import logging

logger = logging.getLogger("open-crawler")
logger.setLevel(logging.DEBUG)


def set_file(crawl_id: str):
    fh = logging.FileHandler(filename=f"/logs/{crawl_id}.log", mode="a")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] (%(asctime)s): %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
