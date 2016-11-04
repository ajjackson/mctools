#! /usr/bin/env python
import ase.io
import argparse

def convert(input_filename,output_filename, from_format=None, to_format=None):

    try:
        structure = ase.io.read(input_filename, format=from_format)
    except:
        raise Exception("Trouble reading input file {0}".format(input_filename))

    structure.write(output_filename, format=to_format)

def main():
    parser = argparse.ArgumentParser(description="Convert between crystal file formats with ASE")
    parser.add_argument('input_file', type=str,
                        help="Path to crystal structure to be converted")
    parser.add_argument('output_file', type=str,
                        help="Output filename")
    parser.add_argument('-f','--from_format', default=None,
                        help="Input file format [If this argument is omitted, ASE will guess]")

    parser.add_argument('-t','--to_format',default=None,
                        help="Output file format [If this argument is omitted, ASE will guess]")
    args=parser.parse_args()

    convert(args.input_file,args.output_file,from_format=args.from_format, to_format=args.to_format)
    
if __name__ == '__main__':
    main()
