"""
    Copyright 2023 Riley Hanus, PhD
    Unauthorized copying and use of this file, via any medium is strictly prohibited
    Proprietary and confidential
    Written by Riley Hanus <hanusriley@gmail.com>, November 2023
"""

from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from jinja2 import Template
from urllib.parse import urlparse
import os as os
import shutil
import glob
import sys
import re as re
from pyfiglet import figlet_format

def toc_loop(toc, level=0, toc_list=[]):
    for item in toc:
        if isinstance(item, tuple):
            toc_loop(item, level)
        elif isinstance(item, list):
            level=level+1
            toc_loop(item, level)
        else:
            toc_list.append([item.title, item.href, level])
    
    return toc_list

def flatten_tex():
    # must be run from the directory make-texedbook.py is located in
    print('Flattening main.tex')
    os.system(
        '''
        cd .build/latex
        latexpand main.tex > main-flat.tex
        cd ../..
        '''
    )

def make_list_of_iframes():
    flatten_tex()
    with open('.build/latex/main-flat.tex', 'r') as file:
        main_flat = file.read()
    list_of_iframes = re.findall(r'\\InsertIframe{(.*?)}', main_flat)
    print("\nList of iframes:")
    print(list_of_iframes)
    return list_of_iframes

def insert_iframes(soup, list_of_iframes):
    divs = soup.find_all(class_="iframe")
    i=0
    for div in divs:
        div.clear()
        div.append(BeautifulSoup(list_of_iframes[i], "html.parser"))
        i=i+1
        print("<iframe> #" + str(i) + " inserted")

def make_list_of_htmls():
    flatten_tex()
    with open('.build/latex/main-flat.tex', 'r') as file:
        main_flat = file.read()
    list_of_htmls = re.findall(r'\\InsertHTML{(.*?)}', main_flat)
    print("\nList of HTML code blocks:")
    print(list_of_htmls)
    return list_of_htmls

def insert_htmls(soup, list_of_htmls):
    divs = soup.find_all(class_="customhtml")
    i=0
    for div in divs:
        div.clear()
        div.append(BeautifulSoup(list_of_htmls[i], "html.parser"))
        i=i+1
        print("<div> #" + str(i) + " inserted")

def calchub_insert_iframe(soup, full_page=False, height="800"):
    divs = soup.find_all(class_="calchub")
    for div in divs:
        print("Inserting calchub <iframe>...")
        href = div.find_all("a")[0]['href']
        parsed_href = urlparse(href)
        text = div.find_all("a")[0].parent.text
        if full_page:
            iframe_html = '<p>' + text + '</p> <iframe width="100%" height="' + height + '" src="' + parsed_href.geturl() + '"></iframe>'
        else:
            old_path = parsed_href.path
            new_path = old_path.replace("calcs", "embed")
            parsed_href = parsed_href._replace(path=new_path, query='showToolbar=true')
            iframe_html = '<p>' + text + '</p> <iframe width="100%" height="' + height + '"src="' + parsed_href.geturl() + '"></iframe>'

        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))

def youtube_insert_iframe(soup, width="560", height="315"):
    divs = soup.find_all(class_="youtube")
    for div in divs:
        print("Inserting youtube <iframe>...")
        href = div.find_all("a")[0]['href']
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe width="'+ width + '" height="' + height + '" src="' + href + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))

def trinket_insert_iframe(soup, width="100%", height="500"):
    divs = soup.find_all(class_="trinket")
    for div in divs:
        print("Inserting trinket <iframe>...")
        href = div.find_all("a")[0]['href']
        print(href)
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe src="' + href + '" width="' + width + '" height="' + height + '" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))

def panopto_insert_iframe(soup, width="560", height="315"):
    divs = soup.find_all(class_="panopto")
    for div in divs:
        print("Inserting panopto <iframe>...")
        href = div.find_all("a")[0]['href']
        href_embed = href.replace("Viewer", "Embed")
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe width="'+ width + '" height="' + height + '" src="' + href_embed + '"></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))

def clean_html(soup):
    soup = str(soup)
    soup = soup.replace(r"\relax", r"")
    return BeautifulSoup(soup, features="lxml")

