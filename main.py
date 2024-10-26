from src.Replicator import Replicator
from my_logging import getMyLogger
import argparse, logging

logger = getMyLogger(__name__)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Replicator argument parser.")
  parser.add_argument('sourceDir', help='Source folder')
  parser.add_argument('replicaDir', help='Replica folder')
  parser.add_argument('--logFilename', nargs='?', default='replicator.log', help='Log filename')

  args = parser.parse_args()

  replicator = Replicator(source_dir=args.sourceDir, replica_dir=args.replicaDir, log_filename=args.logFilename)
  replicator.sync()
