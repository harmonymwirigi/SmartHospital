from scipy.stats.kde import gaussian_kde
import matplotlib.pyplot as plt
import numpy as np
from apps import db
import base64
from apps.home.models import SecondTest
def graph(id):
    def render_picture(data):
        render_pic = base64.b64encode(data).decode('ascii')
        return render_pic
    x, y = np.genfromtxt('C:/Users/Harmony/PycharmProjects/sanakom/apps/home/coordinates.csv', delimiter=',', unpack=True)
    y = y[np.logical_not(np.isnan(y))]
    x = x[np.logical_not(np.isnan(x))]
    k = gaussian_kde(np.vstack([x, y]))
    xi, yi = np.mgrid[x.min():x.max():x.size ** 0.5 * 1j, y.min():y.max():y.size ** 0.5 * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    fig = plt.figure(figsize=(7, 8))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    # alpha=0.5 will make the plots semitransparent
    ax1.pcolormesh(xi, yi, zi.reshape(xi.shape), alpha=0.5)
    ax2.contourf(xi, yi, zi.reshape(xi.shape), alpha=0.5)

    ax1.set_xlim(x.min(), x.max())
    ax1.set_ylim(y.min(), y.max())
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim(y.min(), y.max())

    # you can also overlay your soccer field
    im = plt.imread('C:/Users/Harmony/PycharmProjects/sanakom/apps/home/tailight2.png')
    # ax1.imshow(im, extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    # ax2.imshow(im, extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto')
    fig.savefig('C:/Users/Harmony/PycharmProjects/sanakom/apps/home/result.png')
    k = "C:/Users/Harmony/PycharmProjects/sanakom/apps/home/result.png"
    def convert(filename):
        with open(filename, 'rb') as file:
            data = file.read()
        return data
    picture = SecondTest(made_by = id, picture = render_picture(convert(k)))
    db.session.add(picture)
    db.session.commit()