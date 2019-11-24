import os
import argparse
from PyPDF2 import PdfFileMerger
import logging

logging.basicConfig(format='[%(levelname)s:%(asctime)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S',level=logging.DEBUG)
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

def parsingArguments() :
    parser = argparse.ArgumentParser(description='Merge all pdf files in dir that does not end with "merged" into one output file')
    
    parser.add_argument('dir', help='identify which directories will be affected by the command')
    parser.add_argument('output', help='output file name. suffix "_merged" will be added to it. it is created in the same directory as the input files')
    
    return  parser.parse_args()


def getListOfFilesToMerge():
    filesList = []

    for file in os.listdir('.'):
        if not file.startswith('merged_') and file.endswith('.pdf'):
                filesList.append(file)
    return filesList

def mergeFiles(filesToMerge, output):
    merger = PdfFileMerger()
    for file in filesToMerge:
        logger.info('[INFO] merging file: ' + file)
        input = open(file, "rb")
        merger.append(input)
    # Write to an output PDF document
    output = open(output, "wb")
    merger.write(output)
    logger.info('[INFO] merging successful.')


def main():
    args = parsingArguments()

    currentDir = args.dir
    outputFile = args.output


    with cd(currentDir):
        filesToMerge = getListOfFilesToMerge()
        mergeFiles(filesToMerge, 'merged_' + outputFile)
        

main()