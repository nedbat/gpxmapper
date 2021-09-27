.PHONY: after all savegpx walks large centuries gif png icon publish tidy clean

GPXS = /Users/ned/walks/brookline/*.gpx
GIF = panwalks.gif
PNG = panwalks.png
ICON = panwalks_icon.png
LARGE = panwalks_large.png
XLARGE = panwalks_xlarge.webp
WALK99 = out/099.png
FINAL_FRAME = $$(ls -1 out/*.png | tail -1)

after: savegpx all publish tidy

all: $(WALK99) $(LARGE) $(XLARGE) $(PNG) $(ICON) $(GIF) centuries

savegpx:
	mv -v /dwn/onthegomap-*.gpx ~/walks/brookline/$$(date +%Y%m%d)_brookline.gpx

walks $(WALK99): $(GPXS)
	python dogpx.py "$(GPXS)" walks

large $(LARGE): $(GPXS)
	python dogpx.py "$(GPXS)" large

xlarge $(XLARGE): $(GPXS)
	python dogpx.py "$(GPXS)" xlarge
	magick panwalks_xlarge.png \( \
		+clone -threshold 101% -fill white -draw \
			'circle %[fx:int(w/2)],%[fx:int(h/2)] %[fx:int(w/2)],%[fx:4300+int(h/2)]' \
		\) -channel-fx '| gray=>alpha' panwalks_xlarge.webp
	rm panwalks_xlarge.png

centuries:
	python dogpx.py "$(GPXS)" centuries

gif $(GIF): $(WALK99)
	eval $$(python tapergif.py out/$(GIF) out/*.png)
	gifsicle --no-conserve-memory -i out/$(GIF) -O3 --colors 12 -o $(GIF)

png $(PNG): $(WALK99)
	cp $(FINAL_FRAME) $(PNG)

icon $(ICON): $(PNG)
	convert $(PNG) -resize 256x256 $(ICON)

publish: $(GIF) $(XLARGE) $(PNG)
	scp panwalks* drop1:drop1/www

tidy:
	rm -rf out .DS_Store

clean: tidy
	rm -rf *.png *.gif *.webp

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
