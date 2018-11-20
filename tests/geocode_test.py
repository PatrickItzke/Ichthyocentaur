import unittest
from geoanalysis.geocoding import geocoder 

class Test_Geocoder(unittest.TestCase):
    
    def test_geocode(self):
        longitude, latitude = geocoder.geocode('Test address')
        self.assertGreaterEqual(longitude, -180.0)
        self.assertLessEqual(longitude, 180.0)
        self.assertGreaterEqual(latitude, -90.0)
        self.assertLessEqual(latitude, 90.0)


if __name__ == '__main__':
    unittest.main()