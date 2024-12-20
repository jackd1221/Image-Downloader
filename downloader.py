import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL of the website
URL = "https://www.ifishillinois.org/species/species.html"

# Custom folder name
SAVE_DIR_NAME = "Fish_Images"

def fetch_html(url):
    """Fetch HTML content of a given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch URL: {url}. Status code: {response.status_code}")

def parse_images(html, base_url):
    """Parse and extract image URLs from the HTML."""
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all("img")
    img_urls = []

    for img in img_tags:
        src = img.get("src")
        if src:
            # Resolve relative URLs to absolute ones
            full_url = urljoin(base_url, src)
            # Filter for likely fish-related images (optional based on naming patterns)
            if "fish" in full_url.lower():
                img_urls.append(full_url)
    return img_urls

def download_images(image_urls, save_dir_name):
    """Download images to the specified directory."""
    save_dir = os.path.join(os.getcwd(), save_dir_name)
    os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist

    for idx, img_url in enumerate(image_urls):
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            # Generate a filename for the image
            file_extension = img_url.split(".")[-1]  # Get the file extension
            file_name = os.path.join(save_dir, f"fish_image_{idx + 1}.{file_extension}")
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

def main():
    print("Fetching webpage...")
    html_content = fetch_html(URL)
    print("Parsing image URLs...")
    image_urls = parse_images(html_content, URL)
    print(f"Found {len(image_urls)} images. Downloading...")
    if image_urls:
        download_images(image_urls, SAVE_DIR_NAME)
        print(f"All images downloaded to the '{SAVE_DIR_NAME}' folder in the current directory.")
    else:
        print("No fish images were found.")

if __name__ == "__main__":
    main()