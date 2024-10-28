from src.Replicator import Replicator
from my_logging import getMyLogger
import argparse
from apscheduler.schedulers.blocking import BlockingScheduler

logger = getMyLogger(__name__)

def sync_job(source_dir, replica_dir, log_filename):
  replicator = Replicator(source_dir=source_dir, replica_dir=replica_dir, log_filename=log_filename)
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

  scheduler = BlockingScheduler()
  scheduler.add_job(
    sync_job, 'interval', seconds=interval_seconds, args=[args.sourceDir, args.replicaDir, args.logFilename]
  )

  try:
    logger.debug("Scheduler started.")
    scheduler.start()
  except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
