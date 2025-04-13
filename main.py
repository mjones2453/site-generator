from textnode import TextNode, TextType
import os
import shutil
from block_markdown import markdown_to_html_node
from htmlnode import *

def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)
    path_list = os.listdir(source)

    for i in path_list:
        source_path = os.path.join(source, i)
        destination_path = os.path.join(destination, i)

        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_static(source_path, destination_path)

def extract_title(markdown):
    for item in markdown.splitlines():
        if item.startswith("# "):
            return item.lstrip("# ")
    # If no H1 header is found, return a default title or filename-based title
    return "Untitled Page"  # Default fallback

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as file:
        markdown_content = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_version = markdown_to_html_node(markdown_content)
    html_content = html_version.to_html()
    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Processing directory: {dir_path_content}")
    entries = os.listdir(dir_path_content)

    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        
        if os.path.isfile(entry_path) and entry_path.endswith('.md'):
            # Special case for index.md files
            if entry == "index.md":
                dest_file = os.path.join(dest_dir_path, "index.html")
            else:
                # For non-index files, create a directory with the name and put index.html inside
                base_name = os.path.splitext(entry)[0]  # Remove the .md extension
                dest_dir = os.path.join(dest_dir_path, base_name)
                dest_file = os.path.join(dest_dir, "index.html")
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            
            # Generate the page
            generate_page(entry_path, template_path, dest_file)
            
        elif os.path.isdir(entry_path):
            # Recursively process subdirectories
            subdirectory = os.path.join(dest_dir_path, entry)
            os.makedirs(subdirectory, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, subdirectory)



def main():
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

    print("\nGenerated files:")
    for root, dirs, files in os.walk("public"):
        for file in files:
            if file.endswith('.html'):
                print(os.path.join(root, file))
main()
