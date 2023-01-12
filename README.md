# upload_ADME_to_ChEMBL

This repository is to merge ADME data from TDC to ChEMBL DB.

App for ETL operations on TDC ADME data. ETL operations include 
* extracting ADME data from TDC, 
* splitting data into test, train and validation sets.
* creating pandas dataframe for the split data and adding few more meta data.
* Loading the data to the ChEMBL database.


## Pre-requisites:

1. Python 3.9
2. ChEMBL Database

3. Configuration parameters: Add database details in the config.ini file
[pg_db]
host = 
database =  
user = 
port = 
password = 

None: if the db is hosted on cloud, 
please provide the server details under the host.

## Create ChEMBL database instance
On local machine:
1. Install postgreSQL using command: 
    ```shell
    sudo apt install postgresql
    ```
   
2. open postgres editor using command: 
    ```shell
    sudo su - postgres
    ```
   
3. create user using command: 
    ```shell
    create user adminuser with superuser password 'adminuser'
    ```
   
4. create database using command: 
    ```shell 
    create database chembl;
    ```


## Run the app:

Install all the necessary python libraries using below command:

```sh
python pip install -r requirements.txt
```
Run the app using below command:

```sh
python app.py
```

This will extract all the ADME data and perform transformations. 
It will also create schema and required tables in the db.
It will then load ADME data into appropriate tables.


## SQL to access data

below are few examples of sqls to access ADME data from ChEMBL DB after migrating the data

* To access perticular type of Absorption data:
```sql 
SELECT * 
FROM amdb.absorption 
WHERE drug_type = 'Caco2_Wang'
```
* To access only training data: 
```sql 
SELECT * 
FROM amdb.absorption 
WHERE drug_type = 'Caco2_Wang' 
and dataset_type = 'train'
```


## Reasons and assumptions
* ML teams required data segregated into train, valid, test data. 
* Used split data rather than raw data to identify type of datasets
* build four separate tables for each classification of ADME types for easy access.

## Preparation & Execution
--prep time : 1-2 hours
--execution : 2-3 hours
* Analysed TDC data and its functions(pytdc).
* Explored different libraries - psycopg2, SQLAlchemy
* Explored Datagrid IDE for postgres
