# https://ocefpaf.github.io/python4oceanographers/blog/2015/08/03/fiona_gpx/

import functools
import glob
import itertools
import os
import sys

import cartopy.crs
import cartopy.io.img_tiles
import fiona
import matplotlib.pyplot as plt
import pyproj
import shapely.geometry
import tqdm

DETAIL_LEVEL = 15   # 17 = all street names
DPI = 300


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

METERS_PER_MILE = 1609.34

boundss = []
walks = []
total = 0
for gpxname in sorted(glob.glob(sys.argv[1])):
    with fiona.open(gpxname, layer="routes") as layer:
        lb = layer.bounds
        walk = shapely.geometry.shape({
            "type": "LineString",
            "coordinates": layer[0]["geometry"]["coordinates"],
        })
        walks.append(walk)
        dist = pyproj.Geod(ellps="WGS84").geometry_length(walk)
        total += dist
    boundss.append((lb[0], lb[1]))
    boundss.append((lb[2], lb[3]))
all_points = shapely.geometry.MultiPoint(boundss)
print(total / METERS_PER_MILE, "miles")

sb = all_points.bounds
pad = .01
extent = [sb[0]-pad, sb[2]+pad, sb[1]-pad, sb[3]+pad]

os.makedirs("out", exist_ok=True)

def zip_end(long, short):
    """Zip long and short together, aligned at the end."""
    if not long:
        shorts = []
    else:
        shorts = short[-len(long):]
    together = list(itertools.zip_longest(reversed(long), reversed(shorts), fillvalue=short[0]))
    return list(reversed(together))

def plot_shapes(shapes, styles, fname, detail_level=DETAIL_LEVEL, dpi=DPI):
    fig, ax = plt.subplots(
        subplot_kw=dict(projection=tiles.crs),
    )
    ax.set_extent(extent)
    ax.apply_aspect()
    ax.add_image(tiles, detail_level)

    for shape, style_kwargs in zip_end(shapes, styles):
        if shape is not None:
            ax.add_geometries(
                [shape],
                cartopy.crs.PlateCarree(),
                **style_kwargs,
            )

    plot_png(ax, fname, dpi=dpi)
    plt.close(fig)

styles = [
    dict(edgecolor="#000000", linewidth=.2, facecolor="none"),
    #dict(edgecolor="#7f0000", linewidth=.5, facecolor="none"),
    #dict(edgecolor="#0000ff", linewidth=1, facecolor="none"),
    #dict(edgecolor="#00ff00", linewidth=1, facecolor="none"),
    dict(edgecolor="#ff0000", linewidth=1, facecolor="none"),
]

# first image no walks, last image all walks, not colored.
walks += [None] * (len(styles) - 1)
for num in tqdm.tqdm(range(len(walks) + 1)):
    plot_shapes(walks[:num], styles, f"out/{num:03d}.png")

# Plot everything larger with more detail.
print("panwalks_large.png")
plot_shapes(walks, styles[:1], "panwalks_large.png", detail_level=DETAIL_LEVEL+1, dpi=1200)
