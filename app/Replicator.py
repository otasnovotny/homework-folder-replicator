import os, shutil
from my_logging import getMyLogger

logger = getMyLogger(__name__)


class Replicator:

  def sync(self, source_dir, replica_dir):
    logger.info(f"Syncing `{source_dir}` into `{replica_dir}`")

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