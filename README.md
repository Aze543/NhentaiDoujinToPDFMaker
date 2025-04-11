# NHENTAI DOUJIN-TO-PDF MAKER

---------------------------------------------------------------------------------

A disgusting python script that lets you compile a doujin from nhentai.net 
into a pdf for offline goon reading.

This application has two flavors:

FIRST:
a command-line version where you can use the command nhpdf to run the script

nhpdf <hdoujin-code>

SECOND:
a python script that needs to be run using the python or python3 command

python main.py
python3 main.py

The Instruction below is for the second flavor. I use MacOS, so the
instructions for windows might be not accurate but I tried my best :)

download link: https://github.com/Aze543/NhentaiDoujinToPDFMaker.git


---------------------------------------------------------------------------------

INSTURCTIONS for the First Flavor:

---------------------------------------------------------------------------------

1. You can either download the first flavor in the releases or download it using
the pip command

Win/MacOS: pip install nhpdf

* if you've downloaded it, you need to be in the same directory as the
pyproject.toml, then run the command

Win/MacOS: pip install .

2. enjoy the script, you can run it by typing the command

nhpdf <doujin-code>

Examples:
nhpdf 566212

it also works if you want to down multiple pdfs
nhpdf 566212 563102
   
---------------------------------------------------------------------------------

INSTURCTIONS for the Second Flavor:

Download the second flavor in the releases.

---------------------------------------------------------------------------------

1. install python to your system, look in the internet how

    to check if it works
    
    windows: open cmd >> type python >> hit enter
    
    mac: open terminal >> type python3 >> hit enter
    
    it should open the python

---------------------------------------------------------------------------------

2. install the requirements in 'requirements.txt'

    in the cmd or terminal, go into the directory of the file where
    the main.py and requirements.txt lives
    
    directory means folder
    
    to check if you're now in the directory
    
    windows: the command is dir to see the list of files in the directory
    
    mac: type ls
    
    finally, type this in the cmd or terminal: pip install -r 'requirements.txt'
    
    it should download the packages you need to make the script works

---------------------------------------------------------------------------------

3. last is run the program by typing:

    windows: python main.py
    
    mac: python3 main.py
    
    if you're greeted with the logo "NHENTAI DOUJIN-TO-PDF MAKER"
    in the cmd or terminal, you've successfully install and run the script 
    into your computer, Enjoy!

---------------------------------------------------------------------------------

HOW TO USE THE SCRIPT:

---------------------------------------------------------------------------------

type the code of the nhentai doujin you want, then let the magic work

the output will be in the same directory

Dev Note: This Script only works on nhentai.net

---------------------------------------------------------------------------------
