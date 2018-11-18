import billinfoscraper

default_form_url = 'https://mydom.dominionenergy.com:443/siteminderagent/forms/login.fcc'
default_target_url = 'https://mydom.dominionenergy.com'
if __name__ == '__main__':
	usage = "Web scraper that retrieves user electric bill info"
	parser = argparse.ArgumentParser(usage)
	parser.add_argument('username', nargs=1, help='username for electric bill')
	parser.add_argument('password', nargs=1, help='password for electric bill')
	parser.add_argument('-f','--form-url', dest='form_url', default=default_form_url, help='url login information form is submitted to')
	parser.add_argument('-t','--target-url', dest='target_url', default=default_target_url, help='base url login information form is submitted to')
	args = parser.parse_args()
	scraper = BillInfoScraper(args.username[0],args.password[0],args.target_url,args.form_url)
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