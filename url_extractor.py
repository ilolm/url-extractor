#!/usr/bin/env python3

import requests
import re
import urllib.parse as urlparse
import optparse


target_links = []

def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-u", "--url", dest="target_url", help="Spesify a target url.")

    options = parser.parse_args()[0]

    if not options.target_url:
        parser.error("\033[91m[-] Please specify a target url. --help for more info.")

    return options

def extarct_links_from(target_url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content.decode('utf-8', errors="ignore"))

def crawl(url):
    global target_links
    href_links = extarct_links_from(url)

    for link in href_links:
        link = urlparse.urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if options.target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


options = get_options()
crawl(options.target_url)