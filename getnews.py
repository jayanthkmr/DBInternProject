import sys, urllib2, urllib
from newssentihack import *

try: import simplejson as json
except ImportError: import json

PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
FINANCE_TABLES = {'quotes': 'yahoo.finance.quotes',
                 'options': 'yahoo.finance.options',
                 'quoteslist': 'yahoo.finance.quoteslist',
                 'sectors': 'yahoo.finance.sectors',
                 'industry': 'yahoo.finance.industry'}

def get_proxy_opener(proxyurl, proxyuser, proxypass, proxyscheme="http"):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, proxyurl, proxyuser, proxypass)

    proxy_handler = urllib2.ProxyHandler({proxyscheme: proxyurl})
    proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)

    return urllib2.build_opener(proxy_handler, proxy_auth_handler)

#conn = get_proxy_opener("netmon.iitb.ac.in:80","jayanth","myrollno.is100050041")

class YQLQuery(object):

	def __init__(self):
		self.connection = get_proxy_opener("netmon.iitb.ac.in:80","jayanth","myrollno.is100050041")


	def execute(self, yql):
		queryString = urllib.urlencode({'q': yql, 'format': 'json', 'env': DATATABLES_URL})
		fetchQuery = self.connection.open(PUBLIC_API_URL + '?' + queryString)
		return json.loads(fetchQuery.read())

class QueryError(Exception):

	def __init__(self, value):
		self.value = value



	def __str__(self):
		return repr(self.value)

class StockRetriever(YQLQuery):
    """A wrapper for the Yahoo! Finance YQL api."""
                     
    def __init__(self):
        self.sentiment = Sentiment()
        super(StockRetriever, self).__init__()



    def __format_symbol_list(self, symbolList):
            return ",".join(["\""+stock+"\"" for stock in symbolList])
	


    def __is_valid_response(self, response, field):
        return 'query' in response and 'results' in response['query'] \
            and field in response['query']['results']
    


    def __validate_response(self, response, tagToCheck):
        if self.__is_valid_response(response, tagToCheck):
            quoteInfo = response['query']['results'][tagToCheck]
        else:
            if 'error' in response:
                raise QueryError('YQL query failed with error: "%s".' 
                    % response['error']['description'])
            else:
                raise QueryError('YQL response malformed.')
        return quoteInfo


        
    def get_current_info(self, symbolList, columnsToRetrieve='*'):
        """Retrieves the latest data (15 minute delay) for the 
        provided symbols."""
        
        columns = ','.join(columnsToRetrieve)
        symbols = self.__format_symbol_list(symbolList)

        yql = 'select %s from %s where symbol in (%s)' \
              %(columns, FINANCE_TABLES['quotes'], symbols)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')


    
    def get_historical_info(self, symbol):
        """Retrieves historical stock data for the provided symbol.
        Historical data includes date, open, close, high, low, volume,
        and adjusted close."""
        
        yql = 'select * from csv where url=\'%s\'' \
              ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
               % (HISTORICAL_URL + symbol)
        results = super(StockRetriever, self).execute(yql)
        # delete first row which contains column names
        del results['query']['results']['row'][0]
        return results['query']['results']['row']
        


    
    def get_news_feed(self, symbol):
        """Retrieves the rss feed for the provided symbol."""
        
        feedUrl = RSS_URL + symbol
        yql = 'select title, link, description, pubDate from rss where url=\'%s\'' % feedUrl
        #print yql
        response = super(StockRetriever, self).execute(yql)
        #print response
        if response['query']['results']['item'][0]['title'].find('not found') > 0:
            raise QueryError('Feed for %s does not exist.' % symbol)
        else:
            r = response['query']['results']['item']
            for i in r:
                if i['title']==None:
                    i['titlesentiment'] = [0,1]
                else:
                    i['titlesentiment']=self.sentiment.findsentiment(i['title'])
                if i['description'] ==None:
                    i['descsentiment'] = [0,1]
                else:
                    i['descsentiment']=self.sentiment.findsentiment(i['description'])

            return r
        
    def get_options_info(self, symbol, expiration='', columnsToRetrieve ='*'):
        """Retrieves options data for the provided symbol."""
        
        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'%s\'' \
              % (columns, FINANCE_TABLES['options'], symbol)
        
        if expiration != '':
            yql += " and expiration='%s'" %(expiration)
        
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'optionsChain')


        
    def get_index_summary(self, index, columnsToRetrieve='*'):
        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'@%s\'' \
              % (columns, FINANCE_TABLES['quoteslist'], index)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')


    
    def get_industry_ids(self):
        """retrieves all industry names and ids."""
        
        yql = 'select * from %s' % FINANCE_TABLES['sectors']
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'sector')


    
    def get_industry_index(self, id):
        """retrieves all symbols that belong to an industry."""
        
        yql = 'select * from %s where id =\'%s\'' \
              % (FINANCE_TABLES['industry'], id)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'industry')
        
