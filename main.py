from my_logging import getMyLogger
import argparse, logging

logger = getMyLogger(__name__)

def add_logging_file_handler(filename: str) -> None:
  file_handler = logging.FileHandler(args.logFilename)
  file_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s'))
  file_handler.setLevel(logging.WARNING)
  logger.addHandler(file_handler)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Replicator argument parser.")
  parser.add_argument('sourceDir', help='Source folder')
  parser.add_argument('replicaDir', help='Replica folder')
  parser.add_argument('--logFilename', nargs='?', default='replicator.log', help='Log filename')

  args = parser.parse_args()
  add_logging_file_handler(args.logFilename)
  logger.info(f"Replicating from `{args.sourceDir}` to `{args.replicaDir}`. Logging to `{args.logFilename}`")

  # logger.debug("Debug log...")
  # logger.info("Info log...")
  # logger.warning("Warning log...")
  # logger.error("Error log...")
  # logger.critical("Critical log...")
