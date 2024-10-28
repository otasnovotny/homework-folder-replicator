import os, shutil
from logging import Logger
import time
import sys
from settings import ROOT_DIR


class Replicator:
  lock_file = f"{ROOT_DIR}/tmp/replicator.lock"

  def __init__(self, source_dir: str, replica_dir, logger: Logger, sleep: int = 0):
    self.source_dir = source_dir
    self.replica_dir = replica_dir
    self.logger = logger
    self.sleep = sleep  # Optional sleep for development purposes to simulate a long run

  def _create_lock(self):
    """Create a lock file to indicate the job is running."""

    directory = os.path.dirname(self.lock_file)
    # Create the directory if it does not exist
    if directory:
      os.makedirs(directory, exist_ok=True)

    try:
      with open(self.lock_file, 'x') as f:
        f.write(str(os.getpid()))  # Store the current PID
      return True
    except FileExistsError:
      # Lock file already exists
      return False

  def _remove_lock(self):
    """Remove the lock file when the job is done."""
    if os.path.exists(self.lock_file):
      os.remove(self.lock_file)

  def _replicate_dir(self, source_dir: str, replica_dir: str):
    """
    Do it recursively due to spec: No 3rd libraries
    Otherwise: shutil.copytree(source_dir, target_dir)
    """
    # self.logger.info(f"Syncing `{source_dir}` into `{replica_dir}`")

    # Ensure target directory exists
    if not os.path.exists(replica_dir):
      os.makedirs(replica_dir)

    # Sync files and directories
    for item in os.listdir(source_dir):
      source_path = os.path.join(source_dir, item)
      replica_path = os.path.join(replica_dir, item)

      if os.path.isdir(source_path):
        # Recursively sync directories
        self._replicate_dir(source_path, replica_path)
      else:
        ## Check if the file needs to be copied
        # if not os.path.exists(replica_path) or (os.path.getmtime(source_path) > os.path.getmtime(replica_path)):
        #   shutil.copy(source_path, replica_path)

        if os.path.exists(replica_path):
          self.logger.info(f"Updating `{replica_path}` from {source_path}")
        else:
          self.logger.info(f"Creating `{replica_path}` from `{source_path}`")

        try:
          shutil.copy(source_path, replica_path)
        except Exception as e:
          self.logger.error(e)

    # Remove files in `replica` that are not in `source`
    for item in os.listdir(replica_dir):
      source_path = os.path.join(source_dir, item)
      replica_path = os.path.join(replica_dir, item)

      if not os.path.exists(source_path):
        if os.path.isdir(replica_path):
          # remove dir recursively
          self._remove_dir(dir_path=replica_path)
        else:
          # remove file
          self.logger.info(f"Removing `{replica_path}`")
          try:
            os.remove(replica_path)
          except Exception as e:
            self.logger.error(e)

  def _remove_dir(self, dir_path: str):
    """
    Do it recursively due to spec: No 3rd libraries
    Otherwise: shutil.rmtree(target_path)
    """
    if os.path.exists(dir_path) and os.path.isdir(dir_path):

      # Iterate through all the items in the directory
      for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)  # Get full path of the item
        if os.path.isdir(item_path):
          # If it's a directory, recursively remove it
          self._remove_dir(item_path)
        else:
          # If it's a file, remove it
          self.logger.info(f"Removing file `{item_path}`")
          try:
            os.remove(item_path)
          except Exception as e:
            self.logger.error(e)

      # Finally, remove the empty directory
      self.logger.info(f"Removing empty directory `{dir_path}`")
      try:
        os.rmdir(dir_path)
      except Exception as e:
        self.logger.error(e)
    else:
      self.logger.error(f"The directory does not exist or is not a directory: {dir_path}")

  def sync(self):
    self.logger.info("== Sync triggered ==")
    if not self._create_lock():
      self.logger.warning("Another instance is already running. Exiting.")
      # sys.exit(1)
      return

    try:
      self._replicate_dir(source_dir=self.source_dir, replica_dir=self.replica_dir)

      if self.sleep > 0:
        time.sleep(self.sleep)

    finally:
      self._remove_lock()
