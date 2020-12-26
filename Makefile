.PHONY: all walks gif png publish clean

GPXS = /Users/ned/walks/brookline/*.gpx
GIF = panwalks.gif
PNG = panwalks.png
LAST = out/150.png panwalks_large.png

all: $(LAST) $(PNG) $(GIF)

walks $(LAST): $(GPXS)
	python dogpx.py "$(GPXS)"

gif $(GIF): $(LAST)
	convert -delay 15 -loop 1 out/*.png -strip -coalesce -layers Optimize $(GIF)

png $(PNG): $(LAST)
	cp $$(ls -1 out/*.png | tail -1) $(PNG)

publish: all
	cp panwalks* ~/web/stellated/pix

clean:
	rm -rf *.png *.gif out .DS_Store

# Making the conda environment.  Seems like it needs to be 3.7, and conda uses
# the "current" python to make environments, so:
# This won't work through make, run the commands in a shell.
#
# 1. Make a virtualenv with Python3.7
# 	mktmpenv -p python3.7 -n
# 2. Make a conda environment:
# 	conda create --yes -n gpxmapper
# 	conda activate gpxmapper
# 3. Install the requirements
# 	conda install --yes --file requirements.txt
# 4. Deactivate the virtualenv
# 	deactivate
# 5. Reactivate conda
# 	conda activate gpxmapper

.PHONY: env requirements

env:
	conda activate gpxmapper

requirements:
	conda install --file requirements.txt
