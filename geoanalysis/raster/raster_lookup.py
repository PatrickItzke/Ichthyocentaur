import rasterio
from rasterio import windows
import sys

class RasterValueReader(object):
    
    def __init__(self, rasterio_src, windowed_read=False):
        
        self.raster_src = rasterio_src
        self.windowed_read = windowed_read

        if windowed_read:
            block_rows, block_columns = rasterio_src.block_shapes[0]
            self.block_rows = block_rows
            self.block_columns = block_columns
            


    def getCoordinateBandValue(self, latitude, longitude, band_num):
        """ gets the raster cell value for given latitude and longitude """
        if self.windowed_read:
            return self.getCoordinateBandValueWindowedRead(latitude, longitude, band_num)
        else:
            row, col = self.raster_src.index(longitude, latitude)
            raster = self.raster_src.read(band_num)
            return raster[row, col]


    def getCoordinateBandValueWindowedRead(self, latitude, longitude, band_num):
        """ gets the raster value for given latitude and longitude in a windowed read. Needed for rasters not fitting in memory."""
        row, col = self.raster_src.index(longitude, latitude)
        blocks_row =  row // self.block_rows
        blocks_col = col // self.block_columns        
        window = windows.Window(blocks_col*self.block_columns, blocks_row*self.block_rows, self.block_columns, self.block_rows)
        block_values  = self.raster_src.read(band_num, window=window)
        return block_values[row-(blocks_row*self.block_rows), col-(blocks_col*self.block_columns)]

