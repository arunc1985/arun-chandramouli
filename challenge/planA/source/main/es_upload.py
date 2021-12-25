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
        ESOperator.deleteIndex(self.esConnObj,es_index=es_index)
        return ESOperator.bulkUploadJson(es_conn_object=self.esConnObj,es_index=es_index,json_file_contents=records)

class Uploader:

    @staticmethod
    def upload(bmiUsersJsonFile,bmiCatJsonFile,esHost,esPort,esIndex):
        '''
            Parse Records & Upload to Elasticsearch Index(Bulk Upload)
        '''
        procesor_ins=BMIProcessor(bmiUsersJsonFile,bmiCatJsonFile)
        procesor_ins.getFileContents()
        procesor_ins.getBMIValues()
        es_processor_ins=ESDataUploader(esHost=esHost,esPort=esPort)
        es_processor_ins.getEsConnection()
        es_processor_ins.setRecordsBulk(es_index=esIndex,records=list(procesor_ins.getBMIValues()))
        return "Records Uploaded successfully. Login to Kibana http://<<IP>>:<<5601>> for details."

if __name__ == "__main__":
    # Upload Records
    Uploader.upload(os.environ['bmiUsersJsonFile'],os.environ['bmiCatJsonFile'],os.environ['esHost'],os.environ['esPort'],os.environ['esIndex'])