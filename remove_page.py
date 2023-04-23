import os
import argparse
from PyPDF2 import PdfWriter, PdfReader
import logging

logging.basicConfig(format='[%(levelname)s:%(asctime)s]: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def parsingArguments():
    parser = argparse.ArgumentParser(
        description='Merge all pdf files in dir that does not end with "merged" into one output file')

    parser.add_argument('dir', help='working directory')
    parser.add_argument('input', help='input pdf file to edit')
    parser.add_argument('output', help='output file name.\
                         It is created in the same directory as the input files')
    parser.add_argument('--remove_pages', nargs='+', type=int)
    return parser.parse_args()


def main():
    args = parsingArguments()
    input_fileName = args.input
    output_fileName = args.output
    pagesToRemove = args.remove_pages
    pagesToRemove_startindex_0 = [x - 1 for x in pagesToRemove]

    with cd(args.dir):
        output = PdfWriter()
        input = PdfReader(open(input_fileName, "rb"))

        logger.info(input_fileName + " has %d pages", len(input.pages))
        logger.info('removing pages: %s', pagesToRemove)

        for pageNumber in range(len(input.pages)):
            if pageNumber not in pagesToRemove_startindex_0:
                output.add_page(input.pages[pageNumber])
        outputStream = open(output_fileName, "wb")
        output.write(outputStream)


main()
