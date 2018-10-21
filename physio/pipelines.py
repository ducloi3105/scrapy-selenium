# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PhysioPipeline(object):
    def process_item(self, item, spider):
        if item.get('phone', ''):
            item['phone'] = '\n' + item['phone'][0]
        if item.get('fax', ''):
            item['fax'] = '\n' + item['fax'][0]
        return item
