import unittest
from app import app, classify_weather, load_model
import numpy as np

class TestUnit(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
    
    # Test proper handling of missing input field in the input
    def test_post_missing_field(self):
        form_data = {
            'temperature': '270.277',
            'pressure': '1006',
            'humidity': '84',
            # 'wind_speed' is missing on purpose
            'wind_deg': '274',
            'rain_1h': '0',
            'rain_3h': '0',
            'snow': '0',
            'clouds': '9'
        }
        response = self.client.post('/', data=form_data)

        # Page should still load
        self.assertEqual(response.status_code, 200)
        # Should show some kind of error message
        self.assertIn(b'error', response.data.lower())

    # Test that the model can be loaded correctly
    def test_model_can_be_loaded(self):
        model = load_model()
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, 'predict'))

    # Test model classification for CLEAR
    def test_clear_classification_output(self):
        test_input = np.array([269.686,1002,78,0,23,0,0,0,0]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'clear')

    # Test model classification for RAINY
    def test_rainy_classification_output(self):
        test_input = np.array([279.626,998,99,1,314,0.3,0,0,88]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'rainy')

    # CLOUDY test (instead of foggy), using the array you were given
    def test_cloudy_classification_output(self):
        # [291.15,1028,61,1,260,0,0,0,75]
        test_input = np.array([291.15,1028,61,1,260,0,0,0,75]).reshape(1, -1)
        class_result, _ = classify_weather(test_input)
        self.assertEqual(class_result, 'cloudy')

if __name__ == '__main__':
    unittest.main()
