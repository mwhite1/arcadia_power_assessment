import sys
import requests
import argparse
import re
from bs4 import BeautifulSoup

class LoginException(Exception):
	pass

class LockedAccountException(LoginException):
	pass

class InvalidLoginException(LoginException):
	pass

class BillInfoScraper(object):
	def __init__(self,username,password,target_host,form_url):
		self.form_url = form_url
		self.target_host = target_host
		self.username = username
		self.password = password
		self.bill_due_date = None
		self.bill_amount = None
		self.usage_data = []

	def get_account_page_content(self):
		data = {'__EVENTTARGET':'','__EVENTARGUMENT':'','smauthreason':0,'target':self.target_host,'user':self.username,'password':self.password}
		request = requests.post(self.form_url,data=data)
		return BeautifulSoup(request.content,"html.parser")

	def __repr__(self):
		underline = "".ljust(20,"-")
		header_line = "Bill Info for {username}\n{underline}".format(username=self.username,underline=underline)
		payment_info_header = "\nPayment Info\n{underline}".format(underline=underline)
		due_date_line = "Payment Due Date: {due_date}".format(due_date=self.bill_due_date)
		payment_line = "Payment Amount: {payment_amount}".format(payment_amount=self.bill_amount)
		usage_header = "\nEnergy Usage(kWh)\n{underline}".format(underline=underline)
		usage_data_str = "\n".join(["{date}: {amount}".format(date=date,amount=amount) for date,amount in self.usage_data])
		return "\n".join([header_line,payment_info_header,due_date_line,payment_line,usage_header,usage_data_str])

	def verify_account_page_content(self,content):
		account_form = content.find("form")
		if not account_form:
			return True
		else:
			if account_form.attrs['name'] == 'PWChange':
				raise LockedAccountException()
			else:
				raise InvalidLoginException()

	def get_bill_info(self):
		content = self.get_account_page_content()
		self.verify_account_page_content(content)
		homepage_content = content.find(id='homepageContent')
		payment_info_elements = homepage_content.find_all('span','bodyTextGreen')
		self.bill_due_date = payment_info_elements[0].get_text(strip=True)
		self.bill_amount = payment_info_elements[1].get_text(strip=True)
		usage_data_elem_value = homepage_content.find(id='UsageDataArrHdn').attrs['value']
		usage_data_pairs = re.findall('\d+,\d+',usage_data_elem_value)
		usage_data_kwh = [pair.split(",")[1] for pair in usage_data_pairs]
		usage_data_dates = homepage_content.find(id='UsageDateArrHdn').attrs['value'].split(',')
		usage_data_len = len(usage_data_dates)
		for i,_ in reversed(list(enumerate(usage_data_dates))):
			self.usage_data.append((usage_data_dates[i],usage_data_kwh[i]))