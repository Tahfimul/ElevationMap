import numpy as np
import matplotlib.pylab as plt
from scipy.ndimage.interpolation import zoom
from sklearn.cluster import KMeans
from skimage import measure

global im
im = plt.imread("nyc.jpg")

print(im.shape)



def plti(im, h=8, **kwargs):
    """
    Helper function to plot an image.
    """
    y = im.shape[0]
    x = im.shape[1]
    w = (y/x) * h
    plt.figure(figsize=(w,h))
    plt.imshow(im, interpolation="none", **kwargs)
    plt.axis('off')
    plt.show()

im_small = zoom(im, (0.2,0.2,1))
h,w = im_small.shape[:2]
im_small_long = im_small.reshape((h * w, 3))
im_small_wide = im_small_long.reshape((h,w,3))

km = KMeans(n_clusters=3)

km.fit(im_small_long)

#Orginal Image

cc = km.cluster_centers_.astype(np.uint8)
out = np.asarray([cc[i] for i in km.labels_]).reshape((h,w,3))

plti(out)

rng = range(4)

fig, axs = plt.subplots(nrows=1, ncols=len(rng), figsize=(15,15))

def to_grayscale(im, weights = np.c_[0.2989, 0.5870, 0.1140]):
    """
    Transforms a colour image to a greyscale image by
    taking the mean of the RGB values, weighted
    by the matrix weights
    """
    tile = np.tile(weights, reps=(im.shape[0],im.shape[1],1))
    return np.sum(tile * im, axis=2)
gray_im = to_grayscale(im)


# plti(gray_im, cmap='Greys')

#3 colors

for t, ax in zip(rng, axs):
    rnd_cc = np.random.randint(0,256, size = (3,3))
    out = np.asarray([rnd_cc[i] for i in km.labels_]).reshape((h,w,3))
    ax.imshow(out)
    ax.set_axis_off()



plt.show()


#Single color and black

cc = np.random.randint(0,256, size = (3,3))

img = np.asarray([cc[i] if i == 1 else [0,0,0]
                  for i in km.labels_]).reshape((h,w,3))

plti(img)

#Vectorization
seg = np.asarray([(1 if i == 1 else 0)
                  for i in km.labels_]).reshape((h,w))

contours = measure.find_contours(seg, 0.5, fully_connected="high")

simplified_contours = [measure.approximate_polygon(c, tolerance=5) for c in contours]

plt.figure(figsize=(5,10))

for n, contour in enumerate(simplified_contours):
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)


plt.ylim(h,0)
plt.axes().set_aspect('equal')
plt.show()

# #plti(im)
#
# # Split
# red = im[:, :, 0]
# green = im[:, :, 1]
# blue = im[:, :, 2]
#
# # Plot
# fig, axs = plt.subplots(2,2)
#
# cax_00 = axs[0,0].imshow(im)
# axs[0,0].xaxis.set_major_formatter(plt.NullFormatter())  # kill xlabels
# axs[0,0].yaxis.set_major_formatter(plt.NullFormatter())  # kill ylabels
#
# cax_01 = axs[0,1].imshow(red, cmap='Reds')
# fig.colorbar(cax_01, ax=axs[0,1])
# axs[0,1].xaxis.set_major_formatter(plt.NullFormatter())
# axs[0,1].yaxis.set_major_formatter(plt.NullFormatter())
#
# cax_10 = axs[1,0].imshow(green, cmap='Greens')
# fig.colorbar(cax_10, ax=axs[1,0])
# axs[1,0].xaxis.set_major_formatter(plt.NullFormatter())
# axs[1,0].yaxis.set_major_formatter(plt.NullFormatter())
#
# cax_11 = axs[1,1].imshow(blue, cmap='Blues')
# fig.colorbar(cax_11, ax=axs[1,1])
# axs[1,1].xaxis.set_major_formatter(plt.NullFormatter())
# axs[1,1].yaxis.set_major_formatter(plt.NullFormatter())
# plt.show()
