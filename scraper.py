import requests
from bs4 import BeautifulSoup, Tag
from collections import Counter
import sys
import csv


def cssPath(element):
    if not(isinstance(element, Tag)):
        return
    path = []
    while isinstance(element, Tag):
        selector = element.name.lower()
        if 'class' in element.attrs:
            selector += '.' + element['class'][0]
            path = [selector] + path
            break
        elif 'id' in element.attrs:
            selector += '#' + element['id']
            path = [selector] + path
            break
        else:
            sibling = element
            nth = 1
            while sibling == sibling.previous:
                if sibling.name.lower() == selector:
                   nth += 1
            if nth != 1:
                selector += ":nth-of-type("+str(nth)+")"
        path = [selector] + path
        element = element.parent
    return " > ".join(path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments! Please provide an input file.")
        sys.exit(1)
    input_file = str(sys.argv[1])
    tag = str(sys.argv[2])
    with open(input_file, 'r') as f:
        urls = f.readlines()
    output = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        links = soup.findAll(tag)
        paths = [cssPath(element) for element in links]

        for selector, count in Counter(paths).items():
            output.append([url, selector, count])

    with open('output.tsv', 'wt') as output_file:
        tsv_writer = csv.writer(output_file, delimiter='\t')
        tsv_writer.writerow(['url', 'selector', 'count'])
        [ tsv_writer.writerow(row) for row in output ]
