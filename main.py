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
    logger.info(f"Scheduler started — report runs daily at {REPORT_HOUR:02d}:{REPORT_MINUTE:02d} UTC.")
    scheduler.start()


import logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    run_report()