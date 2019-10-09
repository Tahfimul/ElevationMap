import gdal
import matplotlib.pyplot as plt
gdal.UseExceptions()

ds = gdal.Open('land_shallow_topo_2048.tif')
band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()

print(ds.)

print (elevation.shape)
print (elevation)

# for e in elevation:
#     for i in e:
#         print(str(i))
#     print("--------------")


plt.imshow(elevation, cmap='gist_earth')
plt.show()
