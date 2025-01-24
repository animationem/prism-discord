import requests
import json
from PIL import Image
import os

from pprint import pprint

token = "MTMyNjMzNDUwNzg5MjA4NDgzOA.GF8A9q.I4wzPlDcrqBew3aRsTzdvfPksUIEEf3NIAEQA8"

#-----------------Get Guild ID -----------------
url = "https://discord.com/api/v10/users/@me/guilds"
headers = {"Authorization": f"Bot {token}"}

response = requests.get(url, headers=headers)

data = response.json()

for d in data:
    if d["name"] == "Prism for Discordo":
        guild_id = d["id"]

#-----------------Get Channel ID -----------------
url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
response = requests.get(url, headers=headers)
data = response.json()

for d in data:
 
    if d.get("name") == "Text Channels":
        t_id = d.get("id")
    
    if d.get("name") == "test" and d.get("parent_id") == t_id:
        channel_id = d.get("id")

print(f"Channel Name: Test Channel ID: {channel_id}")

#-----------------Send Message -----------------
url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
headers = {"Authorization": f"Bot {token}"}

#Prep File
file_path="C:/Users/jessi/OneDrive/Desktop/New folder/lodi2.jpg"
files = {'file': open(file_path, 'rb')}

with Image.open(file_path) as img:
    width, height = img.size


#Prep payload with an embed
payload = {
        "content": "hey", 
        "embeds": [
            {
                "title": folder_name, 
                "description": "ur cooked\nDimensions: {}x{}".format(width, height),
                "color": 16711680, 
                
            }
        ]
}

response = requests.post(url, headers=headers, files=files, data={"payload_json": json.dumps(payload)})
