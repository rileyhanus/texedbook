from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from jinja2 import Template

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

def calchub_insert_iframe(soup):
    divs = soup.find_all(class_="calchub")
    if len(divs)==1:
        print("Inserting calchub iframe...")
        href = divs[0].find_all("a")[0]['href']
        text = divs[0].find_all("a")[0].text
        iframe_html = '<p>' + text + '</p> <iframe width="100%" height="500" src="' + href + '"></iframe>'
        divs[0].clear()
        divs[0].append(BeautifulSoup(iframe_html, "html.parser"))
    if len(divs)>1:
        print("ERORR: too many hrefs in calchub div.")


def template_ebook(book_epub, sidebar_element_html, sidebar_html, template_html):
    print("Reading .epub file and building an Epub object...")
    book = epub.read_epub(book_epub)

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

    focus_display_options = 'bg-gray-100 text-gray-900'
    standard_display_options = 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'

    print("Constructing TOC list based on .ncx content...")
    toc_list = toc_loop(book.toc)

    print("\n Looping through Epub Document Items...")
    i=0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            print("\n Templating Document " + str(i) + "...")
            sidebar_content = ''
            j=0
            print("Building Sidebar...")
            for element in toc_list:
                if element[2] == 0:
                    j=j+1
                if i == j:
                    display_options = focus_display_options
                else:
                    display_options = standard_display_options
                sidebar_content = sidebar_content + template_sidebar_element.render(sidebar_element_href="templated_" + element[1], sidebar_element_title=element[0], display_options=display_options) + '\n'
            sidebar = template_sidebar.render(sidebar_content=sidebar_content)

            print("Extracting body...")
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            calchub_insert_iframe(soup)
            body = soup.body
            print("Templating page and writing templated html...")
            templated_html = template_body.render(sidebar=sidebar, body=body)
            
            with open("templated_" + item.get_name(), "w") as file:
                file.write(templated_html)
            i=i+1


template_ebook('./main-epub/main.epub', "sidebar_element.html", "sidebar.html", "template.html")





