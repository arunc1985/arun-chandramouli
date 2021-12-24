'''
	This module contains all the base classes
'''

from utils import ESOperator

class ESDataBase:
    '''
        This class deals with following tasks;
        1. Get Elasticsearch Connection Params
        2. Return the Connection object
    '''
    def __init__(self,**esConnParams):
        '''
            Initialize the ElasticSearch attributes
            :param esConnParams: ElasticSearch Hostname and PORT
        '''
        self.esConnParams=esConnParams

    def getEsConnection(self):
        '''
            Return an ES connection
        '''
        self.esConnObj=ESOperator.esConnection(self.esConnParams['esHost'],self.esConnParams['esPort'])
        return self.esConnObj