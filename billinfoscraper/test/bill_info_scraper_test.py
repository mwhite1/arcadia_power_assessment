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
		bill_due_date = 'August 16, 2018'
		payment_amount = '$114.09'
		usage = [('01/25/2017','704'),('02/23/2017','493'),('03/24/2017','582'),('04/25/2017','961'),('05/24/2017','751'),('06/23/2017','957'),('07/25/2017','1272'),('08/23/2017','1138'),('09/22/2017','1081'),('10/23/2017', '1022'),('11/22/2017','798'),('12/22/2017','638'),('01/24/2018','604'),('02/22/2018','482'),('03/23/2018','631'),('04/24/2018','674'),('05/23/2018','859'),('06/22/2018','985'),('07/24/2018','1098')]
		with open(account_page,"rb") as fh:
			mock_content = fh
			with patch.object(requests,"post") as post_mock:
				post_mock.return_value = mock_response = Mock()
				mock_response.content = fh
				scraper = bill_info_scraper.BillInfoScraper("test","test","test","test")
				scraper.get_bill_info()
		self.assertEquals(bill_due_date,scraper.bill_due_date)
		self.assertEquals(payment_amount,scraper.bill_amount)
		self.assertEquals(usage,scraper.usage_data)
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


