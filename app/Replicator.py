import os, shutil
from my_logging import getMyLogger
import time
import sys

logger = getMyLogger(__name__)


class Replicator:

  lock_file = '/tmp/my_cron_job.lock'

  def create_lock(self):
    """Create a lock file to indicate the job is running."""
    try:
      with open(self.lock_file, 'x') as f:
        f.write(str(os.getpid()))  # Store the current PID
      return True
    except FileExistsError:
      # Lock file already exists
      return False

  def remove_lock(self):
    """Remove the lock file when the job is done."""
    if os.path.exists(self.lock_file):
      os.remove(self.lock_file)

  def sync(self, source_dir, replica_dir):
    # self.remove_lock()
    if not self.create_lock():
        logger.warning("Another instance is already running. Exiting.")
        sys.exit(1)

    logger.info(f"Syncing `{source_dir}` into `{replica_dir}`")

    # simulate long run (17 seconds)
    time.sleep(10)

    try:
      # Ensure target directory exists
      if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)

      # Sync files and directories
      for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        replica_path = os.path.join(replica_dir, item)

        if os.path.isdir(source_path):
          # Recursively sync directories
          self.sync(source_path, replica_path)
        else:
          # Check if the file needs to be copied
          if not os.path.exists(replica_path) or (os.path.getmtime(source_path) > os.path.getmtime(replica_path)):
            shutil.copy(source_path, replica_path)

      # Remove files in `replica` that are not in `source`
      for item in os.listdir(replica_dir):
        source_path = os.path.join(source_dir, item)
        replica_path = os.path.join(replica_dir, item)

        if not os.path.exists(source_path):
          if os.path.isdir(replica_path):
            # try to remove dir if empty
            try:
              os.rmdir(replica_path)
            except OSError:
              # Directory is not empty or cannot be removed
              pass
          else:
            # remove file
            os.remove(replica_path)
    finally:
      self.remove_lock()