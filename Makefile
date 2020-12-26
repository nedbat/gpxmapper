doit:
	python dogpx.py
	convert -delay 15 -loop 1 out_*.png -strip -coalesce -layers Optimize panwalks.gif
	cp $$(ls -1 out_*.png | tail -1) panwalks.png
	rm out_*.png

publish: doit
	cp panwalks* ~/web/stellated/pix

clean:
	rm -rf *.png *.gif .DS_Store
