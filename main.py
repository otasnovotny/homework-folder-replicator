from logging import Logger
from src.Replicator import Replicator
from my_logging import getMyLogger
import argparse, logging
from apscheduler.schedulers.blocking import BlockingScheduler

def sync_job(source_dir: str, replica_dir: str, logger: Logger):
  replicator = Replicator(source_dir=source_dir, replica_dir=replica_dir, logger=logger)
  replicator.sync()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Replicator argument parser.")
  parser.add_argument('sourceDir', help='Source folder')
  parser.add_argument('replicaDir', help='Replica folder')
  parser.add_argument('intervalSeconds', help='Cron interval in seconds')
  parser.add_argument('logFilename', help='Log filename')
  args = parser.parse_args()

  interval_seconds = int(args.intervalSeconds)
  if interval_seconds < 0:
    raise ValueError

  logger = getMyLogger(__name__)
  file_handler = logging.FileHandler(args.logFilename)
  file_handler.setFormatter(logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s'))
  # file_handler.setLevel(logging.WARNING)
  logger.addHandler(file_handler)

  scheduler = BlockingScheduler()
  scheduler.add_job(
    sync_job, 'interval', seconds=interval_seconds, args=[args.sourceDir, args.replicaDir, logger]
  )

  try:
    logger.debug("Scheduler started.")
    scheduler.start()
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
