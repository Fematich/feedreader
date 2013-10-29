#!/bin/sh

virtualenv venv
. venv/bin/activate

pip install feedparser
pip install BeautifulSoup
