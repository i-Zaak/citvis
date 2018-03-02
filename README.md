# citvis

Extraction and interactive visualization of citation network. Intended use is to support individual literature review.

## How to use


General workflow is following:

1. Add papers in pdf format to the `papers` directory.
2. Fill in the bibliographic data to all papers into the `citations.bib` file. File names (without .pdf suffix) has to match the bibtex keys.
3. run `make` to extract the 
4. run `make serve` to create a local webserver with the visualization.

All links can be annotated by hand, for example by the context of the citation from the citing text. The annotations are stored in the `annotated.json` file, which has to be semi-manually kept up to date with the extracted citations. This is achieved by running `make backport`. For example:

{
"somepaper": {
    "someotherpaper": "This paper builds upon somepaper..",
    "someanotherpaper": ""
  },
  ...
}


The appearence of particular nodes can be set in the `highlight.json` file. The style for every node (which is to differ from default) is given in key-value pairs in graphviz language. E.g.:

```
{
"somepaper": {
    "color": "red",
    "peripheries": "2"
  },
 "someotherpaper": {
    "color": "green"
  }
}
```


## How it works

The citation network is created by searching for the titles of the papers in the text extracted from the pdf of the other papers. This obviously works only for pdfs with embedded text, not for scanned documents. If some pdf is mangeled, or cites some other paper not exactly, I just edit the pdf, and add the text of correct citation (e.g. using ocular).
