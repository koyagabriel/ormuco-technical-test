import unittest
from comp_str import compare_string


class CompareStringTest(unittest.TestCase):

	def setUp(self):

		self.data = [
			("1.1", "1.2", "1.1 is less than 1.2"),
			("1.1", "1.1", "1.1 is equal to 1.1"),
			("1.2", "1.1", "1.2 is greater than 1.1")
		]

		self.data2 = [
			("1.4", "1.2", "1.4 is less than 1.2"),
			("1.1", "1", "1.1 is equal to 1"),
			("1.2", "1.4", "1.2 is greater than 1.4")
		]

	
	def test_comparison_truthy(self):
		for value in self.data:
			result = compare_string(value[0], value[1])
			self.assertEqual(result, value[2])

	def test_comparison_falsy(self):
		for value in self.data2:
			result = compare_string(value[0], value[1])
			self.assertNotEqual(result, value[2])
		


if __name__ == '__main__':
	unittest.main()