# A Python program to extract text citations in the LLM outputs into CSV files for easy checking

import os
import re
import csv
import glob

def extract_brackets(md_file_path):
    """
    Extract text within square brackets from a markdown file along with line numbers.
    
    Args:
        md_file_path (str): Path to the markdown file
        
    Returns:
        list: List of tuples containing (line_number, text_in_brackets)
    """
    results = []
    
    with open(md_file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            # Find all instances of text within square brackets
            matches = re.findall(r'\[(.*?)\]', line)
            for match in matches:
                results.append((line_num, match))
    
    return results

def save_to_csv(data, csv_file_path):
    """
    Save extracted data to a CSV file.
    
    Args:
        data (list): List of tuples containing (line_number, text_in_brackets)
        csv_file_path (str): Path to save the CSV file
    """
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow(['Line Number', 'Text in Brackets'])
        # Write data
        writer.writerows(data)

def process_md_files(directory='.'):
    """
    Process all markdown files in the given directory.
    
    Args:
        directory (str): Directory to search for markdown files
    """
    # Find all markdown files in the directory
    md_files = glob.glob(os.path.join(directory, '*.md'))
    
    if not md_files:
        print(f"No markdown files found in {directory}")
        return
    
    for md_file in md_files:
        # Extract base name and create CSV file path
        base_name = os.path.splitext(md_file)[0]
        csv_file = f"{base_name}.csv"
        
        # Extract data from markdown file
        data = extract_brackets(md_file)
        
        # Save data to CSV file
        save_to_csv(data, csv_file)
        
        print(f"Processed {md_file} -> {csv_file} ({len(data)} bracket instances found)")

if __name__ == "__main__":
    import sys
    
    # Use command line argument for directory if provided, otherwise use current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    process_md_files(directory)
