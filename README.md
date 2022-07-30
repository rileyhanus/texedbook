# TexEdBook

## Overview:
This is a package that converts any latex project directly into an html-based learning environment which supports interactive digital content. All functions and environments native to latex are supported. In addition, multi-media content such as videos, embedded coding environments, and live math workspaces (powered by CalcHub) can be implimented directly in the latex code using custom environments provided in this package. Therefore, this package is backwards compatible with legacy educational content, and is also capable of supporting html-based interactive content moving forward. 

## Multi-media content:
Naturally, print and pdf formats do not support many multi-media formats that are desired in a digital learning environment (videos, math workspaces, problem sets and quizzes). When this type of content is included in the latex document, the pdf render simply provides a hyperlink to the url used to access the digital content is given. This is analogous to a print textbook containing a CD with digital content. When TexEdBook compiles the latex project into an interactive html-based learning environment, the multi-media content is imbedded into the web page and is fully functional.

## Packages used:
The input of this package is a latex document. If the document compiles with errors, these errors may propagate into the html pages generated. The package tex4ebook, which uses tex4ht internally, is used to generate a .epub file from the latex document. This .epub is essentially a zipped up folder containing an .ncx navigation file and a series of .html files associated with each section. tex4ebook uses an config.cfg file to designate configuration settings which control how certain latex features are converted to latex. The default usage of the config.cfg file requires all math content, both displayed and in-line math, to be rendered as svg files and place in the html code. The config.cfg file is also where we tell tex4ht how to handle custom environments. 

Within make_texedbook.py, ebooklib is used to parse the .epub file and build objects containing all of the content. Beautiful Soup 4 is used for some html parsing. Jinja2 is used for html templating. 

## Set up texedbook:
Follow these steps to set up your texedbook project.

### Prerequisits:
1. Ensure you have a full Tex Live LaTex distribution installed. See https://www.latex-project.org/get/ . Basic or smaller latex distributions will not work.

   - MacOS: Install MacTex using the .exe installer from the link above. (tested)

   - Linux: run the following commands in the terminal. (tested)

        `sudo apt update`

        `sudo apt install texlive-full`

   - Windows: Install using the TexLive installer (untested)

1. Ensure you have python 3.8 (older versions may work too), venv, wheel, and pip installed. Wheel can be installed with 

    `pip install wheel`

### Download and installation:

1. Clone the repository to your computer and navigate into it by running (you will need to have permissions)

    `git clone https://github.com/rileyhanus/texedbook.git`

    `cd texedbook`

1. Create a virtual environment to work in by running

    `python3 -m venv venv`

    `source venv/bin/activate`

1. Install required packages by running

    `pip install -r requirements.txt`

1. Make sure your main.tex document is finished and compiles without errors.  To Compile main.tex, I recommend using VSCode with the 'Tex Workshop' plugin installed. In VSCode you can compile by simply saving any .tex file in your project.

1. Make sure every figure.pdf has a corresponding figure.xbb by executing the following in the terminal. 

    `cd ./latex`

    `ebb -x *.pdf`

1. Create your main.epub file along with the corresponding .html files for all the Chapters by running the following command in the terminal.

    `tex4ebook -c config.cfg main.tex`

1. Extract the html and navigation meta-data, and template the content onto template.html which renders the interactive learning environment.
    
    `cd ../`

    `python3 make_texedbook.py`
 
1. Open an of the the templated html files to view the html-based learning environment.


## Editing your project:

After making changes to any of your .tex files run step 6 and 7 from "Set up your project" and the .html files will be updated. If you add a new pdf figure you will need to run step 5 as well.


## Quirks

1. Since equations and equation referenceing in TexEdBook is done with Mathjax, and each chapter is compiled into its own htlm page, references can only be made to equation within the chapter. For example, if you label an equation in Chapter 1 

    `/label{eq:ch1-equation}`

    this can only be referenced using 

    `/mjref{eq:ch1-equation}` 

    within Chapter 1. It will through '???' in the rendered html if that same mjref is used in Chapter 2.

    To reference equations between Chapters, you might consider referencing the section/subsection the equation is contained in (to provide a hyperlink), and explicitly stating the equation/variable of interest.

