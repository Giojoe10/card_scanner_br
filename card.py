import requests

class Card:
    def __init__(self, name:str):
        api_data = self.lookup(name)
        if not api_data:
            api_data = self.lookup("Bocarra Sinistra Colossal")
        self.name:str = api_data["name"]
        self.precos:dict = api_data["precos"]
        
        scryfall_data = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={self.name}").json()
        
        if not "card_faces" in scryfall_data.keys() or not "image_uris" in scryfall_data["card_faces"][0].keys():
            self.art_crop = scryfall_data["image_uris"]["art_crop"]
            self.image_url = scryfall_data["image_uris"]["border_crop"]
        else:
            self.art_crop = scryfall_data["card_faces"][0]["image_uris"]["art_crop"]
            self.image_url = scryfall_data["card_faces"][0]["image_uris"]["border_crop"]
    
    def lookup(self, name:str):
        card_data = requests.get("https://ligamagicapi.azurewebsites.net/LigaMagicAPI/" + name.replace(" ", "%20").replace("/", "%2f")).json()
        if "name" in card_data.keys():
            return card_data
        else:
            return None
    
    def get_smallest_price(self):
        min_prices = []
        for set_precos in self.precos.values():
            min_prices.append(min(list(set_precos.values())))
        
        return min(min_prices)

if __name__ == "__main__":
    carta = Card("Chandra, Hope's Beacon")
    print(carta.get_smallest_price())