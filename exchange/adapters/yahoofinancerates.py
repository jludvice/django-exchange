# -*- coding: utf-8 -*-
from decimal import Decimal
import json

__author__ = 'josef'

import csv
import urllib2
import logging

from exchange.adapters import BaseAdapter
from exchange.iso_4217 import code_list

logger = logging.getLogger(__name__)

YAHOO_FINANCE_URL = 'http://download.finance.yahoo.com/d/quotes.csv'
YAHOO_FORMAT = 'f=sl1&e=.csv'

YAHOO_CURRENCIES_LIST_URL = 'http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'


class YahooFinanceRatesAdapter(BaseAdapter):
    """
    this is adapter to populate currency and exchange rates models using yahoo finance
    to use this adapter set this into settings.py
    EXCHANGE_ADAPTER_CLASS='exchange.adapters.yahoofinancerates.YahooFinanceRatesAdapter'
    """

    def __init__(self):
        print "yahoo financer"
        super(YahooFinanceRatesAdapter, self).__init__()

    def yahoo_rate_codes(self, base):
        return ["s=%s%s=X" % (base, code) for code in code_list]

    def get_currencies(self):

        # this should be urllib response
        # content = open('quote.json', 'r')

        json_raw = urllib2.urlopen(YAHOO_CURRENCIES_LIST_URL)
        content = json.load(json_raw)

        count = content.get('list').get('meta').get('count')
        logger.info('Yahoo supports %s currencies' % count)

        resources_list = content.get('list').get('resources')

        curr = []
        for resource in resources_list:
            fields = resource.get('resource').get('fields')
            rate = Decimal(fields.get('price', '0.00'))
            if rate != 0:
                code = fields.get('symbol')[:3]
                print "%s: %s" % (code, rate)
                curr.append((code, code))

        return curr


    def get_exchangerates(self, base):
        rates = '&'.join(self.yahoo_rate_codes(base))
        url = "%(url)s?%(rates)s&%(format)s" % dict(url=YAHOO_FINANCE_URL, rates=rates, format=YAHOO_FORMAT)

        csv_content = urllib2.urlopen(url)

        result = []
        for row in csv.reader(csv_content):

            yahoo_rate_code = row[0]
            if len(yahoo_rate_code) != 8:
                raise ValueError("incorrect rate format from yahoo: %s" % yahoo_rate_code)

            rate = Decimal(row[1])

            if rate:
                logger.debug("Fetched rate: %s / %s : %s" % (base, yahoo_rate_code[3:6], rate))
                result.append((yahoo_rate_code[3:6], rate))
            else:
                logger.info("Skipping rate: %s / %s : %s" % (base, yahoo_rate_code[3:6], rate))

            logger.debug("result length for %s: %s" % (base, len(result)))

        return result


