#!/usr/env/bin/python3
# scannerfilematch.py
# search DNAnexus array project for scanner backup files
# usage: python scannerfilematch.py featureextraction_images.txt > 190502_FEscannerfilereport.txt
import dxpy
import argparse
from subprocess import Popen, PIPE

def search(filename):
    """Search DNAnexus scanner backup project for file and print if found or missing"""
    fsearch = str(filename.rstrip()) + "*"
    pp = Popen(['dx', 'find', 'data', '--name', fsearch, '--project', 'project-FGfQ9y006gPy9xj10B3f0P3Y'], stdout=PIPE, stderr=PIPE)
    returned, err = pp.communicate()
    if returned:
        print(f"{filename} found")
    else:
        print(f"{filename} missing")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file')
    infile = parser.parse_args().image_file
    with open(infile, 'r') as f:
        lines = [ line.rstrip() for line in f.readlines() ]
    for line in lines:
        search(line)


if __name__ == '__main__':
    main()