import os

# Define the root directory and output file
root_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(root_dir, "complete_codebase.md")

# Supported file types and their language labels
file_types = {
    '.py': 'Python',
    '.r': 'R',
    '.vba': 'VBA'
}

# Directories to exclude
exclude_dirs = {'__pycache__', 'venv'}

# Initialize counters
line_counts = {lang: 0 for lang in file_types.values()}
total_lines = 0

# Function to count lines in a file
def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return len(f.readlines())

# Function to consolidate code into markdown format
def consolidate_code(file_path, lang, output_md):
    with open(file_path, 'r', encoding='utf-8') as f:
        output_md.write(f"\n\n## {file_path} ({lang})\n\n")
        output_md.write("```" + lang.lower() + "\n")
        output_md.write(f.read())
        output_md.write("\n```\n")

# Traverse directories, consolidate files, and count lines
with open(output_file, 'w', encoding='utf-8') as output_md:
    for subdir, _, files in os.walk(root_dir):
        # Skip excluded directories
        if any(exclude in subdir for exclude in exclude_dirs):
            continue
        
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in file_types:
                file_path = os.path.join(subdir, file)
                lang = file_types[file_ext]
                
                # Count lines in the file
                lines_in_file = count_lines_in_file(file_path)
                line_counts[lang] += lines_in_file
                total_lines += lines_in_file
                
                # Consolidate the code into the markdown file
                consolidate_code(file_path, lang, output_md)

# Print the total lines of code for each language and overall
print("Lines of Code per Language:")
for lang, count in line_counts.items():
    print(f"{lang}: {count} lines")
print(f"Total Lines of Code: {total_lines} lines")

# Confirm completion
print(f"\nConsolidation complete. Codebase saved to {output_file}.")
