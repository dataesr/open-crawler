import json
import os
import pathlib

import repositories
from models.enums import MetadataType, ProcessStatus
from models.metadata import MetadataTask
from models.process import CrawlProcess
from services.accessibility_best_practices_calculator import (
    AccessibilityError,
    BestPracticesError,
)
from services.carbon_calculator import CarbonCalculatorError
from services.crawler_logger import logger
from services.responsiveness_calculator import ResponsivenessCalculatorError
from services.technologies_calculator import TechnologiesError


def handle_metadata_result(
    task: MetadataTask,
    crawl_process: CrawlProcess,
    result: dict,
    metadata_type: MetadataType,
):
    if not result:
        task.update(status=ProcessStatus.ERROR)
        repositories.crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        logger.error(f"{metadata_type} failed.")
        return
    store_metadata_result(crawl_process, result, metadata_type)
    if task.status == ProcessStatus.STARTED:
        task.update(status=ProcessStatus.SUCCESS)
        repositories.crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        logger.debug(f"{metadata_type} ended!")
    return result


def store_metadata_result(
    crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType
):
    base_file_path = f"{os.environ['LOCAL_FILES_PATH']}/{crawl_process.id}"
    file_path = pathlib.Path(
        f"{base_file_path}/{os.environ['METADATA_FOLDER_NAME']}/{metadata_type}.json"
    )
    file_path.parent.mkdir(exist_ok=True, parents=True)
    file_path.write_text(json.dumps(result, indent=4))


def metadata_task(
    task: MetadataTask,
    crawl_process: CrawlProcess,
    metadata_type: MetadataType,
    calculator,
    method_name: str,
):
    calc_method = getattr(calculator, method_name)
    result = {}
    task.update(status=ProcessStatus.STARTED)
    logger.debug(f"{metadata_type} started!")
    repositories.crawls.update_task(
        crawl_id=crawl_process.id,
        task_name=metadata_type,
        task=task,
    )
    if metadata_process := crawl_process.metadata.get(metadata_type):
        for url in metadata_process.urls:
            try:
                data = calc_method(url)
                result[url] = data
            except (
                AccessibilityError,
                BestPracticesError,
                TechnologiesError,
                ResponsivenessCalculatorError,
                CarbonCalculatorError,
            ) as e:
                logger.warning(
                    f"An error occurred for url {url} during {metadata_type} process. {e}"
                )
                if task.status != ProcessStatus.PARTIAL_ERROR:
                    task.update(status=ProcessStatus.PARTIAL_ERROR)
                    repositories.crawls.update_task(
                        crawl_id=crawl_process.id,
                        task_name=metadata_type,
                        task=task,
                    )
                continue
            except Exception as e:
                logger.error(
                    f"An unknown error occurred for url {url} during {metadata_type} process. {e}"
                )
                if task.status != ProcessStatus.PARTIAL_ERROR:
                    task.update(status=ProcessStatus.PARTIAL_ERROR)
                    repositories.crawls.update_task(
                        crawl_id=crawl_process.id,
                        task_name=metadata_type,
                        task=task,
                    )
                continue
    return handle_metadata_result(task, crawl_process, result, metadata_type)
