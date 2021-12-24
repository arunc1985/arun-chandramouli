'''
    This module contains all the required main APIs for processing and publications
'''
import os
from utils import JsonOperator,ESOperator,BMICalculator
from common_bases import ESDataBase

class BMIProcessor:
    '''
        This class deals with following tasks;
            1. Get JSON input files from Users
            2. Load JSON records into memory
            3. Find BMI Values - BMI, Category, HealthRisk
            4. Update the existing records with new columns
    '''

    def __init__(self,bmiUsersJsonFile,bmiCatJsonFile):
        '''
            Initialize the files attributes
            :param bmiUsersJsonFileContents: File that contains user-data such as Gender, Height, Weight
            :param bmiCatJsonFileContents: 
                File that contains category,healthRisk such as UnderWeight,OverWeight etc..Contains Ranges of weighs
        '''
        self.bmiUsersJsonFile=bmiUsersJsonFile
        self.bmiCatJsonFile=bmiCatJsonFile

    def getFileContents(self):
        '''
            Using Utils read the *JSON* files and load
        '''
        self.bmiUsersJsonFileContents=JsonOperator.readJson(json_file=self.bmiUsersJsonFile)
        self.bmiCatJsonFileContents=JsonOperator.readJson(json_file=self.bmiCatJsonFile)

    def getBMIValues(self):
        '''
            Given the JSON set of records from step -getFileContents,
            find out the BMI Index, Category, HealthRisk etc and yield the records.
        '''
        return BMICalculator.calculateBmi(self.bmiUsersJsonFileContents,self.bmiCatJsonFileContents)

'''
    Note to Reader :: The Reason for having base class ESDataBase is to;
        1. Write all Common Reusable code as part ot base class
        2. Reuse the code in the Uploader and Parser classes of ElasticSearch
        3. Easr of Development Extension and Maintenance
'''
class ESDataUploader(ESDataBase):
    '''
        This class deals with following tasks;
        1. Upload records in BULK to ElasticSearch Database
    '''
    def setRecordsBulk(self,es_index,records):
        '''
            Delete index & Push records in BULK into ElasticSearch
        '''
        #ESOperator.deleteIndex(self.esConnObj,es_index=es_index)
        return ESOperator.bulkUploadJson(es_conn_object=self.esConnObj,es_index=es_index,json_file_contents=records)

class ESDataParser(ESDataBase):
    '''
        This class deals with following tasks;
        1. Parse the ElasticSearch Database Index according to given query and return results
    '''
    def getRecordsFromIndex(self,es_index,query):
        '''
            Get Records from an Index and return
        '''
        return ESOperator.bulkReadJson(es_conn_object=self.esConnObj,es_index=es_index,query=query)

class Uploader:

    @staticmethod
    def upload(bmiUsersJsonFile,bmiCatJsonFile,esHost,esPort,esIndex):
        '''
            Parse Records & Upload to Elasticsearch Index(Bulk Upload)
        '''
        procesor_ins=BMIProcessor(bmiUsersJsonFile,bmiCatJsonFile)
        procesor_ins.getFileContents()
        procesor_ins.getBMIValues()
        es_processor_ins=ESDataUploader(esHost='localhost',esPort='9200')     
        es_processor_ins.getEsConnection()
        es_processor_ins.setRecordsBulk(es_index='bmi',records=list(procesor_ins.getBMIValues()))
        return True

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
    # Upload Records
    Uploader.upload(bmiUsersJsonFile,bmiCatJsonFile,esHost,esPort,esIndex)