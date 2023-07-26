import subprocess
import sys
import os

# Define the command-line arguments for the script
if len(sys.argv) != 3:
    print("Usage: pandora.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} does not exist")
    sys.exit(1)

# Call the formatter.py script to format the input data
formatter_cmd = ["python", "./formatter.py", "-a", input_file, f"{output_file}.txt.tmp"]
subprocess.run(formatter_cmd, check=True)

# Add a header section to the formatted output
header = br"""$p_{\mathrm{T}}$ (GeV/c)
1
$R_{AA}$
Centrality
yes
none
none
2
sys(uncorr)
symmetric
sys(norm)
symmetric
"""

with open(f"{output_file}.txt.tmp", "rb") as tmp_file:
    formatted_data = tmp_file.readlines()[1:]   # Consider only everything past the first line in the temporary file
    formatted_data.append(b"***\n")

with open(output_file, "wb") as out_file:
    out_file.write(header + b"".join(formatted_data))

# Call the yaml_data C++ executable to convert the formatted data to YAML
yaml_cmd = ["./yaml_data", "1", output_file]
subprocess.run(yaml_cmd, check=True)

# Remove the temporary output file created by formatter.py
subprocess.run(["rm", f"{output_file}.txt.tmp"], check=True)

# Remove the intermediate .txt file created by pandora.py
subprocess.run(["rm", f"{output_file}"], check=True)