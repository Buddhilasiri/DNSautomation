import os

def extract_cf_proxied(input_file, output_file):
    """
    Reads a text file, extracts lines containing 'cf_tags=cf-proxied:true',
    and writes them to a separate output file.

    Parameters:
    input_file (str): Path to the input text file.
    output_file (str): Path to the output text file where filtered lines will be saved.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if 'cf_tags=cf-proxied:true' in line:
                    outfile.write(line)
        print(f"Extraction complete. Output saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace these with actual file names
    input_files = ["########.txt", "########.txt"]
    
    for input_file in input_files:
        output_file = f"{os.path.splitext(input_file)[0]}_proxied.txt"
        extract_cf_proxied(input_file, output_file)
