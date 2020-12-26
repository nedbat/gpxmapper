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
