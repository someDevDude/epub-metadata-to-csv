#!/usr/bin/python

import argparse
import logging
import os
from exiftool import ExifToolHelper
import csv

argparser = argparse.ArgumentParser()
argparser.add_argument("-r", "--recursive", help="Recursively search files", action=argparse.BooleanOptionalAction)
argparser.add_argument("-o", "--outputLocation", help="Output file location")
argparser.add_argument("-s", "--silent", help="Disable logging",  action=argparse.BooleanOptionalAction)
argparser.add_argument("-i", "--inputLocation", help="Disable logging")
args = argparser.parse_args()

isRecursive = args.recursive if args.recursive is not None else False
outputLocation = args.outputLocation if args.outputLocation is not None else "./"
isSilent = args.silent if args.silent is not None else False
inputLocation = args.inputLocation if args.inputLocation is not None else None

def main():
  if os.path.exists(f"{outputLocation}/bookOutput.csv"):
    os.remove(f"{outputLocation}/bookOutput.csv")

  with open(f"{outputLocation}/bookOutput.csv", "a") as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["filename", "title", "author", "publisher"])
    logging.basicConfig(format='%(message)s', level=logging.DEBUG if not isSilent else logging.CRITICAL)
    logging.debug("Starting script")

    if inputLocation is None:
      logging.critical("Input location not specified, aborting")
      exit(1)
    
    extractMetadataForDirectory(inputLocation, csvWriter)

def extractMetadataForDirectory(directory, csvWriter):
  logging.debug(f"Starting {directory}")
  for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if os.path.isdir(f"{directory}/{filename}"):
      if isRecursive:
        extractMetadataForDirectory(f"{directory}/{filename}", csvWriter)
    elif filename.endswith(".epub") or filename.endswith(".pdf"):
      processFile(f"{directory}/{filename}", csvWriter)
    else:
      logging.debug(f"Unknown file type: {directory}/{filename}")

def processFile(fileLocation, csvWriter):
  logging.debug(f"found epub: {fileLocation}")
  with ExifToolHelper() as et:
    for metadata in et.get_metadata(fileLocation):
      csvWriter.writerow([fileLocation, metadata["XML:Title"] if "XML:Title" in metadata else "", metadata["XML:Creator"] if "XML:Creator" in metadata else "", metadata["XML:Publisher"] if "XML:Publisher" in metadata else ""])


if __name__ == "__main__":
  main()