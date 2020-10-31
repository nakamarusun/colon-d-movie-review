import requests
from bs4 import BeautifulSoup
import re

# Function to find nth occurence in a string.
def findnth(string, substring, occurence):
    val = -1
    for i in range(occurence):
        val = string.find(substring, val + 1)

    return val

def scrape_g_image(query, small_image=False):
    """
    Scrapes google image by searching with the inputted query.
    Will return one image link / base64 image based on the result.
    If it fails, will return None.

    params:

    :query, string of text that wanted to be searched.

    :small_image, whether to return a really tiny image or a small image.
    """
    # Here we can adjust what mode we want to retrieve the image.
    # If small_image is true, we get all the image based on their very small
    # thumbnail from google, and the user have to load the links individually.
    # If it is false, then the image got will be higher quality, and the user does
    # not have to load the link individually.
    if small_image:
        html = requests.get('https://www.google.com/search?q={}&tbm=isch'.format(query)).text
        bp = BeautifulSoup(html, 'html.parser')
        img = bp.find_all('img')
        
        return img[1].get('src')
    
    else:
        # The header is there so that as if a windows computer is accessing the website.
        # This will provide a different response from small_image=True.

        html = requests.get('https://www.google.com/search?q={}&tbm=isch'.format(query), headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0", "Accept": "image/webp,*/*"
            }).text

        # Defines a RegEx pattern in which the image is contained
        pattern = re.compile(r"_setImgSrc\('[0-9]+','[^']+'\)", re.MULTILINE)

        # Searches the text
        raw_data = pattern.search(html)

        if not raw_data:
            # Debugging purposes
            with open("failed.html", "wb+") as file:
                file.write(bytes(html, "utf-8"))
                print("Logged failed image parsing.")
            return None
        else:
            # Raw data
            img_str = raw_data.group()
            return img_str.replace("\\", "")[findnth(img_str, "'", 3) + 1:-2]