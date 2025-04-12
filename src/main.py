from textnode import TextNode, TextType
import os
import shutil

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


    # Now recursively copy everything from source to destination
    # You'll need to implement this part!
    # Hint: Use os.listdir to get contents, check if each item is a file or directory
    # If it's a file, copy it with shutil.copy
    # If it's a directory, recursively call this function


def main():
    copy_static("static", "public")
    node = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(node)


main()
