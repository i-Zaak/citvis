"""Reads the citation data in json format and outputs the citation network in
graphviz format.

Usage:
    draw_citations.py <JSON_FILE> <BIBTEX_FILE> [-s STYLE_FILE]

Arguments:
    JSON_FILE       Citation network.
    BIBTEX_FILE     Database containing publication titles and authors.

Options:
    -h --help
    -s STYLE_FILE   File with node styles in json format.
"""

from docopt import docopt
import json
import re
import bibtexparser

preamble = """digraph citations {
"""

def year_from_key(key):
    year = re.findall("[0-9]{4}", key)[0]
    return year

if __name__ == "__main__":
    args = docopt(__doc__)
    filename = args['<JSON_FILE>']
    bib_filename = args['<BIBTEX_FILE>']
    highlight_file = args['-s']

    # read the citation network data
    with open(filename) as infile:
        citations = json.load(infile)

    # read the biblio data
    with open(bib_filename) as bib_file:
        bib = bibtexparser.load(bib_file).entries_dict

    # output the network in graphviz format
    print preamble

    all_years = set()
    for key, citation in citations.iteritems():
        all_years.add(year_from_key(key))
        for dest_key, _ in citation.iteritems():
            all_years.add(year_from_key(dest_key))

    all_years = list(all_years)
    all_years.sort()
    print " -> ".join(all_years[::-1])

    if highlight_file:
        with open(highlight_file) as high_file:
            highlights = json.load(high_file)
        for key, style in highlights.iteritems():
            print '%s [' % key,
            print ','.join([ '%s=%s'%(key,val) for key, val in style.iteritems()]),
            print ']'

    # citation edges
    all_keys = set()
    for key, citation in citations.iteritems():
        for dest_key, context in citation.iteritems():
            print '%s -> %s [ tooltip="[%s]&#10;&#10;%s"]' % (key, dest_key, key, context)
            all_keys.add(dest_key)
        all_keys.add(key)

    # query bib database for key titles
    for key in all_keys:
        if key in bib.keys():
            print '%s [tooltip="%s&#10;&#10;%s"]' % (key,bib[key]['title'], bib[key]['author'])
    
    # extract the years
    year_ranks = {}
    for key in all_keys:
        year = year_from_key(key)
        year_ranks.setdefault(year,[]).append(key)

    # force same years on same line (in order)
    for year in all_years:
        print "{rank = same; " + year + "; " ,
        for key in year_ranks[year]:
            print key + "; ",
        print "}"
    print "}"
