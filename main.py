import img2pdf # type: ignore
import requests
from typing import NoReturn
from bs4 import BeautifulSoup
import re
import sys
import time
import threading


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

def loading_animation():
    global la, pages, page_num
    spinner = ['|', '/', '-', '\\']
    while not la:
        for frame in spinner:
            sys.stdout.write(f'\rDownloading the pages ({page_num}/{pages})...{frame}')
            sys.stdout.flush()
            time.sleep(0.1)
            if la:  
                break

def get_images(raw: list, pages: int) -> list:
    imgs= []
    page = 1
    for item in raw:
        img_code, f_type = re.search(r'/(\d+)', item['data-src']).group(), re.search(r'\.([a-zA-Z0-9]+)$', item['data-src']).group()
        imgs.append(f'https://i3.nhentai.net/galleries{img_code}/{page}{f_type}')
        page += 1
        if page > pages:
            return imgs
        
def compile_images(urls: list, name: str) -> NoReturn:
    global page_num
    raw_images = []
    for url in urls:
        page_num += 1
        response = requests.get(url)
        raw_images.append(response.content)
        sys.stdout.flush()
    with open(f"{name}.pdf", "wb") as file:
        file.write(img2pdf.convert(raw_images))

def main(on):
    global la, page_num, pages
    print(f"{logo}\n")
    while on:
        la = False
        page_num = 0
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
        url_images = get_images(raw_data, pages)
        print(f"\nH-Doujin Details:\nname: {name}\nauthor: {author}\npages: {pages}\n")

        function_thread = threading.Thread(target=loading_animation)
        function_thread.start()
        compile_images(url_images, name)
        la = True
        function_thread.join()
        print(f"\n\nOperation was success, the file was saved into the same directory.")
        user_response = input("\nstill need then app to create another pdf (Y or N)?\n").lower()
        if not user_response == 'y' or user_response == 'yes':
            print("Exiting.....")
            on = False

if __name__ == "__main__":
    main(on=True)
