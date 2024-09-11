import os
import pyautogui
from time import sleep
from PIL import Image
import pyscreeze
import requests
from bs4 import BeautifulSoup

def web_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img')
    image_urls = [image['src'] for image in images if 'http' in image['src']]
    return image_urls

def download_image(url, chapter, page):
    response = requests.get(url)
    img_name = f'chapter_{chapter}_page_{page}.jpg'
    print(page)
    with open(img_name, 'wb') as f:
        f.write(response.content)
    return os.path.getsize(img_name)  # Return the size of the downloaded image

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def convert_images_to_cbz(folder_name):
    import zipfile
    with zipfile.ZipFile(f'{folder_name}.cbz', 'w') as cbz:
        for filename in os.listdir(folder_name):
            cbz.write(f'{folder_name}/{filename}', filename)

def save_images_to_folder(image_urls, folder_name, chapter, convert_to_cbz=True):
    create_folder(folder_name)
    chapter_size = 0
    for page_number, url in enumerate(image_urls, 1):
        try:
            img_size = download_image(url, chapter, page_number)
            chapter_size += img_size
            os.rename(f'chapter_{chapter}_page_{page_number}.jpg', f'{folder_name}/chapter_{chapter}_page_{page_number}.jpg')
        except Exception as e:
            print(f"Failed to download image: {page_number} in chapter: {chapter} - {e}")

    print(f"Total size for chapter {chapter}: {chapter_size / (1024 * 1024):.2f} MB")  # Print size in MB

    if convert_to_cbz:
        convert_images_to_cbz(folder_name)
    
    return chapter_size

def ai_mode(folder_name='D:/batcave/my labo/soloLeveling/from'):
    pyautogui.hotkey('win', '7')
    sleep(1)

    screen_width, screen_height = pyautogui.size()

    # Calculate the middle of the screen
    middle_x = screen_width // 2
    middle_y = screen_height // 2

    # Click at the middle of the screen
    pyautogui.click(middle_x, middle_y)
    sleep(1.5)
    pyautogui.hotkey('ctrl', 'l')
    sleep(0.5)
    pyautogui.typewrite(folder_name)
    sleep(0.5)
    pyautogui.press('enter')
    sleep(0.5)
    pyautogui.click(middle_x, middle_y)
    sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    sleep(0.5)
    pyautogui.press('enter')
    sleep(0.5)
    # Load the image
    image_path = 'start.png'

    # Find the coordinates of the image on the screen
    sleep(1.5)
    image_location = pyautogui.locateOnScreen(image_path, minSearchTime=3, confidence=0.6)
    if image_location:
        # Get the center of the found image
        center_x, center_y = pyautogui.center(image_location)
        
        # Click on the center of the image
        pyautogui.click(center_x, center_y)
    else:
        print("Image not found on the screen.")

min_page = 1
max_page = 21
#convert_to_cbz = False

#total_size = 0

#pages = range(int(min_page), int(max_page + 1))
#for page in pages:
    #print("Starting chapter", page)
    #url = f'https://w1.sololevelingthemanga.com/manga/solo-leveling-chapter-{page}/'
    #image_urls = web_scrape(url)
    #chapter_size = save_images_to_folder(image_urls, f'from {min_page} to {max_page}', page, convert_to_cbz)
    #total_size += chapter_size
#
#print(f"Total size for all chapters: {total_size / (1024 * 1024):.2f} MB")
#
#ai_mode(f'D:/batcave/my_labo/soloLeveling/from {min_page} to {max_page}')

convert_images_to_cbz(f"high_1_to_21")

