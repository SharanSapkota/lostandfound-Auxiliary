import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from api_client import ApiClient
from report_generator import ReportGenerator
from config import REPORT_HOUR, REPORT_MINUTE

logger = logging.getLogger(__name__)

def run_report():
    try:
        client = ApiClient()
        client.login()
        generator = ReportGenerator(client)
        report = generator.generate()
        generator.print_report(report)
    except Exception as e:
        logger.error(f"Report generation failed: {e}")


def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_report,
        trigger=CronTrigger(hour=REPORT_HOUR, minute=REPORT_MINUTE),
        id="daily_report",
        replace_existing=True,
    )
    scheduler.start()