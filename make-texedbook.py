from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from jinja2 import Template
from urllib.parse import urlparse
import os as os
import shutil
import glob
import sys

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

def calchub_insert_iframe(soup, full_page=False, height="800"):
    divs = soup.find_all(class_="calchub")
    for div in divs:
        print("Inserting calchub iframe...")
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
        print("Inserting youtube iframe...")
        href = div.find_all("a")[0]['href']
        parsed_href = urlparse(href)
        query = parsed_href.query
        video_code = query.split('=')[1]
        parsed_href = parsed_href._replace(path='embed/' + video_code, query='')
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe width="'+ width + '" height="' + height + '" src="' + parsed_href.geturl() + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))



def trinket_insert_iframe(soup, width="100%", height="500"):
    divs = soup.find_all(class_="trinket")
    for div in divs:
        print("Inserting trinket iframe...")
        href = div.find_all("a")[0]['href']
        print(href)
        # parsed_href = urlparse(href)
        # print(parsed_href)
        # path = parsed_href.path
        # trinket_code = path.split('/')[-1]
        # print(trinket_code)
        # parsed_href = parsed_href._replace(path='embed/' + video_code, query='')
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe src="' + href + '" width="' + width + '" height="' + height + '" frameborder="0" marginwidth="0" marginheight="0" allowfullscreen></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))


def panopto_insert_iframe(soup, width="560", height="315"):
    divs = soup.find_all(class_="panopto")
    for div in divs:
        print("Inserting panopto iframe...")
        href = div.find_all("a")[0]['href']
        href_embed = href.replace("Viewer", "Embed")
        text = div.find_all("a")[0].parent.text
        iframe_html = '<p>' + text + '</p>  <iframe width="'+ width + '" height="' + height + '" src="' + href_embed + '"></iframe>'
        div.clear()
        div.append(BeautifulSoup(iframe_html, "html.parser"))


def clean_html(soup):
    soup = str(soup)
    # soup = soup.encode('unicode_escape')
    soup = soup.replace(r"\relax", r"")
    return BeautifulSoup(soup, features="lxml")


