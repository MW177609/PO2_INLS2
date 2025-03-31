import requests

class FetchNasaImages:
    def __init__(self):
        self.base_url = "https://images-api.nasa.gov/search"
    
    def fetch_images(self, query):
        # pobiera dane z API NASA
        params = {'q': query}
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Nie udało się pobrać danych, kod ststusu: {response.ststus_code}')
        
    def display_results(self, data, limit=5):
        # wyświetla wynik w formacie tekstowym
        items = data.get("collection", {}).get("items", [])

        if not items:
            print("Brak wyników dla tego zapytania")
            return
        
        for item in items[:limit]:
            item_data = item.get("data", [])
            if item_data:
                title = item_data[0].get("title", "Brak tytułu")
                print(f"Tytuł: {title}")

            link = item.get("links", [])
            if link:
                href = link[0].get("href", "Brak linku")
                print(f"Link: {href}")

            print("-" * 40)
    
    def run(self):

        query = input("Podaj zapytanie: ")
        try:
            data = self.fetch_images(query)
            self.display_results(data)
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

def main():
    fetcher = FetchNasaImages()
    fetcher.run()

if __name__ == "__main__":
    main()