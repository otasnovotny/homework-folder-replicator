from my_logging import getMyLogger

logger = getMyLogger(__name__)

if __name__ == '__main__':
  logger.debug("Debug log...")
  logger.info("Info log...")
  logger.warning("Warning log...")
  logger.error("error error...")
  logger.critical("Critical error...")