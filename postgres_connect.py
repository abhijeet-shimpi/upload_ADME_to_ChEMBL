'''This module is for performing database operations'''

import psycopg2
import psycopg2.extras as extras

# Defining datatypes in postgres db
DEFAULT_DATATYPES = dict(
    str = 'text',
    int = 'int',
    datetime = 'timestamp',
    bool = 'boolean',
    float = 'float'

)

class Pgsql:
    def __init__(self, config: dict()):
        self.connection_details = config.get('pg_connection_detail')
        self.cnn = self.connection()
        self.cursor = self.cnn.cursor()
        self.adme_type = config.get('adme_type')
        self.model = config.get('model')
        self.table_name = self.model.table_name.get(self.adme_type)
        self.col_types: dict() = None
        self.text_column = None
        self.col_names = self.model_columns()
        self.create_schema_if_not_exist()
        self.create_table_if_not_exist()

    def connection(self):
        # connect to postgres instance of Chembl and return psycopg connection object
        self.cnn = psycopg2.connect(**self.connection_details)
        print('Connected to PostgreSQL')
        return self.cnn

    def close_cnn(self):
        self.cnn.close()

    def create_schema_if_not_exist(self):
        # create schema for first instance
        qry = f"""CREATE SCHEMA IF NOT EXISTS {self.model.schema};"""
        self.cursor.execute(qry)

    def create_table_if_not_exist(self):
        # create table for first instance
        qry = f"""
                CREATE TABLE IF NOT EXISTS {self.model.schema}.{self.table_name}
                ({self.text_column})
                """
        self.cursor.execute(qry)

    def model_columns(self):
        #resolving dataclass fields into different formats
        self.col_names = list(self.model.__dataclass_fields__.keys())

        self.col_types = dict()
        text_cols = list()
        for col in self.col_names:
            fields_type = self.model.__dataclass_fields__[col].type.__name__
            fields_type = DEFAULT_DATATYPES[fields_type]
            self.col_types[col] = fields_type
            text_cols.append(f'{col} {fields_type}')
        self.text_column = ','.join(text_cols)
        return self.col_names

    def execute_query(self, qry, parameter=[]):
        self.cursor.execute(qry, parameter)
        self.commit()

    def bulk_execute(self, qry, values):
        # Function executes the insert query on to Chembl db
        extras.execute_values(self.cursor, qry, values)
        self.commit()

    def insert_data(self, data):
        #convert split dataframe rows into list of tuples before bulk insertion process
        #build insert query and passing to bulk execute function

        # tuples = [tuple(row) for index, row in data.iterrows()]
        values = list(data.itertuples(index=False, name=None))
        qry = f'''INSERT INTO {self.model.schema}.{self.table_name} ({','.join(self.col_names)}) VALUES %s'''
        self.bulk_execute(qry, values)
        self.close_cnn()
        print(f'Data inserted in {self.model.schema}.{self.table_name} table successfull!')

    def delete_rows(self):
        pass

    def commit(self):
        self.cnn.commit()

    def read_from_cursor(self):
        #to read output of a query from Chembl db
        cols = [col_def[0] for col_def in self.cursor.description]
        rows = self.cursor.fetchall()
        return cols, rows



