# https://ocefpaf.github.io/python4oceanographers/blog/2015/08/03/fiona_gpx/

import functools
import glob
import os
import sys

import cartopy.crs
import cartopy.io.img_tiles
import fiona
import matplotlib.pyplot as plt
import shapely.geometry
import tqdm

DETAIL_LEVEL = 15   # 17 = all street names
DPI = 300
GPXS = "/Users/ned/walks/brookline/*.gpx"


def plot_png(ax, fname, dpi=DPI):
    plt = ax.get_figure()
    plt.get_axes()[0].set_axis_off()
    plt.savefig(fname, dpi=dpi, bbox_inches="tight", pad_inches=0)


class PositronTiles(cartopy.io.img_tiles.GoogleWTS):
    # Maybe there's already a way to get these tiles?
    def _image_url(self, tile):
        x, y, z = tile
        url = f"https://cartodb-basemaps-1.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"
        return url

    # We're drawing a lot of maps, cache the tiles
    @functools.lru_cache(maxsize=None)
    def get_image(self, tile):
        return super().get_image(tile)

tiles = PositronTiles()

boundss = []
walks = []
for gpxname in sorted(glob.glob(GPXS)):
    with fiona.open(gpxname, layer="routes") as layer:
        lb = layer.bounds
        walk = shapely.geometry.shape({
            "type": "LineString",
            "coordinates": layer[0]["geometry"]["coordinates"],
        })
        walks.append(walk)
    boundss.append((lb[0], lb[1]))
    boundss.append((lb[2], lb[3]))
all_points = shapely.geometry.MultiPoint(boundss)

sb = all_points.bounds
pad = .01
extent = [sb[0]-pad, sb[2]+pad, sb[1]-pad, sb[3]+pad]

os.makedirs("out", exist_ok=True)

# +2: first image no walks, last image all walks, not red.
for num in tqdm.tqdm(range(len(walks) + 2)):
    fig, ax = plt.subplots(
        subplot_kw=dict(projection=tiles.crs),
    )
    ax.set_extent(extent)
    ax.apply_aspect()
    ax.add_image(tiles, DETAIL_LEVEL)

    for iwalk, walk in enumerate(walks[:num]):
        latest = (iwalk == num-1)
        ax.add_geometries(
            [walk], 
            cartopy.crs.PlateCarree(),
            facecolor="none",
            edgecolor="red" if latest else "black",
            linewidth=1 if latest else .2,
        )

    plot_png(ax, f"out/{num:03d}.png")
    if num == len(walks) + 1:
        plot_png(ax, "panwalks_large.png", dpi=1200)
    plt.close(fig)
