import os
import shutil
from markdown_to_blocks import markdown_to_html_node, extract_title
import sys

def main():

    basepath = sys.argv[0] or "/"

    staticToPublic()
    generate_pages_recursive('content', 'template.html', 'docs', basepath)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):


    entries = os.listdir(dir_path_content)

    for entry in entries:

        item = os.path.join(dir_path_content, entry)
        dest_item = os.path.join(dest_dir_path, entry)

        if os.path.isfile(item):

            if entry.lower().endswith('.md') or entry.lower().endswith('.markdown'):

                dest_html = os.path.splitext(dest_item)[0] + '.html'
                generate_page(item, template_path, dest_html, basepath)

        elif os.path.isdir(item):
            generate_pages_recursive(item, template_path, dest_item, basepath)

def generate_page(from_path, template_path, dest_path, basepath):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content) or ""

    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    page_content = page_content.replace('href="/', 'href="').replace('src="/', 'src="')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)


def staticToPublic():
    destPath = "./public"

    if ( not os.path.exists(destPath) ):
        os.mkdir(destPath)

    try:
        print("Cleaning public dir")
        shutil.rmtree(destPath)
        os.mkdir(destPath)
    except Exception:
        raise OSError("Couldn't clear the dest folder")

    sourcePath = "./static"

    if ( os.path.exists(sourcePath) ):

        recurserCopy(sourcePath, destPath)

    else:
        raise FileNotFoundError("Couldn't resovle the source path ", sourcePath)



def recurserCopy(sourcePath, destPath):

    entries = os.listdir(sourcePath)


    for entry in entries:

        item = os.path.join(sourcePath, entry)
        if os.path.isfile(item):

            shutil.copy2(item, destPath)

            print(f"Copied File {item} to {destPath}")

        elif os.path.isdir(item):

            dirDestPath = os.path.join(destPath, entry)
            if not os.path.exists(dirDestPath):
                os.mkdir(dirDestPath)

            print(f"Creating subDir {dirDestPath}")

            recurserCopy(item, dirDestPath)

    


if __name__ == "__main__":
    main()