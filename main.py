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
    raise Exception("no H1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as file:
        original_path = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    html_version = markdown_to_html_node(original_path)
    html_content = html_version.to_html()
    title = extract_title(original_path)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template)



def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
main()
