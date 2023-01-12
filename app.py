from tdc.single_pred import ADME
import utils
import metadata
from postgres_connect import Pgsql
import model
import pandas as pd
from datetime import datetime

class ETL:
    '''
    main class to perform ETL operation.
    '''
    def __init__(self, name, adme_type):
        '''
        init function to initialise clase parameters
        :arg
            :param name: drug type
            :param adme_type: ADME type (Abosoption, Distribution, Metabolism and Excretion
        '''
        self.data_df = pd.DataFrame()
        self.name = name
        self.adme_type = adme_type
        self.split = dict()


    def extract(self):
        '''
        function to extracting ADME data from TDC source
        :return:nothing
        '''
        print(f'Data extraction started for {self.adme_type}:{self.name}')
        data = ADME(name=self.name)
        self.split = data.get_split()


    def transform(self):
        '''
        function to perform minor transformations on ADME data
        Transformation: merging split data
                       Adding ADME_type, Drug_type and date inserted in dataset
                       Casting Drug_ID to str format to maintain data consistency
        '''
        print(f'Data tranforming for {self.adme_type}:{self.name}')

        # iterating over split data keys (train, test, valid)
        # storing/appending data in separate dataframe - data_df
        for key in self.split:
            dataset = pd.DataFrame(self.split[key])
            dataset['dataset_type'] = key
            self.data_df = self.data_df.append(dataset)

        self.data_df['adme_type'] = self.adme_type
        self.data_df['drug_type'] = self.name
        self.data_df['date_inserted'] = str(datetime.now()).split('.')[0]

        # Drug_id field contains different datatypes in all ADME types
        # Transforming Drug_id column to str for consistency
        # Drug_id also contains apostrophes, converting this into double apostrophes
        self.data_df['Drug_ID'] = self.data_df['Drug_ID'].astype('string').str.replace('\'', '\'\'')

    def validation(self):
        pass

    def load(self):
        '''
        Loading dataset in Chembl database
        :return: Nothing
        '''

        # get config parameters from config.ini in dict format
        pg_connection_detail = utils.config('pg_db')
        config = dict(pg_connection_detail= pg_connection_detail,
                      model = model.ADME,
                      adme_type = self.adme_type)
        # connect to postgres db
        conn = Pgsql(config)
        conn.insert_data(self.data_df)



if __name__  == "__main__":

    '''
    Functions gets ADME list from metadata.py file
    Iterate on the above list and perform ETL operations    
    '''

    for adme_type in metadata.adme_dict:
        for name in metadata.adme_dict[adme_type]:
            etl = ETL(name, adme_type)
            etl.extract()
            etl.transform()
            etl.load()
