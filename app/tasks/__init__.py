
from app.tasks.html_crawl.main import get_html_crawl
from app.tasks.lighthouse import get_lighthouse
from app.tasks.technologies import get_technologies
from app.tasks.carbon_footprint import get_carbon_footprint
from app.tasks.finalize import finalize_crawl_process

__all__ = ["get_html_crawl", "get_lighthouse", "get_technologies",
           "get_carbon_footprint", "finalize_crawl_process"]