def template_ebook(book_epub, sidebar_element_html, sidebar_html, template_html, css):
    print("Initializing .build/output/")
    target = os.path.join('.build', 'output')
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    
    print("Reading .epub file and building an Epub object...")
    book = epub.read_epub(book_epub)
    print("\n  Book Title: " + book.title + "\n")
    print(book.get_metadata("DC", "creator"))

    print("\nOpening html templates and building Template objects...")
    with open(sidebar_element_html, "r", encoding='utf-8') as f:
        sidebar_element_template = f.read()
    with open(sidebar_html, "r", encoding='utf-8') as f:
        sidebar_template = f.read()
    with open(template_html, "r", encoding='utf-8') as f:
        body_template = f.read()
    template_sidebar_element = Template(sidebar_element_template)
    template_sidebar = Template(sidebar_template)
    template_body = Template(body_template)

    # Setup sidebar and nav menu display options, content, and focus settings
    standard_display_options = 'bg-gray-75 text-gray-600 hover:bg-gray-200 hover:text-gray-900'
    sidebar_font_sizes = [' text-md font-bold ', ' text-sm font-bold ', ' text-xs ', ' text-xs ', ' text-xs ', ' text-xs ']

    print("\nConstructing TOC list based on .ncx content...")
    toc_list = toc_loop(book.toc)
    print("\nTable of contents: ")
    print(toc_list)
    item_name_list = [row[1].split('#')[0] for row in toc_list]

    focus_list = []
    focus_counter=0
    for element in toc_list:
        if element[2] == 0:
            focus_counter=focus_counter+1
        focus_list.append(focus_counter)

    # Get a list of document names for use when templating
    document_item_list = book.get_items()
    document_name_list = []
    for item in document_item_list:
        document_name_list.append(item.get_name())

    print('\nMaking template_main.html...')
    title_page_html = book.get_item_with_href("main.html").get_content()
    soup = BeautifulSoup(title_page_html, 'html.parser')
    body = soup.body

    # Build sidebar and template it into template
    sidebar_content = ''
    for element in toc_list:
        display_options = standard_display_options
        sidebar_content = sidebar_content + template_sidebar_element.render(sidebar_element_href="templated_main.html#" + element[1].split('#')[1],  
                                                                            sidebar_element_title=element[0], 
                                                                            display_options=display_options + sidebar_font_sizes[element[2]] + " px-" + str(4+4*element[2])) + '\n'
        sidebar = template_sidebar.render(sidebar_content=sidebar_content, standard_display_options=standard_display_options + sidebar_font_sizes[0] + " px-" + str(4+4*0)) + '\n'
    templated_html = template_body.render(title=book.title, sidebar=sidebar, body=body, standard_display_options=standard_display_options + sidebar_font_sizes[0] + " px-" + str(4+4*0)) + '\n'
    templated_soup = BeautifulSoup(templated_html, 'html.parser')
    
    print("\nLooping through Epub Document Items and appending body to the body of templated_main.html...")
    for item in book.get_items():
        if item.get_name() in item_name_list:
            print(item.get_name())
            new_content = item.get_content()
            new_soup = BeautifulSoup(new_content, 'html.parser')
            # Fixing hrefs such that they point to templated_main.html instead of xxx.html
            a_tags = new_soup.body.find_all("a", href=True) 
            for a_tag in a_tags:
                href = a_tag['href']
                for document_name in document_name_list:
                    if document_name in href:
                        href = href.replace(document_name, "templated_main.html")
                        a_tag['href'] = href
            # Insert iframes
            calchub_insert_iframe(new_soup)
            youtube_insert_iframe(new_soup)
            trinket_insert_iframe(new_soup)
            panopto_insert_iframe(new_soup)
            new_soup = clean_html(new_soup)
            new_body_html = new_soup.find('body').findChildren(recursive=False)
            for i in range(len(new_body_html)):
                templated_soup.body.append(new_body_html[i])
    print("\nInserting iframes...")
    list_of_iframes = make_list_of_iframes()
    insert_iframes(templated_soup, list_of_iframes)

    print("\nInserting html...")
    list_of_htmls = make_list_of_htmls()
    insert_htmls(templated_soup, list_of_htmls)

    with open(".build/output/templated_" + "main.html", "w") as file:
        print("\nWriting " + ".build/output/templated_" + "main.html")
        file.write(str(templated_soup))

    print("\nCopying figures, css, and pdf to ./build/output ")
    # Copy figure files to the ./output/ directory
    if os.path.exists(".build/output/figures"):
        shutil.rmtree(".build/output/figures")
    
    if os.path.exists(".build/latex/figures"):
        shutil.copytree(".build/latex/figures", ".build/output/figures")
    
    # Copy css into .build/output/
    shutil.copy(css, '.build/output')

    # Copy the latex compiled pdf into .build/output 
    shutil.copy('.build/latex/main.pdf', '.build/output')


if __name__ == "__main__":
    print(figlet_format("run.py"))

    # Check if path to latex dir was given
    if len(sys.argv) < 2:
        print("texedbook requires path to latex project directory")
        exit()
    latex_dir = os.path.join(sys.argv[1], '*')

    # Initialize .build/
    print("Initializing .build/")
    if os.path.exists('.build'):
        os.system('rm -r .build')
    os.system('mkdir .build')
    os.system('mkdir .build/latex')
    print("Copying " + latex_dir + " into .build/latex/")
    os.system('rsync -rv --exclude=.git ' + latex_dir + ' .build/latex' )

    # Clean up .tex files with vim regular expressions
    tex_files = glob.glob(os.path.join('.build', 'latex', '*.tex'))
    for tex_file in tex_files:
        os.system('vim -s aux/vim-cmds ' + tex_file)

    # Build the latex project, run tex4ebook, and run make-texedbook.py
    print(figlet_format("tex4ebook"))
    os.system(
        '''
        source venv/bin/activate
        cd .build/latex
        tex4ebook -c ../../aux/config.cfg main.tex
        cd ../..
        ''')
    print(figlet_format("make-texedbook.py"))

    template_ebook(".build/latex/main-epub/main.epub", 
                    "./templates/sidebar_element.html",
                    "./templates/sidebar.html", 
                    "./templates/template.html", 
                    "./templates/custom.css")
    
    print(figlet_format("texedbook \n build complete"))
