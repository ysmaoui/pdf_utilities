import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter
import logging


logging.basicConfig(format='[%(levelname)s:%(asctime)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    args = parsingArguments()

    odd_pages = PdfFileReader(open(args.file1, "rb"))
    even_pages = PdfFileReader(open(args.file2, "rb"))

    output = PdfFileWriter()

    # this is always valid:  odd_pages.numPages >= even_pages.numPages

    number_of_odd_pages = odd_pages.numPages
    number_of_even_pages = even_pages.numPages

    offset = number_of_odd_pages - number_of_even_pages + 1

    for i in range(number_of_odd_pages):
        logger.info("Adding pages: odd[%s]  even[%s]", i, odd_pages.numPages - (i + offset))
        output.addPage(odd_pages.getPage(i))
        if(number_of_odd_pages >= (i + offset)):
            output.addPage(even_pages.getPage(number_of_odd_pages - (i + offset)))

    outputStream = open(args.output, "wb")
    output.write(outputStream)


def parsingArguments():
    parser = argparse.ArgumentParser(
        description='merge 2 pdf files, the first one contains the odd pages\
                     and the second one contains the even pages.\
                     this is useful in case your scanner doesn\'t support duplex scanning')

    parser.add_argument(
        'file1', help='file1 contains odd pages in ascendent order [1,3,..]')
    parser.add_argument(
        'file2', help='file2 contains even pages in descendent order [..,4,2]')
    parser.add_argument(
        'output', help='output file name. suffix "_merged" will be added to it. it is created in the same directory as the input files')

    return parser.parse_args()


main()
