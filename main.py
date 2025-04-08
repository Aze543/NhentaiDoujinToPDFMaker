import img2pdf # type: ignore
import requests
from typing import NoReturn
from bs4 import BeautifulSoup
import re
import sys
import time
import threading

on = True
la = False
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
    global la
    spinner = ['|', '/', '-', '\\']
    while not la:
        for frame in spinner:
            sys.stdout.write(f'\rLet the magic work... {frame}')
            sys.stdout.flush()
            time.sleep(0.1)
            if la:  
                sys.stdout.flush()
                break
    sys.stdout.write('\rLet the magic work...   ')  
    sys.stdout.flush()

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
    raw_images = []
    for url in urls:
        response = requests.get(url)
        raw_images.append(response.content)
    with open(f"{name}.pdf", "wb") as file:
        file.write(img2pdf.convert(raw_images))

def main(on):
    global la
    print(f"{logo}\n\n")
    while on:
        try: 
            code = int(input("Type the code(IYKYK): "))
        except Exception as e:
            print("\nThe code needs to be numbers (Ex: 177013) :) \n")
            continue
        url = f'https://nhentai.net/g/{code}/'
        response = requests.get(url)
        try: 
            soup = BeautifulSoup(response.text, "html.parser")
            pages = len(soup.find_all(class_='gallerythumb'))
            name = soup.find(class_='pretty').text
            raw_data = soup.find_all(class_='lazyload')
        except Exception as e:
            print("\n[ERROR]: The code cannot be found in the website.\n")
            continue
        function_thread = threading.Thread(target=loading_animation)
        function_thread.start()
        url_images = get_images(raw_data, pages)
        compile_images(url_images, name)
        la = True
        function_thread.join()
        print(f"\nThe Operation was success, the file was saved into '{name}.pdf'")
        user_response = input("\nstill need then app to create another pdf(Y or N)?\n").lower()
        if not user_response == 'y' or user_response == 'yes':
            print("Exiting.....")
            on = False

if __name__ == "__main__":
    main(on)
