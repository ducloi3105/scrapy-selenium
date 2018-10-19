# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from scrapy.loader import ItemLoader
from physio.items import PhysioItem

URI = "https://www.physiotherapy.asn.au/APAWCM/Controls/FindaPhysio.aspx"
POSTCODE = ['2000']
# POSTCODE = ['2000','2600','3000','4000','5000','6000','7000','8000']
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


def start_repo(postcode):
    driver = webdriver.Chrome()
    driver.get(URI)

    # search by postcode and radius
    time.sleep(1)
    el_postcode = driver.find_element_by_id(ID_POSTCODE)
    el_postcode.send_keys(postcode)

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
    start_urls = ["https://www.physiotherapy.asn.au"]
    postcode = ''

    def parse(self, response):
        print 'vaoday'
        for code in POSTCODE:
            self.postcode = code
            urls = start_repo(code)

            for url in urls:
                yield scrapy.Request(url, callback=self.get_details)

    def get_details(self, response):
        print 'vaoday      111111111111111'
        practitioner_name = ''
        practise_name = ''
        address = ''
        phone = ''
        fax = ''
        email = ''
        web_url = ''
        postcode_searched = self.postcode

        top_left = response.xpath('//*[@id="topLeft"]')
        td_bolded_once = top_left.xpath('.//table').xpath('.//td')
        bolded_once = td_bolded_once[0].xpath('text()').extract_first()
        if bolded_once == "Practitioner Name":
            practitioner_name = td_bolded_once[1].xpath('text()').extract_first()

        table_contact = top_left.xpath('.//*[@id="ctl00_TemplateBody_WebPartManager1_gwpste_container_ContactDetails_ciContactDetails_ContactDetailsControl1_contactDetailsList_gridCD"]')
        td_bolded_two = table_contact[0].xpath('.//table').xpath('.//td')
        get_name = get_add = get_phone = get_fax = get_email = get_web = False
        for td in td_bolded_two:
            txt = td.xpath('text()').extract_first()
            if txt == "Practice Name":
                get_add = get_phone = get_fax = get_email = get_web = False
                get_name = True
                continue
            if txt == "Address":
                get_name = get_phone = get_fax = get_email = get_web = False
                get_add = True
                continue
            if txt == "Phone":
                get_name = get_add = get_fax = get_email = get_web = False
                get_phone = True
                continue
            if txt == "Fax":
                get_name = get_add = get_phone = get_email = get_web = False
                get_fax = True
                continue
            if txt == "Email":
                get_name = get_add = get_phone = get_fax = get_web = False
                get_email = True
                continue
            if txt == "Web":
                get_name = get_add = get_phone = get_fax = get_email = False
                get_web = True
                continue
            if get_name:
                practise_name = txt
            if get_add:
                address = txt
            if get_phone:
                phone = txt
            if get_fax:
                fax = txt
            if get_email:
                email = td.xpath('.//a/@href').extract_first()
            if get_web:
                web_url = td.xpath('.//a/@href').extract_first()
                break

        profile_url = response.request.url
        l = ItemLoader(item=PhysioItem(), response=response)
        l.add_value('practitioner_name', practitioner_name)
        l.add_value('practise_name', practise_name)
        l.add_value('address', address)
        l.add_value('phone', phone)
        l.add_value('fax', fax)
        l.add_value('email', email.replace('mailto: ', '', 1))
        l.add_value('web_url', web_url)
        l.add_value('profile_url', profile_url)
        # l.add_value('postcode_searched', postcode_searched)
        return l.load_item()