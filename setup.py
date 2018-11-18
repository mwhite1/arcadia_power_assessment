from distutils.core import setup

setup(
    name='arcadia_power_assessment',
    version='0.0.3',
    author='Malcolm White',
    author_email='malcolm.m14@gmail.com',
    packages=['billinfoscraper', 'billinfoscraper.test'],
    scripts=['bin/get_bill_info.py'],
    url='http://pypi.python.org/pypi/arcadia_power_assessment/',
    license='LICENSE.txt',
    description='arcadia power assessment',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4==4.6.0",
        "mock==2.0.0",
        "requests==2.20",
        "urllib3==1.23"
    ],
)