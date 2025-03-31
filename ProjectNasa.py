import requests
import json

def fetch_nasa_images(query):
    url = "https://images-api.nasa.gov/search"

    params_query = {
        'q' : query
    }

    # example: https://images-api.nasa.gov/search?q=sun
    response = requests.get(url, params=params_query)
    # print(response)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Nie udało się pobrać danych, kod statusu: {response.status_code}')

def main():
    query = input("Podaj zapytanie: ") # To nam wywołuje terminal z treścią zadania do wykonania
    try:
        data = fetch_nasa_images(query)
        items = data.get("collection", {}).get("items", [])
        # items = [{}, {}, {}] lub [{}] items[0]
        if not items:
            print("Brak wyników dla podanego zapytania")
            return

        for item in items[:5]:
            item_data = item.get("data", [])

            if item_data:
                title = item_data[0].get("title", "Brak tytułu")
                print(f"Tytuł: {title}")

            link = item.get("links", [])

            if link:
                href = link[0].get("href", "Brak linku")
                print(f"Link: {href}")

            print("-" * 40)


    except Exception as e:
        print(f"Wystąpił błąd: {e}")

# data = fetch_nasa_images("sun")
# print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()