# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
import time

URI = "https://www.physiotherapy.asn.au/APAWCM/Controls/FindaPhysio.aspx"
POSTCODE = '2000'
RADIUS = '1'
ID_POSTCODE = 'ctl00_TemplateBody_WebPartManager1_gwpste_container_FindaPhysioIPart_ciFindaPhysioIPart_FP1_fpSearch_txtPostCode'
ID_RADIUS = 'ctl00_TemplateBody_WebPartManager1_gwpste_container_FindaPhysioIPart_ciFindaPhysioIPart_FP1_fpSearch_txtRadius'
BTN_SUBMIT = '.FPSearchButton input[type="submit"].TextButtonAPA'
BTN_NEXT = '#gridPagerTop .ICPagerButtonRight'


def next_page(driver):
    btn_next = driver.find_element_by_css_selector('#gridPagerTop .ICPagerButtonRight')
    btn_next.click()


def get_links(driver):
    # get link
    links = []
    i = 2
    while True:
        try:
            xpath = '//table//tr[{i}]/td[2]/a'.format(i=i)
            links.append(driver.find_element_by_xpath(xpath).get_attribute('href'))
        except:
            break
        i += 1
    return links


def start_repo():
    driver = webdriver.Firefox()
    driver.get(URI)

    # search by postcode and radius
    time.sleep(1)
    el_postcode = driver.find_element_by_id(ID_POSTCODE)
    el_postcode.send_keys(POSTCODE)

    el_radius = driver.find_element_by_id(ID_RADIUS)
    el_radius.send_keys(RADIUS)
    time.sleep(1)

    el_submit = driver.find_element_by_css_selector(BTN_SUBMIT)
    el_submit.click()

    # get link in page here
    links = get_links(driver)
    # next_page
    while True:
        try:
            btn_next = driver.find_element_by_css_selector(BTN_NEXT)
            if btn_next.get_attribute("disabled") == 'true':
                break
            btn_next.click()
            links += get_links(driver)
        except:
            break
    print len(links)
    driver.close()

    return links


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    # allowed_domains = start_repo()
    start_urls = ['https://www.physiotherapy.asn.au/APAWCM/Global_Navigation/FP_ContactDetails/APAWCM/Controls/ContactDetails.aspx?id=52312']

    def parse(self, response):
        print 11111111111111111111111111111
        print response
