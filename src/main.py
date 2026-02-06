import os
import shutil
import sys
from textnode import TextNode, TextType
from splitter import markdown_to_html_node, extract_title

def copy_files_recursive(src_dir, dst_dir):
    """
    Recursively copy all files and subdirectories from src_dir to dst_dir.
    First deletes all contents of dst_dir to ensure a clean copy.
    
    Args:
        src_dir: Source directory path
        dst_dir: Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dst_dir):
        print(f"Deleting existing destination directory: {dst_dir}")
        shutil.rmtree(dst_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dst_dir}")
    os.mkdir(dst_dir)
    
    # Walk through source directory and copy all files and subdirectories
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(dst_dir, filename)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # Recursively copy subdirectory
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_files_recursive(src_path, dst_path)

def generate_page(from_path, template_path, dest_path, basepath):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown source file
        template_path: Path to the HTML template file
        dest_path: Path to write the generated HTML file
        basepath: Base path for the site (e.g., "/" or "/blog/")
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r") as f:
        markdown = f.read()

    # Read the template file
    with open(template_path, "r") as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown)

    # Replace placeholders in template
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # Replace href and src paths with basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    # Create any necessary directories
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Write the output file
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """
    Recursively crawl the content directory and generate an HTML page
    for every markdown file found, preserving the directory structure.
    
    Args:
        dir_path_content: Path to the content directory to crawl
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated pages
        basepath: Base path for the site (e.g., "/" or "/blog/")
    """
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(src_path):
            # Only process markdown files
            if entry.endswith(".md"):
                # Change .md extension to .html
                dest_filename = entry.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_filename)
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            # Recurse into subdirectory
            new_dest = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(src_path, template_path, new_dest, basepath)

def main():
    # Get basepath from CLI argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using basepath: {basepath}\n")

    # Copy static directory to docs directory
    copy_files_recursive("static", "docs")
    print("\nFile copy complete!\n")

    # Generate pages from all markdown files in content directory
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()