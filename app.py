from tdc.single_pred import ADME
import utils
from sql_connect import Pgsql
import model
import pandas as pd
from datetime import datetime

class ETL:

    def __init__(self, name, adme_type):
        self.data_df = pd.DataFrame()
        self.name = name
        self.adme_type = adme_type
        self.split = dict()
        self.df = pd.DataFrame()

    def extract(self):

        print(f'Data extraction started for {self.adme_type}:{self.name}')
        data = ADME(name=self.name)
        self.split = data.get_split()
        print(self.split)
        # df = data.get_data(format='df')
        # self.data_df = self.data_df.append(df)


    def transform(self):
        print(f'Data tranforming for {self.adme_type}:{self.name}')

        for key in self.split:
            dataset = pd.DataFrame(self.split[key])
            dataset['dataset_type'] = key
            self.data_df = self.data_df.append(dataset)

        self.data_df['adme_type'] = self.adme_type
        self.data_df['drug_type'] = self.name
        self.data_df['date_inserted'] = str(datetime.now()).split('.')[0]
        self.data_df['Drug_ID'] = self.data_df['Drug_ID'].str.replace('\'', '\'\'')

    def validation(self):
        pass

    def load(self):
        pg_connection_detail = utils.config('pg_db')
        config = dict(pg_connection_detail= pg_connection_detail,
                      model = model.ADME,
                      adme_type = self.adme_type)
        conn = Pgsql(config)
        conn.insert_data(self.data_df)



if __name__  == "__main__":
    adme = dict(
        Distribution = ['BBB_Martins'],
        Absorption = ['Caco2_Wang']
    )
    for adme_type in adme:
        for name in adme[adme_type]:
            etl = ETL(name, adme_type)
            etl.extract()
            etl.transform()
            etl.load()
