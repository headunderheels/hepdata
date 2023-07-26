#!/bin/zsh

# Define the input and output directories
input_dir="./binned/2"
output_dir="./output"

# Iterate over every file in the input directory
for input_file in ${input_dir}/*; do
    # Construct the output file path
    output_file=${output_dir}/$(basename ${input_file})

    # Call the pandora.py script for the input file
    python pandora.py ${input_file} ${output_file}
done