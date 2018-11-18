========================
Arcadia Power Assessment
========================
This repository contains the code for the Arcadia Power assessment

Prerequisites
=============
    Install Python 3.7
    pip install requests
    pip install beautifulsoup4
    pip install mock

bill_info_scraper.py
====================
    Web scraper that retrieves user power bill information
    usage: python bill_info_scraper username password [options] 
    username: User name to submit to server
    password: Password to submit to server
    form-url: Url for login form.  This is how login information is submitted and verified
    target-url: Url for final destination.  Url to retrieve bill information
    
bill_info_scraper_test.py
=========================
    Script that tests the functionality of the above script.  