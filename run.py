"""
    Copyright 2023 Riley Hanus, PhD
    Unauthorized copying and use of this file, via any medium is strictly prohibited
    Proprietary and confidential

    Written by Riley Hanus <hanusriley@gmail.com>, November 2023
"""

import glob
import os
import sys
from pyfiglet import figlet_format


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
os.system(
    '''
    python3 make-texedbook.py
    '''
)

print(figlet_format("build complete"))