def template_ebook(book_epub, sidebar_element_html, sidebar_html, template_html, css, one_page=False):
    print("Remaking .build/")
    target = os.path.join('.build', 'output')
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    
    print("Reading .epub file and building an Epub object...")
    book = epub.read_epub(book_epub)
    print("\n  Book Title: " + book.title + "\n")
    print(book.get_metadata("DC", "creator"))

    print("Opening html templates and building Template objects...")
    with open(sidebar_element_html, "r", encoding='utf-8') as f:
        sidebar_element_template = f.read()
    with open(sidebar_html, "r", encoding='utf-8') as f:
        sidebar_template = f.read()
    with open(template_html, "r", encoding='utf-8') as f:
        body_template = f.read()
    template_sidebar_element = Template(sidebar_element_template)
    template_sidebar = Template(sidebar_template)
    template_body = Template(body_template)

    focus_display_options = 'bg-gray-200 text-gray-900 hover:text-gray-600'
    standard_display_options = 'bg-gray-75 text-gray-600 hover:bg-gray-200 hover:text-gray-900'
    sidebar_font_sizes = [' text-md font-bold ', ' text-sm font-bold ', ' text-xs ', ' text-xs ', ' text-xs ', ' text-xs ']

    print("Constructing TOC list based on .ncx content...")
    toc_list = toc_loop(book.toc)
    # print(toc_list)
    item_name_list = [row[1].split('#')[0] for row in toc_list]

    focus_list = []
    focus_counter=0
    for element in toc_list:
        if element[2] == 0:
            focus_counter=focus_counter+1
        focus_list.append(focus_counter)
    # Getting a list of document names
    document_item_list = book.get_items()
    document_name_list = []
    for item in document_item_list:
        document_name_list.append(item.get_name())

    if one_page:
        print('Make title page template_main.html...')
        title_page_html = book.get_item_with_href("main.html").get_content()
        soup = BeautifulSoup(title_page_html, 'html.parser')
        body = soup.body
        sidebar_content = ''
        for element in toc_list:
            display_options = standard_display_options
            sidebar_content = sidebar_content + template_sidebar_element.render(sidebar_element_href="templated_main.html#" + element[1].split('#')[1],  
                                                                                sidebar_element_title=element[0], 
                                                                                display_options=display_options + sidebar_font_sizes[element[2]] + " px-" + str(4+4*element[2])) + '\n'
            sidebar = template_sidebar.render(sidebar_content=sidebar_content, standard_display_options=standard_display_options + sidebar_font_sizes[0] + " px-" + str(4+4*0)) + '\n'
        templated_html = template_body.render(title=book.title, sidebar=sidebar, body=body, standard_display_options=standard_display_options + sidebar_font_sizes[0] + " px-" + str(4+4*0)) + '\n'
        templated_soup = BeautifulSoup(templated_html, 'html.parser')
        
        print("\nLooping through Epub Document Items and appending body to main.html...")
        for item in book.get_items():
            if item.get_name() in item_name_list:
                print("Extracting body...")
                new_content = item.get_content()
                new_soup = BeautifulSoup(new_content, 'html.parser')
                # fixing hrefs such that they point to templated_xxx.html instead of xxx.html
                a_tags = new_soup.body.find_all("a", href=True) 
                for a_tag in a_tags:
                    href = a_tag['href']
                    for document_name in document_name_list:
                        if document_name in href:
                            href = href.replace(document_name, "templated_main.html")
                            a_tag['href'] = href
                calchub_insert_iframe(new_soup)
                youtube_insert_iframe(new_soup)
                trinket_insert_iframe(new_soup)
                panopto_insert_iframe(new_soup)
                new_soup = clean_html(new_soup)
                new_body_html = new_soup.find('body').findChildren(recursive=False)
                for i in range(len(new_body_html)):
                    templated_soup.body.append(new_body_html[i])
        with open(".build/output/templated_" + "main.html", "w") as file:
            file.write(str(templated_soup))
    else:  
        print('Make title page template_main.html...')
        title_page_html = book.get_item_with_href("main.html").get_content()
        soup = BeautifulSoup(title_page_html, 'html.parser')
        body = soup.body
        sidebar_content = ''
        for element in toc_list:
            display_options = standard_display_options
            sidebar_content = sidebar_content + template_sidebar_element.render(sidebar_element_href="templated_" + element[1],  sidebar_element_title=element[0], display_options=display_options + sidebar_font_sizes[element[2]] + " px-" + str(4+4*element[2])) + '\n'
            sidebar = template_sidebar.render(sidebar_content=sidebar_content)
        templated_html = template_body.render(title=book.title, sidebar=sidebar, body=body)
        with open(".build/output/templated_" + "main.html", "w") as file:
            file.write(templated_html)
        shutil.copy(css, '.build/output')
        
        print("\nLooping through Epub Document Items...")
        for item in book.get_items():
            if item.get_name() in item_name_list:
                document_name = item.get_name()
                print("\nDocument " + document_name + " ...")
                sidebar_content = ''
                print("Building Sidebar...")
                for element in toc_list:
                    print(element)
                    if document_name == element[1].split('#')[0]:
                        display_options = focus_display_options
                    else:
                        display_options = standard_display_options
                    sidebar_content = sidebar_content + template_sidebar_element.render(sidebar_element_href="templated_" + element[1],  sidebar_element_title=element[0], display_options=display_options + sidebar_font_sizes[element[2]] + " px-" + str(4+4*element[2])) + '\n'
                sidebar = template_sidebar.render(sidebar_content=sidebar_content)

                print("Extracting body...")
                content = item.get_content()
                soup = BeautifulSoup(content, 'html.parser')
                calchub_insert_iframe(soup)
                youtube_insert_iframe(soup)
                trinket_insert_iframe(soup)
                panopto_insert_iframe(soup)
                soup = clean_html(soup)
                body = soup.body
                
                # fixing hrefs such that they point to templated_xxx.html instead of xxx.html
                a_tags = body.find_all("a", href=True) 
                for a_tag in a_tags:
                    href = a_tag['href']
                    for document_name in document_name_list:
                        if document_name in href:
                            href = href.replace(document_name, "templated_" + document_name)
                            a_tag['href'] = href
                            
                print("Templating page and writing templated html...")
                templated_html = template_body.render(title=book.title, sidebar=sidebar, body=body)
                with open(".build/output/templated_" + item.get_name(), "w") as file:
                    file.write(templated_html)

    # copy figure files to the ./output/ directory
    if os.path.exists(".build/output/figures"):
        shutil.rmtree(".build/output/figures")
    
    if os.path.exists(".build/latex/figures"):
        shutil.copytree(".build/latex/figures", ".build/output/figures")
    # svg_sources = glob.glob(os.path.join('.', 'latex', '*.svg'))
    # png_sources = glob.glob(os.path.join('.', 'latex', '*.png'))
    # pdf_sources = glob.glob(os.path.join('.', 'latex', '*.pdf'))
    # try:
    #     for source in svg_sources:
    #         shutil.copy(source, target)
    #     for source in png_sources:
    #         shutil.copy(source, target)
    #     for source in pdf_sources:
    #         shutil.copy(source, target)
    # except IOError as e:
    #     print("Unable to copy file. %s" % e)
    # except:
    #     print("Unexpected error:", sys.exc_info())

    # copy the required .css file to the .build/output directory
    shutil.copy(css, '.build/output')
    shutil.copy('.build/latex/main.pdf', '.build/output')



template_ebook(".build/latex/main-epub/main.epub", 
               "./templates/sidebar_element.html",
               "./templates/sidebar.html", 
               "./templates/template.html", 
               "./templates/custom.css", 
               one_page=True)
