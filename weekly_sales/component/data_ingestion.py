from threading import local
from weekly_sales.entity.config_entity import DataIngestionConfig
import sys,os
from weekly_sales.exception import CustomException
from weekly_sales.logger import logging
from weekly_sales.entity.artifact_entity import DataIngestionArtifact
import tarfile
import numpy as np
import urllib.request

import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from weekly_sales.util.util import read_write_file
import shutil


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise Exception(e)
    

   

    def transfer_data(self):
        
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)
            local_file = self.data_ingestion_config.local_file
            shutil.copy(local_file, raw_data_dir)
            return local_file
        except Exception as e:
            raise Exception(e)
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            sales_file_path = os.path.join(raw_data_dir,file_name)


            logging.info(f"Reading csv file: [{sales_file_path}]")
            sales_data_frame = pd.read_csv(sales_file_path)

            sales_data_frame["income_cat"] = pd.cut(
                sales_data_frame["Weekly_Sales"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(sales_data_frame, sales_data_frame["income_cat"]):
                strat_train_set = sales_data_frame.loc[train_index].drop(["income_cat","Store","Date"],axis=1)
                strat_test_set = sales_data_frame.loc[test_index].drop(["income_cat","Store","Date"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise Exception(e) 

    def initiate_data_ingestion_from_local(self):
        try:
            self.transfer_data()
            self.split_data_as_train_test()

        except Exception as e:
            raise Exception(e)
    
    


    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
