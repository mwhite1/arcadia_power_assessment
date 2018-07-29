import unittest
import os
import bill_info_scraper
from mock import Mock
from mock import patch
import requests

class TestBillInfoScraper(unittest.TestCase):
	def testValidAccountPage(self):
		"""
		Testing to see if no exception is raised when html content represents
		valid login information
		"""
		account_page = os.path.join("test_files","account_page.html")
		with open(account_page,"rb") as fh:
			mock_content = fh
			with patch.object(requests,"post") as post_mock:
				post_mock.return_value = mock_response = Mock()
				mock_response.content = fh
				scraper = bill_info_scraper.BillInfoScraper("test","test","test","test")
				scraper.get_bill_info()
	def testInvalidAccountPage(self):
		"""
		Verifying InvalidLoginException gets raised in the event user enters
		invalid login information
		"""
		incorrect_login_page = os.path.join("test_files","invalid_login.html")
		with open(incorrect_login_page,"rb") as fh:
			mock_content = fh
			with patch.object(requests,"post") as post_mock:
				post_mock.return_value = mock_response = Mock()
				mock_response.content = fh
				scraper = bill_info_scraper.BillInfoScraper("test","test","test","test")
				self.assertRaises(bill_info_scraper.InvalidLoginException,scraper.get_bill_info)
	def testLockedAccountPage(self):
		"""
		Verifying LockedException gets raised in the event user locks their account
		"""
		locked_account_page = os.path.join("test_files","account_locked.html")
		with open(locked_account_page,"rb") as fh:
			mock_content = fh
			with patch.object(requests,"post") as post_mock:
				post_mock.return_value = mock_response = Mock()
				mock_response.content = fh
				scraper = bill_info_scraper.BillInfoScraper("test","test","test","test")
				self.assertRaises(bill_info_scraper.LockedAccountException,scraper.get_bill_info)


if __name__ == "__main__":
	unittest.main()


