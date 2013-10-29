#!/bin/sh

virtualenv venv
. venv/bin/activate

pip install feedparser
pip install requests
pip install BeautifulSoup
