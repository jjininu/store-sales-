import os
import sys

from housing.exception import HousingException
from housing.util.util import load_object

import pandas as pd


class HousingData:

    def __init__(self,
                 Store : int64,
                 Date : object,
                 Weekly_Sales : float64,
                 Holiday_Flag : int64,
                 Temperature : float64,
                 Fuel_Price : float64,
                 CPI : float64,
                 Unemployment: float64,
                 ):
        try:
            
            self.Store = Store,
            self.Date = Date,
            self.Weekly_Sales = Weekly_Sales,
            self.Holiday_Flag = Holiday_Flag,
            self.Temperature = Temperature,
            self.Fuel_Price = Fuel_Price,
            self.CPI = CPI,
            self.Unemployment = Unemployment 




            
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_sales_input_data_frame(self)
        try:
            sales_input_dict = self.get_sales_data_as_dict()
            return pd.DataFrame(sales_input_dict)
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_sales_data_as_dict(self):
        try:
            input_data = {
               "Store" : [self.Store],
                "Dates" : [self.Date] ,
                "Weekly_Sales" : [self.Weekly_Sales],
                "Holiday_Flag" : [self.Holiday_Flag],
                "Temperature" : [self.Temperature],
                "Fuel_Price" : [self.Fuel_Price],
                "CPI" : [self.CPI],
                "Unemployment" : [self.Unemployment]
                }
            return input_data
        except Exception as e:
            raise CustomException(e, sys)


class salesPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise CustomException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise CustomException(e, sys) from e