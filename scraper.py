import requests
from bs4 import BeautifulSoup, Tag
from collections import Counter
import sys
import csv
import asyncio
from pyppeteer import launch


async def main(request_url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(request_url)
    content = await page.content()
    await browser.close()
    return content


def css_path(element):
    if not (isinstance(element, Tag)):
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
                selector += ":nth-of-type(" + str(nth) + ")"
        path = [selector] + path
        element = element.parent
    return " > ".join(path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments! Please provide an input file.")
        sys.exit(1)
    # Input file: TSV file with two fields (url, jsRenderRequired <accepted_values>: 'true', 'false')
    # Please refer `sample.tsv` for better understanding
    input_file = str(sys.argv[1])
    tag = str(sys.argv[2])
    with open(input_file, 'r') as f:
        input_rows = list(map(lambda line: line.split('\t'), f.readlines()))
    output = []
    for url, jsEnabled, *_ in input_rows:
        r = requests.get(url)
        htmlContent = bytes()

        if jsEnabled == "true":
            htmlContent = bytes(asyncio.get_event_loop().run_until_complete(main(url)), encoding='UTF-8')
        else:
            htmlContent = r.content

        soup = BeautifulSoup(htmlContent, 'html5lib')
        links = soup.findAll(tag)
        paths = [css_path(element) for element in links]

        for selector, count in Counter(paths).items():
            output.append([url, selector, count])

    with open('output.tsv', 'wt') as output_file:
        tsv_writer = csv.writer(output_file, delimiter='\t')
        tsv_writer.writerow(['url', 'selector', 'count'])
        [tsv_writer.writerow(row) for row in output]
