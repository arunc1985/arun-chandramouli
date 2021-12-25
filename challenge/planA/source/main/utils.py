'''
    This module contains all the Python Utils for re-usable code.
'''
import json
from elasticsearch import Elasticsearch, helpers

class JsonOperator:

    @staticmethod
    def readJson(json_file):
        '''
            Read the Json file and return the contents
            :param json_file: Fullpath of the json file
            :return: Json file contents as-is
            :exception: Raise Error
        '''
        try:
            with open(json_file,'r') as reader:
                return json.load(reader)
        except Exception as error:
            raise Exception("Unable to read Json file - {} ".format(json_file))

class ESOperator:

    @staticmethod
    def esConnection(es_host,es_port):
        ''' 
            Create a new Elasticsearch connection object & return
            :param: es_host: Host VM IP where Elasticsearch is deployed
            :param: es_port: Port on which Elasticsearch is deployed
            :return: Elasticsearch connection object
            :exception: Raise Error
        '''
        try:
            es_conn_object = Elasticsearch([{'host': es_host, 'port': es_port}])
            return es_conn_object
        except Exception as error:
            raise Exception("Unable to create an Elasticsearch connection object - {} {} ".format(es_host,es_port))

    @staticmethod
    def bulkUploadJson(es_conn_object,es_index,json_file_contents):
        '''
            Do a bulk upload of JSON file contents into Elasticsearch
            :param: es_conn_object: Elasticsearch connection object
            :param: es_index: Elasticsearch index into which records are to be pushed
            :param: json_file_contents: Contents of User's json file
            :return: True
            :exception: Raise Error
        '''
        def _yield_records():
            # A simple function to yield records for ES format and fsater processing
            for record in json_file_contents:
                yield {
                    "_index": es_index,
                    "bmi": record,
                    }
        try:            
            return helpers.bulk(es_conn_object,_yield_records())
        except Exception as error:
            raise Exception("Unable to do bulk upload to index - {} ".format(es_index))

    @staticmethod
    def bulkReadJson(es_conn_object,es_index,query):
        '''
            Return all records from a given index
            :param: es_conn_object: Elasticsearch connection object
            :param: es_index: Elasticsearch index into which records are to be pushed
            :return: Elasticsearch Index records
            :exception: Raise Error

            Sample Query:
            doc = {
                'query': {
                    'match' : {'bmi.healthRisk':'Medium risk'}
               }
            }           

            doc = {
                'query': {
                    'match' : {'bmi.Gender':'Male'}
               }
            }           

            doc = {
                'query': {
                    'match' : {'bmi.cat':'ModerateObese'}
               }
            }           

            doc = {
                'query': {
                    'match_all' : {}
               }
            }
        '''
        try:
            return es_conn_object.search(index=es_index, body=query,doc_type='_doc')
        except Exception as error:
            raise error

    @staticmethod
    def deleteIndex(es_conn_object,es_index):
        '''
            Delete an existing index
            :param: es_conn_object: Elasticsearch connection object
            :param: es_index: Elasticsearch index into which records are to be pushed
            :return: True
            :exception: Raise Error
        '''
        try:
            es_conn_object.indices.delete(index=es_index, ignore=[400,404])
            return True
        except Exception as error:
            raise Exception("Unable to delete index - {} ".format(es_index))

class BMICalculator:

    @staticmethod
    def calculateBmi(bmiUsersJsonFileContents,bmiCatJsonFileContents):
        '''
            Given height and weight, calculate and return BMI
            Formula 1 - BMI
            BMI(kg/m2) = mass(kg) / height(m)2
            Sample Record:
                {"Gender": "Male", "HeightCm": 161, "WeightKg": 85 }
            :param bmiUsersJsonFileContents: Contens of User's json with height,weight etc...
            :param bmiCatJsonFileContents: Contents of the BMI Category Table
            :return: Updated JSON with BMI Index, Category
            :exception: Continue with default
        '''

        # Function to Calculate the BMI Category and HealthRisk
        # Note to Reader : The Reason for using Inner function is to avoid *External FAT Function Calls*
        def calc_table(bmi):
            try:
                for cats in bmiCatJsonFileContents:
                    if bmi > cats['low'] and bmi < cats['high']:
                        return {'cat':cats['cat'],'healthRisk':cats['healthRisk']}
            except Exception as error:
                print("error :: ",error)
                return {}

        def process_recs():
            for each_record in bmiUsersJsonFileContents:
                try:
                    # Calculate BMI and yield millions of Records
                    each_record['bmi']=round(each_record['WeightKg']/(each_record['HeightCm']/100)**2,2)
                    result_calc_table=calc_table(each_record['bmi'])
                    each_record['cat'],each_record['healthRisk']=result_calc_table['cat'],result_calc_table['healthRisk']
                    yield each_record
                except Exception as error:
                    # On exception with any record, continue .. ## TODO - logStash ##
                    print("error :: ",error)
                    continue
        return process_recs()