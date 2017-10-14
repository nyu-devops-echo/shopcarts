import unittest
from models.dataerror import DataValidationError
from models.shopcart import Shopcart
from mock import patch

class TestProduct(unittest.TestCase):
	"""Data Error Model"""
	@patch('models.shopcart.Shopcart')
	def test_error(self, error_mock):
		"""Test that error can be raised"""
		error_mock.side_effect = DataValidationError()
		self.assertRaises(DataValidationError)

if __name__ == '__main__':
    unittest.main()
