TexEdBook

Overview:
This is a package that converts any latex project directly into an html-based learning environment which supports interactive digital content. All functions and environments native to latex are supported. In addition, multi-media content such as videos and live math workspaces (powered by CalcHub) can be implimented directly in the latex code using custom environments. Therefore, this package is backwards compatible with legacy educational content, and is also capable of supporting html-based interactive content moving forward. 

Multi-media content:
Naturally, print and pdf formats do not support many multi-media products that are desired in a digital learning environment (videos, math workspaces, problem sets and quizes). In this case a hyperlink to the url used to access the digital content is given, analogous to a print textbook containing a CD with digital content. When TexEdBook compiles the latex project into an interactive html-based learning environment, the multi-media content is imbedded into the web page and is fully functional.

Packages used:
The input of this package is a latex document that compiles with no errors. The package tex4ebook, which uses tex4ht internally, is used to generate a .epub file from the latex document. This .epub is essentially a zipped up folder containing an .ncx navigation file and a series of .html files associated with each section. tex4ebook uses an config.cfg file to designate configuration settings which control how certain latex features are converted to latex. The default usage of the config.cfg file requires all math content, both displayed and in-line math, to be rendered as svg files and place in the html code. The config.cfg file is also where you will tell tex4ht how to handle custom environments. 

Within template.py, ebooklib is used to parse the .epub file and build objects containing all of the content. Beautiful soup 4 is used for some html parsing. Jinja2 is used for html templating. 


Set up your project:
Follow these steps to set up your texedbook project.

1. Clone the repository to your computer and navigate into it by running (you will need to have permissions)

git clone https://github.com/rileyhanus/texedbook.git
cd texedbook

2. Create a virtual environment to work in by running

python3 -m venv venv
source venv/bin/activate

3. Install required packages by running

pip install -r requirements.txt

4. Make sure your main.tex document is finished and compiles without errors.  To Compile main.tex, I recommend using VSCode with the 'Tex Workshop' plugin installed. You can compile by simply saving any .tex file.

5. Make sure every figure.pdf has a corresponding figure.xbb by executing the following in the terminal. 

ebb -x *.pdf

6. Create your main.epub file along with the corresponding .html files for all the Chapters by running the following command in the terminal.

tex4ebook -c config.cfg main.tex

7. Extract the html and navigation meta-data, and template the content onto template.html which renders the interactive learning environment.

tex4ebook -c config.cfg main.tex
python make_texedbook.py
 
8. Open an of the the templated html files to view the html-based learning environment.


Editing your project:

After making changes to any of your .tex files run step 6 and 7 from "Set up your project" and the .html files will be updated. If you add a new pdf figure you will need to run step 5 as well.

