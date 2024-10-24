from unittest import TestCase

from app.Replicator import Replicator
from settings import SOURCE_DIR, REPLICA_DIR


class TestReplicator(TestCase):

	def setUp(self):
		self.replicator = Replicator()

	def test_sync(self):
		self.replicator.sync(source_dir=SOURCE_DIR, replica_dir=REPLICA_DIR)