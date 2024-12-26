import unittest
import pandas as pd
from pandas._libs.tslibs.timestamps import Timestamp
from backend.trend_model.trend_model import predict_next_failure, predict_next_n_failures

class TestTrendModel(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(True, "Este teste sempre deve passar.")

    def test_dataframe_creation(self):
        data = {
            "timestamp": pd.to_datetime([
                "2024-11-28 12:00:00",
                "2024-11-28 12:30:00",
                "2024-11-28 13:00:00",
            ]),
            "interval_minutes": [None, 30.0, 30.0],
        }
        df = pd.DataFrame(data)
        self.assertEqual(len(df), 3, "O DataFrame deveria conter 3 entradas.")
        self.assertIn("interval_minutes", df.columns, "O DataFrame deveria conter a coluna 'interval_minutes'.")

    def test_predict_function(self):
        data = {
            "timestamp": pd.to_datetime([
                "2024-11-28 12:00:00",
                "2024-11-28 12:30:00",
                "2024-11-28 13:00:00",
            ]),
            "interval_minutes": [None, 30.0, 30.0],
        }
        df = pd.DataFrame(data)
        prediction = predict_next_failure(df, window_size=2)
        self.assertIsNotNone(prediction, "A previsão não deveria ser None.")
        self.assertIsInstance(prediction, Timestamp, "A previsão deveria ser um objeto Timestamp.")

    def test_predict_next_n_failures(self):
        data = {
            "timestamp": pd.to_datetime([
                "2024-11-28 12:00:00",
                "2024-11-28 12:30:00",
                "2024-11-28 13:00:00",
            ]),
            "interval_minutes": [None, 30.0, 30.0],
        }
        df = pd.DataFrame(data)
        predictions = predict_next_n_failures(df, n=3, window_size=2)
        self.assertEqual(len(predictions), 3, "A previsão deveria conter 3 falhas.")
        for prediction in predictions:
            self.assertIsInstance(prediction, Timestamp, "Cada previsão deveria ser um objeto Timestamp.")

if __name__ == "__main__":
    unittest.main()
