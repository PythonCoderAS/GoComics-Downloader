#!/usr/bin/env python
# -*- coding: utf-8 -*-

# compatibility
from __future__ import absolute_import, print_function, unicode_literals

from .constants import (image_class, one_day)
from .downloader import download_file
from .exceptions import (DoubleInputException, NoInputException, IncompleteInputException, InvalidDate)

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import bs4
import datetime
import mainchecker

mainchecker.check_for_main()


def check_if_redirect(link):
    """
    :type link: str
    :param link: Link of website to check
    :return: True/False
    :rtype: bool
    """
    website = urllib2.urlopen(link)
    if website.url == link:
        return False
    else:
        return True


def datetime_parser(dt):
    """
    :rtype: list
    :param dt: datetime.datetime object
    :return: the year, month and date
    """
    return dt.strftime('%Y:%m:%d').split(':')


def get_comic_page(comic_name, year=None, month=None, day=None, dt=None):
    """
    :type dt: datetime.datetime
    :type day: int
    :type month: int
    :type year: int
    :type comic_name: str
    :param comic_name: name of the comic
    :param year: the year of the page of the comic, eg 2017
    :param month: the month of the page of the comic, eg 5
    :param day: the day of the page of the comic, eg 26
    :param dt: a datetime.datetime object
    :return: bs4.BeautifulSoup object
    :rtype: bs4.BeautifulSoup
    """
    if not year is None and not month is None and not day is None:
        ymd = True
    elif year is None and month is None and day is None:
        ymd = False
    else:
        raise exceptions.IncompleteInputException(year, month, day)
    if not dt is None and ymd:
        raise exceptions.DoubleInputException(year, month, day, dt)
    elif not dt is None:
        year, month, day = datetime_parser(dt)
    url = 'http://www.gocomics.com/{cn}/{y}/{m}/{d}'.format(cn=comic_name, y=year, m=month,
                                                            d=day)
    check_if_redirect(url)
    page = urllib2.urlopen(url)
    content = page.read()
    soup = bs4.BeautifulSoup(content, "lxml")
    assert isinstance(soup, bs4.BeautifulSoup)
    return soup


def process_image(soup):
    """
    
    :type soup: bs4.BeautifulSoup
    :param soup: the BeautifulSoup object 
    :return: string
    :rtype: str
    """
    findall = soup.find_all('picture', class_=image_class)
    entry = findall[0].img['src']
    assert isinstance(entry, str)
    return entry


def download_image(link, save_name=None):
    """

    :type save_name: str
    :type link: str
    :param link: the link of file to download
    :param save_name: the filename you want to save as.
    :return: filenane
    :rtype: str
    """
    return download_file(link, dest=save_name)


def get_picture(comic_name, year=None, month=None, day=None, dt=None, save_name=None):
    """
    :type save_name: str
    :type dt: datetime.datetime
    :type day: int
    :type month: int
    :type year: int
    :type comic_name: str
    :param comic_name: name of the comic
    :param year: the year of the page of the comic, eg 2017
    :param month: the month of the page of the comic, eg 5
    :param day: the day of the page of the comic, eg 26
    :param dt: a datetime.datetime object
    :param save_name: the filename you want to save as
    :return: None
    :rtype: None
    """
    soup = get_comic_page(comic_name, year=year, month=month, day=day, dt=dt)
    link = process_image(soup)
    download_image(link, save_name=save_name)


def save_structure(time_object):
    """
    :type time_object: datetime.datetime
    :param time_object: the datetime.datetime object
    :return: year-month-date
    :rtype: str
    """
    return time_object.strftime('%Y-%m-%d')


def download_all(comic_name, date=datetime.datetime.now()):
    """
    :type date: datetime.datetime
    :param date: the datetime.datetime object
    :type comic_name: str
    :param comic_name: the comic to download
    :return: Nothing
    :rtype: None
    """
    save_name = save_structure(date) + '.jpg'
    try:
        while True:
            try:
                get_picture(comic_name, dt=date, save_name=save_name)
            except ValueError:
                get_picture(comic_name, dt=date, save_name=save_name)
            date = date - one_day
            save_name = save_structure(date) + '.jpg'
    except InvalidDate:
        print('Complete.')
