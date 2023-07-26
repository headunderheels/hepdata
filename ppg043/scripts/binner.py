import argparse
import numpy as np
import pandas as pd

def find_bins(input_file, output_file=None):
    # Load data
    data = pd.read_csv(input_file, sep=' ', header=None, names=['value', 'count'])

    if len(data.columns) < 2:
        raise ValueError("Input data must have at least two columns")

    # Compute bin edges
    numeric_data = data[data.iloc[:, 0].apply(lambda x: isinstance(x, (int, float)))]
    if len(numeric_data) == 0:
        raise ValueError("Input data does not contain any numeric values")
    bin_edges = np.arange(numeric_data.iloc[:, 0].min(), numeric_data.iloc[:, 0].max() + 1, 1)
    data['bin'] = pd.cut(numeric_data.iloc[:, 0], bin_edges, labels=False)

    # Write output file if specified
    if output_file is not None:
        data.to_csv(output_file, sep=' ', index=False)

    return data

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Reconstruct bins from data in the PHENIX repository.')

    # Add input file argument
    parser.add_argument('input_file', metavar='input_file', type=str, help='the input file to process')

    # Add output file argument
    parser.add_argument('-o', '--output-file', metavar='output_file', type=str, help='the output file to write')

    # Parse arguments
    args = parser.parse_args()

    # Find bins and write to file
    find_bins(args.input_file, args.output_file)
    
    # Test: display output file
    if args.output_file is not None:
        print(pd.read_csv(args.output_file, sep=' ', header=0))

if __name__ == '__main__':
    main()