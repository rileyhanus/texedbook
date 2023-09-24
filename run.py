import glob
import os
import sys

if len(sys.argv) < 2:
    print("texedbook requires path to latex project directory")
    exit()

latex_dir = os.path.join(sys.argv[1], '*')

if os.path.exists('.build'):
    os.system('rm -r .build')
os.system('mkdir .build')
os.system('mkdir .build/latex')
os.system('rsync -rv --exclude=.git ' + latex_dir + ' .build/latex' )

tex_files = glob.glob(os.path.join('.build', 'latex', '*.tex'))

for tex_file in tex_files:
    os.system('vim -s vim-cmds ' + tex_file)

os.system(
    '''
    source venv/bin/activate
    cd .build/latex
    ebb -x *.pdf
    tex4ebook -c ../../config.cfg main.tex
    cd ../..
    python3 make-texedbook.py
    '''
)
