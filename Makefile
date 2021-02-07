.PHONY: all walks gif png publish clean

GPXS = /Users/ned/walks/brookline/*.gpx
GIF = panwalks.gif
PNG = panwalks.png
LAST = panwalks_large.png
FINAL_FRAME = $$(ls -1 out/*.png | tail -1)

after: walks publish tidy

all: $(LAST) $(PNG) $(GIF)

walks $(LAST): $(GPXS)
	python dogpx.py "$(GPXS)"

gif $(GIF): $(LAST)
	convert -delay 15 -loop 0 out/*.png -delay 1000 $(FINAL_FRAME) -strip -coalesce -layers Optimize out/$(GIF)
	gifsicle -i out/$(GIF) -O3 --colors 12 -o $(GIF)

png $(PNG): $(LAST)
	cp $(FINAL_FRAME) $(PNG)

publish: all
	scp panwalks* drop1:drop1/www

tidy:
	rm -rf out .DS_Store

clean: tidy
	rm -rf *.png *.gif

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
