import requests
import json
import urllib


name =  "Black Lotus"
parsed = urllib.parse.quote(name)


url = "https://www.ligamagic.com.br/?view=cards/card&card=" + parsed
r = requests.get(url)

print("Procurando preço da carta: " + name)

data = r.text
pos1 = data.find("var g_avgprice=")
pos2 = data.find(";",pos1)
#print(data[pos1+16:pos2-1])
range = data[pos1+16:pos2-1]
json_data = json.loads(range)
for key in json_data.keys():
    pos1 = data.find(f"<option value='{key}'>")
    pos2 = data.find("<", pos1+1)
    setName= data[pos1+16+len(key)+1:pos2]
    preco = json_data[key]["precoMenor"]
    print(f"{setName}: R${preco:.2f}")