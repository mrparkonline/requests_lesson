# External Import
import requests

# Internal Import
import os
import json

# 1. Create our learning data
# Create folders for our non-terriers and terriers
def directoryExists(dir_path):
    return os.path.exists(dir_path)

def checkPath():
    result = False
    non_terrier_path = "./db/nonterrier/"
    if directoryExists(non_terrier_path):
        print("Non-terrier DB exists")
        result = True
    else:
        os.makedirs(non_terrier_path)
        print("Non-terrier DB made.")

    terrier_path = "./db/terrier/"
    if directoryExists(terrier_path):
        print("Terrier DB exists")
        result = result and True
    else:
        os.makedirs(terrier_path)
        print("Terrier DB made.")
        result = False
    
    return result
# end of checkPath()

#2. Get all dog breed names
non_terriers = []
terriers = []
MAIN_URL = "https://dog.ceo/api/breeds/"
BREED_URL = "https://dog.ceo/api/breed/"

breed_list_url = "list/all"
response = requests.get(MAIN_URL + breed_list_url)

if response.status_code == 200:
    data = response.json()
    breed_table = data['message']
    
    for key, value in breed_table.items():
        if key == 'terrier':
            for terrier_type in value:
                terriers.append(f"{key}/{terrier_type}")
        else:
            if not value:
                non_terriers.append(key)
            else:
                for breed in value:
                    non_terriers.append(f"{key}/{breed}")
    print('Terriers:' , terriers)
    print('Non Terriers', non_terriers)
else:
    print("Failed to get dog breed lists")

#3. Get All Terrier Pictures
counter = 0
file_path = './db/terrier/'
for terrier in terriers:
    url = f"{BREED_URL}{terrier}/images"
    response = requests.get(url) # Get current terrier's img url list
    if response.status_code == 200:
        data = response.json()
        img_urls = data['message'] # per img url, download the file
        for url in img_urls:
            counter += 1
            current_path = f"{file_path}{counter}.jpg"
            img_response = requests.get(url)
            with open(current_path, 'wb') as f:
                f.write(img_response.content)
        print(f"{terrier} download complete")
    else:
        print("Failed to download image")
