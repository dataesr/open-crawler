import json

from app.repositories.crawls import crawls
from app.repositories.files import files
from app.models.enums import MetadataType, ProcessStatus
from app.models.metadata import MetadataTask
from app.models.process import CrawlProcess
from app.services.lighthouse_calculator import LighthouseError
from app.services.carbon_calculator import CarbonCalculatorError
from app.services.crawler_logger import logger
from app.services.responsiveness_calculator import ResponsivenessCalculatorError
from app.services.technologies_calculator import TechnologiesError


def handle_metadata_result(
    task: MetadataTask,
    crawl_process: CrawlProcess,
    result: dict,
    metadata_type: MetadataType,
):
    if not result:
        task.update(status=ProcessStatus.ERROR)
        crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        logger.error(f"{metadata_type} failed.")
        return
    store_metadata_result(crawl_process, result, metadata_type)
    if task.status == ProcessStatus.STARTED:
        task.update(status=ProcessStatus.SUCCESS)
        crawls.update_task(
            crawl_id=crawl_process.id,
            task_name=metadata_type,
            task=task,
        )
        logger.debug(f"{metadata_type} ended!")
    return result


def store_metadata_result(
    crawl_process: CrawlProcess, result: dict, metadata_type: MetadataType
):
    return files.store_metadata_file(
        crawl_id=crawl_process.id,
        object_name=f"{metadata_type}.json",
        content_type='application/json',
        data=json.dumps(result, indent=2, default=str)
    )


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
    crawls.update_task(
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
                LighthouseError,
                TechnologiesError,
                ResponsivenessCalculatorError,
                CarbonCalculatorError,
            ) as e:
                logger.warning(
                    f"An error occurred for url {url} during {metadata_type} process. {e}"
                )
                if task.status != ProcessStatus.PARTIAL_ERROR:
                    task.update(status=ProcessStatus.PARTIAL_ERROR)
                    crawls.update_task(
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
                    crawls.update_task(
                        crawl_id=crawl_process.id,
                        task_name=metadata_type,
                        task=task,
                    )
                continue
    return handle_metadata_result(task, crawl_process, result, metadata_type)
