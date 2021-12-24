'''
    This module contains all the required main APIs for processing and publications
'''
import os
from utils import ESOperator
from common_bases import ESDataBase

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

if __name__ == "__main__":
    '''
        unset bmiUsersJsonFile
        unset bmiCatJsonFile
        unset esHost
        unset esPort
        unset esIndex
        unset bmiCAT
        export bmiCatJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/bmi_cat.json
        export bmiUsersJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/sample2.json
        export esHost=localhost
        export esPort=9200
        export esIndex='bmi'
        export bmiCAT="OverWeight"
    '''
    bmiUsersJsonFile=os.environ['bmiUsersJsonFile']
    bmiCatJsonFile=os.environ['bmiCatJsonFile']
    esHost=os.environ['esHost']    
    esPort=os.environ['esPort']    
    esIndex=os.environ['esIndex'] 

    es_processor_ins_parser=ESDataFilter(esHost='localhost',esPort='9200')
    es_processor_ins_parser.getEsConnection()
    es_processor_ins_parser.getRecordsFromIndex(es_index='bmi',query={'bmi.cat':'ModerateObese'})
