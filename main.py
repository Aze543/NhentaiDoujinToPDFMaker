import img2pdf # type: ignore
import requests
from typing import NoReturn
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import sys
import time
import threading
from math import trunc
from pathlib import Path

nhpdf_dir = Path.home()/"Documents"/"nhpdf"
nhpdf_dir.mkdir(parents=True, exist_ok=True) 

logo = """
.##..##..##..##..######..##..##..######...####...######.                        
.###.##..##..##..##......###.##....##....##..##....##...                        
.##.###..######..####....##.###....##....######....##...                        
.##..##..##..##..##......##..##....##....##..##....##...                        
.##..##..##..##..######..##..##....##....##..##..######.                        
........................................................                        
.#####....####...##..##..######..######..##..##..........######...####..........
.##..##..##..##..##..##......##....##....###.##............##....##..##.........
.##..##..##..##..##..##......##....##....##.###..######....##....##..##..######.
.##..##..##..##..##..##..##..##....##....##..##............##....##..##.........
.#####....####....####....####...######..##..##............##.....####..........
................................................................................
.#####...#####...######..........##...##...####...##..##..######..#####..       
.##..##..##..##..##..............###.###..##..##..##.##...##......##..##.       
.#####...##..##..####............##.#.##..######..####....####....#####..       
.##......##..##..##..............##...##..##..##..##.##...##......##..##.       
.##......#####...##..............##...##..##..##..##..##..######..##..##.       
.........................................................................         
"""

def loading_animation() -> NoReturn:
    global la, pages, page
    spinner = ['|', '/', '-', '\\']
    while not la:
        for frame in spinner:
            sys.stdout.write(f'\rDownloading the pages ({trunc(((page-1)/pages)*100)}%/{100}%)...{frame}')
            sys.stdout.flush()
            time.sleep(0.1)
            if la:  
                sys.stdout.write(f'\rDownloading the pages (100%/100%)...{frame}')
                sys.stdout.flush()
                break


def download_image(raw_url: str) -> bytes:
    global pages, page
    page += 1
    img_code, f_type = re.search(r'/(\d+)', raw_url['data-src']).group(), re.search(r'\b(.(jpg|jpeg|png|webp|gif|tiff|svg))\b', raw_url['data-src']).group()
    url = f'https://i3.nhentai.net/galleries{img_code}/{page}{f_type}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None

def compile_images(raw: list, name: str) -> NoReturn:
    with ThreadPoolExecutor(max_workers=10) as executor:
        raw_images = list(executor.map(download_image, raw))
    nhpdf = nhpdf_dir/f"{name}.pdf"
    with open(nhpdf, "wb") as file:
        file.write(img2pdf.convert(raw_images))


def main(on):
    global la, page, pages
    print(f"{logo}\n")
    while on:
        la = False
        page = 0
        try: 
            code = int(input("\nType the code(IYKYK): "))
        except Exception:
            print("\nThe code needs to be numbers (Ex: 177013) :) \n")
            continue
        url = f'https://nhentai.net/g/{code}/'
        response = requests.get(url)
        try: 
            soup = BeautifulSoup(response.text, "html.parser")
            pages = len(soup.find_all(class_='gallerythumb'))
            name = soup.find(class_='pretty').text
            author = soup.find(class_='before').text
            raw_data = soup.find_all(class_='lazyload')
            if not author:
                author = '[NAME-MISSING]: They forgot to put the author name in the website.'
        except Exception:
            print("\n[ERROR]: The code cannot be found in the website.\n")
            continue
        print(f"\nH-Doujin Details:\nname: {name}\nauthor: {author}\npages: {pages}\n")
        raw_data.remove(raw_data[0])
        function_thread = threading.Thread(target=loading_animation)
        function_thread.start()
        compile_images(raw_data[:pages], name)
        la = True
        function_thread.join()
        print(f"\n\nOperation was success, the file was saved into the same directory.")
        user_response = input("\nstill need then app to create another pdf (Y or N)?\n").lower()
        if not user_response == 'y' or user_response == 'yes':
            print("Exiting.....")
            on = False

if __name__ == "__main__":
    main(on=True)
