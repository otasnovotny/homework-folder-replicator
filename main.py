from src.Replicator import Replicator
from my_logging import getMyLogger
import argparse, logging
import os

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

  replicator = Replicator(source_dir=args.sourceDir, replica_dir=args.replicaDir, log_filename=args.logFilename)
  replicator.sync()
