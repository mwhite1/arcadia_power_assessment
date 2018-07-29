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

if __name__ == '__main__':
	usage = "Web scraper that retrieves user electric bill info"
	parser = argparse.ArgumentParser()
	parser.add_argument('-u','--username', dest='username', required=True)
	parser.add_argument('-p','--password', dest='password', required=True)
	parser.add_argument('-f','--form-url', dest='form_url', default='https://mydom.dominionenergy.com:443/siteminderagent/forms/login.fcc')
	parser.add_argument('-t','--target-url', dest='target_url', default='https://mydom.dominionenergy.com')
	args = parser.parse_args()
	scraper = BillInfoScraper(args.username,args.password,args.target_url,args.form_url)
	try:
		scraper.get_bill_info()
	except LoginException as e:
		if e.__class__.__name__ == "InvalidLoginException":
			print("invalid login information for %s" % args.username)
			sys.exit(1)
		else:
			print("%s account is locked" % args.username)
			sys.exit(1)
	except requests.ConnectionError as e:
		print("Connection error: %s" % e)
		sys.exit(1)
	print(scraper)

