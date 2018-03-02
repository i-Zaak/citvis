PAPERS = $(wildcard papers/*)

all:build/citations.svg

build/citations.json:citations.bib $(PAPERS)
	python extract_citations.py papers citations.bib > build/citations.json

build/merged.json: build/citations.json annotated.json
	python merge_annotations.py annotated.json build/citations.json  > build/merged.json

build/citations.dot: citations.bib build/merged.json highlight.json
	python draw_citations.py build/merged.json citations.bib -s highlight.json > build/citations.dot

build/citations.svg: build/citations.dot
	dot  -T svg -o build/citations.svg < build/citations.dot

serve:
	cd build
	@echo "Go to http://localhost:8000 to view the interactive visualisation."
	python -m SimpleHTTPServer

backport:
	meld annotated.json build/merged.json

clean:
	rm -f build/*
