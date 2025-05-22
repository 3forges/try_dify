import logging
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.speechtotext.whisper_service import whisper_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 50  # 50 minutes
wait_seconds = 60 * 45  # 45 minutes


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        whisper_service.init_model()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing Whisper AI")
    init()
    logger.info("Whisper AI finished initializing")


if __name__ == "__main__":
    main()
