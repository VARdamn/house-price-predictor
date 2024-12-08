import joblib
import numpy as np
import pandas as pd

from config import config


class Predictor:

    def __init__(self, data):
        self.data = data

    def deserialize_pipeline(self):
        return joblib.load(config.PIPELINE_FILE)

    # Функция предобработки полученных данных
    def preprocess_data(self):
        cols_names = [
            'Этаж',
            'Кол-во этажей',
            'Кол-во комнат',
            'Наличие мебели',
            'Округ',
            'Ближайшее метро, мин.',
            'Продажа от агента',
            'Парковка',
            'Последний этаж',
            'Первый этаж',
            'Площадь_log',
            'Жилая_площадь_log',
            'Площадь_кухни_log',
            'Наличие балкона',
            'Кол-во лифтов',
            'Наличие грузового лифта',
        ]
        if self.data['floor'] == self.data['floors_count']:
            last_floor = 1
        else:
            last_floor = 0
        if self.data['floor'] == 1:
            first_floor = 1
        else:
            first_floor = 0

        # Значения столбцов
        cols_values = np.array(
            [
                self.data['floor'],
                self.data['floors_count'],
                self.data['rooms_count'],
                self.data['has_furniture'],
                self.data['district'],
                self.data['nearest_underground'],
                self.data['is_seller_agent'],
                self.data['parking_type'],
                last_floor,
                first_floor,
                np.log(self.data['area']),
                np.log(self.data['living_area']),
                np.log(self.data['kitchen_area']),
                self.data['has_balconies'],
                self.data['lifts_count'],
                self.data['has_cargo_lifts'],
            ]
        ).reshape(1, 16)

        pd_data = pd.DataFrame(cols_values, columns=cols_names)
        return pd_data

    # Функция, возвращающая предсказание
    def get_prediction(self):
        pipeline = self.deserialize_pipeline()
        user_data = self.preprocess_data()
        predict = np.exp(pipeline.predict(user_data)) + 1
        return '{:.2f}'.format(predict[0])
