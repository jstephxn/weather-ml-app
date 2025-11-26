import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        
    def test_model_app_integration(self):
        # Valid test input that should work with the trained model
        form_data = {
            'temperature': '275.15',   # Kelvin
            'pressure': '1013',        # hPa
            'humidity': '85',          # %
            'wind_speed': '3.6',       # m/s
            'wind_deg': '180',         # degrees
            'rain_1h': '0',            # mm
            'rain_3h': '0',            # mm
            'snow': '0',               # mm
            'clouds': '20'             # %
        }

        response = self.client.post('/', data=form_data)

        # Ensure that the result page includes a weather prediction
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'prediction result', response.data.lower())
        self.assertIn(b'the weather is:', response.data.lower())
    
        # Ensure that the result page includes a prediction time
        self.assertIn(b'prediction time:', response.data.lower())

        html_text = response.data.decode('utf-8').lower()
        valid_classes = [
            'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
            'misty', 'rainy', 'smokey', 'thunderstorm'
        ]
        found = any(weather in html_text for weather in valid_classes)
        
        # Ensure that classification is in valid classes
        self.assertTrue(found, "Predicted class is not one of the 9 valid weather classes")

if __name__ == '__main__':
    unittest.main()
