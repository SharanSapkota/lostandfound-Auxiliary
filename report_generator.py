import logging
from datetime import datetime, timedelta
from api_client import ApiClient

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, client: ApiClient):
        self.client = client

    def generate(self) -> dict:
        since = datetime.utcnow() - timedelta(hours=24)

        all_items = self.client.get_all_items()
        all_pickups = self.client.get_all_pickups()

        new_items = [
            i for i in all_items
            if datetime.fromisoformat(i["created_at"]) >= since
        ]
        available_items = [i for i in all_items if i["status"] == "available"]
        returned_items = [i for i in all_items if i["status"] == "returned"]

        all_claims = []
        for item in all_items:
            claims = self.client.get_all_claims_for_item(item["id"])
            all_claims.extend(claims)

        new_claims = [
            c for c in all_claims
            if datetime.fromisoformat(c["created_at"]) >= since
        ]
        approved_claims = [c for c in all_claims if c["status"] == "approved"]
        rejected_claims = [c for c in all_claims if c["status"] == "rejected"]
        pending_claims = [c for c in all_claims if c["status"] == "pending"]

        pickups_today = [
            p for p in all_pickups
            if datetime.fromisoformat(p["picked_up_at"]) >= since
        ]

        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "period": "last_24_hours",
            "items": {
                "new_reported": len(new_items),
                "still_available": len(available_items),
                "returned": len(returned_items),
            },
            "claims": {
                "new_submitted": len(new_claims),
                "approved": len(approved_claims),
                "rejected": len(rejected_claims),
                "pending": len(pending_claims),
            },
            "pickups": {
                "completed": len(pickups_today),
            },
        }

        return report

    def print_report(self, report: dict):
        logger.info("========== DAILY REPORT ==========")
        logger.info(f"Generated at  : {report['generated_at']}")
        logger.info(f"Period        : {report['period']}")
        logger.info("--- Items ---")
        logger.info(f"New reported  : {report['items']['new_reported']}")
        logger.info(f"Available     : {report['items']['still_available']}")
        logger.info(f"Returned      : {report['items']['returned']}")
        logger.info("--- Claims ---")
        logger.info(f"New submitted : {report['claims']['new_submitted']}")
        logger.info(f"Approved      : {report['claims']['approved']}")
        logger.info(f"Rejected      : {report['claims']['rejected']}")
        logger.info(f"Still pending : {report['claims']['pending']}")
        logger.info("--- Pickups ---")
        logger.info(f"Completed     : {report['pickups']['completed']}")
