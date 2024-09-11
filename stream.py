import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import streamlit as st
import zipfile
import io
import re

data = {"berserk": "https://theberserk.online/manga/berserk-chapter-0-0"}
st.table(data)
url = st.text_input("URL to download")
if url != "" and url[-1] == '/': 
    url = url[:-1]

anime_name = st.text_input("anime name")

#id = st.checkbox("id")
#href = st.checkbox("href")
#decoding = st.checkbox("decoding")
#title = st.checkbox("title")
def web_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = soup.find_all('img', src = True)

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

import zipfile

def convert_images_to_cbz(folder_name):
    with zipfile.ZipFile(f'{folder_name}.cbz', 'w') as cbz:
        filenames = sort_filenames(os.listdir(folder_name))
        print(filenames)
        for filename in filenames:
            cbz.write(os.path.join(folder_name, filename), filename)

def sort_filenames(filenames):
    def extract_number(filename):
        match = re.search(r'page_(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    return sorted(filenames, key=extract_number)

def save_images_to_folder(image_urls, folder_name, chapter, convert_to_cbz=True):
    create_folder(folder_name)
    num_images = len(image_urls)
    chapter_size = 0
    progress_bar = st.progress(0, text=f"Downloading images for Chapter {chapter}")
    for page_number, url in enumerate(image_urls, 1):
        try:
            img_size = download_image(url, chapter, page_number)
            chapter_size += img_size
            os.rename(f'chapter_{chapter}_page_{page_number}.jpg', f'{folder_name}/chapter_{chapter}_page_{page_number}.jpg')
        except Exception as e:
            print(f"Failed to download image: {page_number} in chapter: {chapter} - {e}")
        progress = (page_number / num_images) * 100
        progress_bar.progress(int(progress), text=f"Downloading image {page_number}/{num_images} with size {chapter_size / (1024 * 1024):.2f} MB")


    st.write(f"Total size for chapter {chapter}: {chapter_size / (1024 * 1024):.2f} MB")  # Print size in MB

    if convert_to_cbz:
        convert_images_to_cbz(folder_name)
    
    return chapter_size


min_page = st.number_input("minimum",min_value=0)
max_page = st.number_input("maximum",min_value=0)
convert_to_cbz = True

st.title("Download Images as CBZ")
submit_button = st.button("Create cbz file and download")
st.title("Download Images as ZIP")
submit_zip =  st.button("Create ZIP and Download")


total_size = 0

pages = range(int(min_page), int(max_page + 1))
output_path = f"from_{min_page}_to_{max_page}_{anime_name}"

if submit_button:
    for page in pages:
        print("Starting chapter", page)
        ch_url = url + f'{page}/'
        image_urls = web_scrape(ch_url)
        chapter_size = save_images_to_folder(image_urls, f'from_{min_page}_to_{max_page}_{anime_name}', page, convert_to_cbz)
        total_size += chapter_size

    if convert_to_cbz:
        convert_images_to_cbz(output_path)
        if os.path.exists(output_path):
            with open(output_path+".cbz", "rb") as file:
                st.download_button(
                    label="Download CBZ",
                    data=file,
                    file_name=output_path+anime_name+'.cbz',
                    mime="application/x-cbz"
                )
        else:
            st.error("The file was not generated. Please try again.")

if submit_zip:
    def create_zip_from_folder(folder_path):
        # Create a BytesIO object to hold the ZIP file in memory
        buffer = io.BytesIO()
        
        # Create a ZIP file in memory
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zip_file.write(file_path, arcname)
        
        buffer.seek(0)  # Move to the beginning of the BytesIO object
        return buffer
    # Streamlit app code
    st.title("Download Images as ZIP")

    # Get user input for folder path (use a placeholder or a specific folder path)
    folder_path = output_path  # Replace this with the actual path

    # Create a ZIP file from the folder
    zip_buffer = create_zip_from_folder(folder_path)
    
    # Provide the download button
    st.download_button(
        label="Download ZIP",
        data=zip_buffer,
        file_name="images.zip",
        mime="application/zip"
    )
