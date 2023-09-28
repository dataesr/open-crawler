import unittest

from models.enums import MetadataType, ProcessStatus


class TestMetadataType(unittest.TestCase):
    def test_enum_members(self):
        # Check if the enum has the expected members
        self.assertEqual(MetadataType.ACCESSIBILITY, "accessibility")
        self.assertEqual(MetadataType.TECHNOLOGIES, "technologies_and_trackers")
        self.assertEqual(MetadataType.RESPONSIVENESS, "responsiveness")
        self.assertEqual(MetadataType.GOOD_PRACTICES, "good_practices")
        self.assertEqual(MetadataType.CARBON_FOOTPRINT, "carbon_footprint")

    def test_enum_member_count(self):
        # Check if the enum has only the expected members
        self.assertEqual(len(MetadataType), 5)


class TestProcessStatus(unittest.TestCase):
    def test_enum_members(self):
        self.assertEqual(ProcessStatus.PENDING, "pending")
        self.assertEqual(ProcessStatus.STARTED, "started")
        self.assertEqual(ProcessStatus.SUCCESS, "success")
        self.assertEqual(ProcessStatus.ERROR, "error")
        self.assertEqual(ProcessStatus.PARTIAL_ERROR, "partial_error")

    def test_enum_member_count(self):
        self.assertEqual(len(ProcessStatus), 5)


if __name__ == "__main__":
    unittest.main()
