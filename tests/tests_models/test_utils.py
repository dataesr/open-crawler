import unittest
from uuid import UUID

from models.enums import ProcessStatus
from models.utils import get_uuid, BaseTaskModel


class TestGetUUIDFunction(unittest.TestCase):
    def test_get_uuid_returns_valid_uuid(self):
        uuid_str = get_uuid()
        try:
            uuid_obj = UUID(uuid_str, version=4)
            self.assertEqual(uuid_str, str(uuid_obj))
        except ValueError:
            self.fail("get_uuid() did not return a valid UUID4")


class TestBaseTaskModel(unittest.TestCase):
    def test_default_values(self):
        task = BaseTaskModel()

        self.assertIsNone(task.task_id)
        self.assertIsNone(task.started_at)
        self.assertIsNone(task.finished_at)
        self.assertEqual(task.status, ProcessStatus.PENDING)

    def test_update_method(self):
        task = BaseTaskModel()

        # Update the task_id only
        new_task_id = "new_id_123"
        task.update(task_id=new_task_id)
        self.assertEqual(task.task_id, new_task_id)
        self.assertIsNone(task.started_at)
        self.assertIsNone(task.finished_at)
        self.assertEqual(task.status, ProcessStatus.PENDING)

        # Update the status to STARTED
        task.update(status=ProcessStatus.STARTED)
        self.assertIsNotNone(task.started_at)
        self.assertIsNone(task.finished_at)
        self.assertEqual(task.status, ProcessStatus.STARTED)

        # Update the status to SUCCESS
        task.update(status=ProcessStatus.SUCCESS)
        self.assertIsNotNone(task.finished_at)
        self.assertEqual(task.status, ProcessStatus.SUCCESS)


if __name__ == "__main__":
    unittest.main()
