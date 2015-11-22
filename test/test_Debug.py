from unittest import TestCase

from debugTools import Debug


class TestDebug(TestCase):
	def test_severity_debuginfo(self):
		self.assertEqual(Debug.Severity.DebugInfo.value, 4)

	def test_severity_info(self):
		self.assertEqual(Debug.Severity.Info.value, 3)

	def test_severity_warning(self):
		self.assertEqual(Debug.Severity.Warning.value, 2)

	def test_severity_error(self):
		self.assertEqual(Debug.Severity.Error.value, 1)

	def test_severity_debuginfo_string(self):
		self.assertEqual(Debug.Severity.DebugInfo.__str__, "Debug")

	def test_severity_info_string(self):
		self.assertEqual(Debug.Severity.Info.__str__, "Info")

	def test_severity_warning_string(self):
		self.assertEqual(Debug.Severity.Warning.__str__, "Warning")

	def test_severity_error_string(self):
		self.assertEqual(Debug.Severity.Error.__str__, "Error")

	def test_severity_valueerror(self):
		self.assertRaises(ValueError)