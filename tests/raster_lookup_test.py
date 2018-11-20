import sys
import unittest
import rasterio
import numpy
from geoanalysis.raster import raster_lookup 

class Test_RasterLookupTest(unittest.TestCase):
    def test_raster_lookup(self):
        
        with rasterio.open('./tests/TRMM_3B43M_2016-08-01_rgb_1440x720.tiff') as src:
            reader = raster_lookup.RasterValueReader(src)
            value = reader.getCoordinateBandValue(11.581074, 48.165809, 1)
            
            self.assertGreater(value, -999, "Value is " + value.astype(str))

    def test_raster_lookup_windowed(self):
        with rasterio.open('./tests/TRMM_3B43M_2016-08-01_rgb_1440x720.tiff') as src:
            
            reader = raster_lookup.RasterValueReader(src, windowed_read=True)
            value = reader.getCoordinateBandValue(11.581074, 48.165809, 1)
            
            self.assertGreater(value, -999, "Value is " + value.astype(str))


if __name__ == '__main__':
    unittest.main()


