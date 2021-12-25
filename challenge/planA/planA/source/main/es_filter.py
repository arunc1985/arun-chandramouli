'''
    This module contains all the required main APIs for processing and publications
'''
import os
from utils import ESOperator
from common_bases import ESDataBase
import json

class ESDataFilter(ESDataBase):
    '''
        This class deals with following tasks;
        1. Parse the ElasticSearch Database Index according to given query and return results
    '''
    def getRecordsFromIndex(self,es_index,query):
        '''
            Get Records from an Index and return
        '''
        return ESOperator.bulkReadJson(es_conn_object=self.esConnObj,es_index=es_index,query=query)

class Filters:

    @staticmethod
    def filter(esHost,esPort,esQuery):
        '''
            Parse Records & Upload to Elasticsearch Index(Bulk Upload)
        '''
        es_processor_ins_parser=ESDataFilter(esHost=esHost,esPort=esPort)
        es_processor_ins_parser.getEsConnection()
        es_processor_ins_parser.getRecordsFromIndex(es_index=esIndex,query=json.loads(esQuery))
        return True

if __name__ == "__main__":

    Filters.filter(os.environ['esHost'],os.environ['esPort'],os.environ['ESQUERY'])
    