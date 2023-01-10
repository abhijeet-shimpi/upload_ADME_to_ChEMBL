from tdc.single_pred import ADME
import utils
from sql_connect import Pgsql
import model
import pandas as pd
from datetime import datetime

class ETL:

    def __init__(self):
        self.data_df = pd.DataFrame()

    def extract(self):
        name = 'BBB_Martins'
        adme_type = 'Distribution'
        data = ADME(name=name)
        # split = data.get_split()
        df = data.get_data(format='df')
        self.data_df = self.data_df.append(df)
        self.data_df['adme_type'] = adme_type
        self.data_df['drug_type'] = name
        self.data_df['date_inserted'] = datetime.now()
        print(self.data_df)

    def transform(self):
        pass

    def validation(self):
        pass

    def load(self):
        pg_connection_detail = utils.config('pg_db')
        config = dict(pg_connection_detail= pg_connection_detail,
                      model = model.ADME)
        conn = Pgsql(config)
        conn.insert_pd_df(self.data_df)
        print('Data inserted successfull!')


if __name__  == "__main__":
    ETL().extract()
    ETL().load()
