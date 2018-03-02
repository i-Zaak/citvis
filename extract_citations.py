"""Finds the citations between papers in pdf by looking for titles in the fulltext. The names of the pdf files need to match the keys in supplied bibtex database for title query.

Usage:
    extract_citations.py <PDF_DIRECTORY> <BIBTEX_FILE>

Arguments:
    PDF_DIRECTORY   Where to look for the pdf files.
    BIBTEX_FILE     Database containing the publication titles.
"""

from subprocess import check_output
import re
import string
import bibtexparser
import glob, os
import json
from docopt import docopt

def compile_title_re(title):
    title = title.lstrip()
    title = title.rstrip(string.whitespace + ".")
    title_ws = re.sub('[\W\s]+','[\W\s]+',title)
    title_re = re.compile(title_ws, re.IGNORECASE | re.MULTILINE)
    return title_re


def read_bib(filename):
    with open(filename) as bib_file:
        bib = bibtexparser.load(bib_file).entries_dict
    return bib



def read_text(key):
    t = check_output(["pdftotext", "-enc", "ASCII7" , key + ".pdf" , "-"])
    return t
    


if __name__ == "__main__":
    args = docopt(__doc__)
    bibtex_file = args['<BIBTEX_FILE>']
    pdf_dir = args['<PDF_DIRECTORY>']
    
    bib = read_bib(bibtex_file)
    
    os.chdir(pdf_dir)
    keys = glob.glob("*.pdf")
    keys = map(lambda x: os.path.splitext(x)[0],keys)
    

    title_res = {}
    for key in keys:
        title = bib[key]['title']
        title_res[key] = compile_title_re(title)
    
    citations = {}
    for key in keys:
        text = read_text(key)
        for cited_key in keys:
            if cited_key == key:
                continue
            if title_res[cited_key].search(text):
                #print key + " cites " + cited_key
                if citations.has_key(key):
                    citations[key][cited_key] = ""
                else:
                    citations[key] = {cited_key:""}

    print json.dumps(citations, indent=2, sort_keys=True)



