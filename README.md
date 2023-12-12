# texedbook

`tex`: Latex based. `ed`: Education focused. `book`: Classic textbook functionality maintained.

## Overview:
This is code base enables authors to publish latex based articles, educational content, and textbooks online without the need to learn html, css, and javascript. Most importantly, any website element (e.g. iframe or custom html element) can be embedded in the output html page directly from the latex code using custom commands provided in this package. The author compiles the publication in latex (using `latexmk`) following the conventions outlined in [Author's Guide to Textbook](./authors_guide/main.pdf), and then runs

`python make_texedbook.py ./path/to/latex/project/directory/`

which does the following.

1. Initializes the `.build/` directory
1. Compiles the latex project using the `latexmk` command (native to the full latex distibution)
1. Generates the required raw html and metadata using the `tex4ebook` command (also native to the full latex distribution) along with the `config.cfg` file provided here.
1. Templates the raw html into the `texedbook` html templates using the open source python packages `BeautifulSoup` and `jinga2`, among others.
1. Builds the webpage navigation (computer and mobile)
1. Sews up hyperlinks
1. Parses the latex project and templates in any custom html, or embed code that the author included.

## Set up texedbook:
Follow these steps to set up `texedbook` for use on your computer.

### Prerequisits:
1. Ensure you have a full Tex Live LaTex distribution installed. See [latex-project.org](https://www.latex-project.org/get/) . Basic or smaller latex distributions will not work. You will need the `latexmk` and `tex4ebook` commands to work in your terminal.

   - MacOS: Install MacTex using the .exe installer from the link above. (tested)

   - Linux: run the following commands in the terminal. (tested)

        `sudo apt update`

        `sudo apt install texlive-full`

   - Windows: Install using the TexLive installer (untested)

1. Ensure you have Python 3.8 (older versions may work too), venv, wheel, and pip installed. Wheel can be installed with 

    - `pip` comes with the standard Python 3 distribution so you should have it. If you don't have it you could try reinstalling Python 3.8 or newer from [python.org](https://www.python.org/)
    - `venv` also comes with the standard Python 3 distribution.
    - `wheel` can be installed with `pip install wheel`

### Download and installation:

1. Clone the repository to your computer and navigate into it by running the following in the terminal (you will need to have permissions)

    `git clone https://github.com/rileyhanus/texedbook.git`

    `cd texedbook`

1. Create a virtual environment to work in by running

    `python -m venv venv`

    `source venv/bin/activate`

1. Install required packages by running

    `pip install -r requirements.txt`

1. Test by running the following (htlatex will throw some benign errors which you can ignore)

    `python make_texedbook.py ./authors_guide`

1. View result by opening `./output/templated_main.html`


### Running texedbook
1. Make sure your main.tex document is finished and compiles without major errors using `latexmk`. 

1. Run texedbook

    `python make_texedbook.py ./path/to/latex/project/directory/`
`
 
1. Open `./output/templated_main.html` files to view the output webpage

    