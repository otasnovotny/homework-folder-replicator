import os
import shutil
from unittest import TestCase

from src.Replicator import Replicator
from settings import ROOT_DIR

TMP_DIR = os.path.join(ROOT_DIR, 'tmp')
SOURCE_DIR = os.path.join(TMP_DIR, 'source')
REPLICA_DIR = os.path.join(TMP_DIR, 'replica')

class TestReplicator(TestCase):

	def setUp(self):
		# prepare `source` dir
		if os.path.exists(SOURCE_DIR):
			shutil.rmtree(SOURCE_DIR)
		os.makedirs(SOURCE_DIR, exist_ok=True)

		# prepare `replica` dir
		if os.path.exists(REPLICA_DIR):
			shutil.rmtree(REPLICA_DIR)
		os.makedirs(REPLICA_DIR, exist_ok=True)

		self.replicator = Replicator(
			source_dir=SOURCE_DIR, replica_dir=REPLICA_DIR, log_filename=f"{ROOT_DIR}/replicator.log"
		)

	def tearDown(self):
		# I suppose I can use rmtree here ;-)
		shutil.rmtree(SOURCE_DIR, ignore_errors=True)
		shutil.rmtree(REPLICA_DIR, ignore_errors=True)

	def test_sync_file_in_dir(self):
		"""Test copy file"""

		# before action
		filename = 'test.txt'
		dirname = 'some_dir'

		source_dir_path =  os.path.join(SOURCE_DIR, dirname)
		source_file_path = os.path.join(source_dir_path, filename)
		os.makedirs(source_dir_path, exist_ok=True)

		replica_dir_path = os.path.join(REPLICA_DIR, dirname)
		replica_file_path = os.path.join(replica_dir_path, filename)

		with open(source_file_path, 'w') as source_file:
			source_file.write("This is a new file.\n")

		self.assertEqual(os.path.exists(source_file_path), True)
		self.assertEqual(os.path.exists(replica_file_path), False)

		# action
		self.replicator.sync()

		# after action
		self.assertEqual(os.path.exists(source_file_path), True)
		self.assertEqual(os.path.exists(replica_file_path), True)

	def test_remove_non_existing(self):
		"""Test remove file / dir from `replica` if it does not exist in `source`"""

		# before action
		filename = 'test.txt'
		dirname = 'some_dir'

		source_dir_path = os.path.join(SOURCE_DIR, dirname)
		source_file_path = os.path.join(source_dir_path, filename)

		replica_dir_path = os.path.join(REPLICA_DIR, dirname)
		replica_file_path = os.path.join(replica_dir_path, filename)
		os.makedirs(replica_dir_path, exist_ok=True)

		with open(replica_file_path, 'w') as replica_file:
			replica_file.write("This is a leftover file in `replica`.\n")

		self.assertEqual(os.path.exists(source_file_path), False)
		self.assertEqual(os.path.exists(replica_file_path), True)

		# action
		self.replicator.sync()

		# after action
		self.assertEqual(os.path.exists(source_file_path), False)
		self.assertEqual(os.path.exists(replica_file_path), False)
		self.assertEqual(os.path.exists(replica_dir_path), False)