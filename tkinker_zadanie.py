import tkinter as tk # tk, ttk, messagebox - tworzy okna, przyciski, pola tekstowe i komunikaty (np. ostrzeżenia)
from datetime import datetime # generuje znaczniki czasowe dla logów
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk # przetwarza obray (skaluje) i konwertuje je na na format wyświetlany przez tkinter
import requests # wysyła żądania HTTP do API NASA w celu pobrania danych i obrazów
from io import BytesIO # umożliwia odzczyt danych obrazów jako strumienia w pamięci

# inicjalizuje aplikację, ustawia okno główne i podstawowe zminne
class FetchNasaImagesApp:
    def __init__(self, root):
        self.root = root # przechowuje referencję do głównego okne tkinter
        self.root.title("NASA Image Search") # tytuł okna
        self.base_url = "https://images-api.nasa.gov/search" # definiuje adres API NASA do wyszukiwania

        self.images = [] # lista przechowująca obiekty (w tym wypadku obrazy), aby zapobieć ich usuwaniu przez garbage (collection Pythona)
        self.setup_ui() # wywołuje metodę konfigurującą interfejs graficzny

    # Tworzy i konfiguruje interfejs graficzy aplikacji
    def setup_ui(self):
        self.root.configure(bg = 'black') # czarne tło dla całego okna

        # Pasek na wyszukiwanie
        top_frame = tk.Frame(self.root, bg = 'black') # tworzy ramkę na pasek wyszukiwania
        top_frame.pack(side = tk.TOP, pady = 20) # to odpowiada gdzie pasek się znajduje

        self.search_var = tk.StringVar() # zmienna przechowująca teks wpisany w polu wyszukiwania

        # Pole tekstowe na 30 znaków szerokości
        search_entry = tk.Entry(top_frame, textvariable = self.search_var, font=("Arial", 14), width=30, bg= 'black', fg = 'lime', insertbackground = 'lime')
        search_entry.grid(row=0, column=0, padx=(0, 10))

        # Przycisk "szukaj" wywołujący metodę "search_images" po kliknięciu
        search_button = tk.Button(top_frame, text = "Szukaj", command = self.search_images, font = ("Arial", 14), bg = 'black', fg = 'lime', activebackground = 'black', activeforeground = 'lime', borderwidth= 2, highlightbackground= 'lime', highlightcolor= 'lime')
        search_button.grid(row = 0, column = 1)

        # Wycentrowanie pola wyszukuwania, dają mu większą wagę (rozciąga się), a przycisk "szukaj" pozostaje nie zieniony
        top_frame.grid_columnconfigure(0, weight = 1)
        top_frame.grid_columnconfigure(1, weight = 0)

        # Panel główny
        main_frame = tk.Frame(self.root, bg = 'black')
        main_frame.pack(fill = tk.BOTH, expand = True) # Ramka wypełnijąca okno rozciąga się w pionie i poziomie

        # Lewa strona - obrazy
        # ramka na obrazy, rozciąga się w lewej części
        self.left_frame = tk.Frame(main_frame, bg = 'black')
        self.left_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True, padx = 10, pady = 10)

        # Wewnętrzna ramka na siatkę obrazów, wypełnia dostępną przestrzeń
        self.images_frame = tk.Frame(self.left_frame, bg = 'black')
        self.images_frame.pack(fill = tk.BOTH, expand = True)

        # Prawa strona - logi
        # Ramka o stałej szerokości (300 pix) na panel logów
        self.right_frame = tk.Frame(main_frame, width = 300, bg = 'black')
        self.right_frame.pack(side = tk.RIGHT, fill = tk.Y)

        # Etykieta "Logi" nad panelem logów
        log_label = tk.Label(self.right_frame, text = "Logi", font = ("Arial", 14), bg = 'black', fg = 'lime')
        log_label.pack(pady = (10, 0))

        # Pole tekstowe (tylko do odczytu) do wyświetlania logów, rozciąga się wypełniając przestrzeń
        self.log_text = tk.Text(self.right_frame, state = 'disabled', width = 40, bg = 'black', fg = 'lime', insertbackground = 'lime', highlightbackground = 'lime', highlightcolor = 'lime', highlightthickness = 2)
        self.log_text.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)

    # Logi
    # Dodje wiadomości do panelu logów z aktualnym znacznikeim czasowym
    def log(self, message):
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Generuje znacznik czasu
        self.log_text.configure(state = 'normal') # Wyłącza edytowanie pola tekstowego logów
        self.log_text.insert(tk.END,f"[{timestamp}] {message}\n") # dodaje wiadomości w formacie : na końcu tekstu z nową linią
        self.log_text.configure(state = 'disabled') # wyłącza edytowanie aby użtkownik nie mógł zmnieniać logów
        self.log_text.see(tk.END) # Przewija panel logów do najnowszej wiadomości, aby była zawsze widoczna

    # Wyszukiwanie obrazów
    # wyszukuje obrazy w API NASA na podstawie zapytania użytkownika i inicjuje ich wyświetlenie
    def search_images(self):
        query = self.search_var.get() # pobiera tekst z pola wyszukiwania

        if not query: # jeśli query jest puste loguje bład i pokazuje ostrzeżenie w oknie dialogowym
            self.log("Błąd: Wprowadź zapytanie wyszukiwania.")
            messagebox.showwarning("Błąd", "Wprowadź zapytanie!")
            return

        self.clear_images()
        self.log(f"Wyszukiwanie: {query}")

        try:
            params = {'q': query, 'media_type': 'image'} # tworzy parametry żądania (q - zapytanie, a "media_type: image" - wynik w postaci obrazów)
            response = requests.get(self.base_url, params = params) # wysyła żądanie "get" do API NASA
            response.raise_for_status() # sprawdza czy odpowiedź HTTp jest poprawna

            # Przetwarzanie odpowiedzi
            data = response.json() # parsuje odpowiedź json
            items = data.get("collection", {}).get("items", []) # pobiera listę wyników z odpowiedzi z zabezpieczeniem przed brakiem kluczy

            if not items: # jeśli "items" jest puste, loguje brak wyników i kończy
                self.log("Brak wyników dla danego wyszukiwania.")
                return
            # loguje liczbe znalezionych wyników i limit (max. 9 obrazków)
            self.log(f"Znaleziono {len(items)} wyników. Wyświetlam maksymalnie 9 obrazów.")
            self.display_images(items)

        # Obsługa błędów
        except requests.exceptions.HTTPError as e: # loguje kod błędu HTTP i przyczynę
            self.log(f"Błąd HTTP: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.ConnectionError: # loguje problem z połączeniem
            self.log("Błąd połączenia: Nie można połączyć się serwerem NASA.")
        except requests.exceptions.Timeout: # loguje przekroczenie limitu czasu
            self.log("Błąd: Przekroczono limit czasu żądania.")
        except requests.exceptions.RequestException as e: # loguje inne błedy żądania
            self.log(f"Błąd żądania: {str(e)}") # e - obiekt wątku (błąd), w stringu żeby był w formie tekstu
        except ValueError as e: # loguje błędy parsowania json
            self.log(f"Błąd parsowania json: {str(e)}")
        except Exception as e: # loguje niespodziewane błedy,
            self.log(f"Niespodziewany błąd: {str(e)}")

    # czyści siatkę obrazów przed nowym wyszukanie (zabija dzieci XD)
    def clear_images(self):
        for widget in self.images_frame.winfo_children(): # pobiera wszystkie widżety (ramki z obrazkami i tytułami) w "images_frame"
            widget.destroy() # usuwa każdy widżet z interfejsu
        self.images.clear() # czyści listę referencji do obiektów "PhotoImage", zwalniając pamięć

    # Wyświetla do 9 obrazków w siatce 3x3, jeden po drugin, z etykietą "Ładowanie..." na pierwszym planie
    def display_images(self, items):
        col_count = 3 # skala siatki
        row = 0 # zmienne śledzące pozycję w siatce i liczbę wyświetlanych obrazów
        col = 0
        shown = 0

        # Etykieta ładowania
        # twoży etykietę "ładowanie..."
        loading_label = tk.Label(self.root, text = "Ładowanie...", font = ("Arial", 20, "bold"), fg = "lime", bg = "black")
        loading_label.place(relx = 0.5, rely = 0.5, anchor = "center") #umieszcza ją na środku okna głównego, na pierwszym planie

        self.root.update() # odświeża interfejs, aby etykieta była widoczna przed ładowaniem obrazów

        def load_image(item): # Ładuje i wyświetla pojedynczy obraz w siatce
            nonlocal row, col, shown # używa zmiennych z zwenętrznego zakresu
            links = item.get("links", []) # pobiera links i data z elementu json
            data = item.get("data", [])
            if not links or not data: # jeśli brak, zapisuje w logach i pomija
                self.log("Pominięto element: Brak linków lub danych.")
                return True

            img_url = links[0].get("href") # pobiera img_url (adres obrazu) i tytuł, domyślnie jak obraz nie ma tytułu daje "Brak tytułu"
            title = data[0].get("title", "Brak tytułu")

            if not img_url: # jeśli brak img_url loguje i pomija
                self.log("Pominięto element: Brak linku obrazu.")
                return True

            self.log(f"Ładowanie obrazu '{title[:50]}' ({img_url})") # wpisuje w logi rozpoczęcie ładowania obrazu z tytułem i URL

            # Ładowanie obrazu
            try:
                img_data = requests.get(img_url).content # pobiera dane zobrazu
                image = Image.open(BytesIO(img_data)) # otwiera obraz w pamięci
                image.thumbnail((200, 200)) # skaluje obraz do maksymalnie 200 x 200 pikseli
                photo = ImageTk.PhotoImage(image) # konwertuje obraz na format tkinter
                self.images.append(photo) # zapisuje referencję, aby uniknąć garbage (collection Pythona)

                # Ramka na obraz i tytuł
                img_container = tk.Frame(self.images_frame, bg = 'black') # tworzy ramkę na obraz i tytuł
                img_container.grid(row = row, column = col, padx = 5, pady = 5) # grid umieszcza ramkę w siatce

                # Obraz z zieloną ramką
                # przycisk z obrazem który po kliknęciu wywołuje "ope_image_window(img_url)", reszta odpowiada za zieloną ramkę wokół zdjęcia
                img_button = tk.Button(img_container, image=photo, command=lambda url=img_url: self.open_image_window(url), bg = 'lime', activebackground= 'lime', borderwidth = 2, highlightthickness = 2, highlightbackground = 'lime', highlightcolor = 'lime')
                img_button.pack()

                # Tytuł
                # "title_label" - etykieta z tytułem (max 50 znaków)
                title_label = tk.Label(img_container, text = title[:50] + "..." if len(title) > 50 else title, font = ("Arial", 10), bg = 'black', fg = 'lime')
                title_label.pack() # układa przycisk i etykietę w ramce

                self.images_frame.update() # odświeża siatkę, aby obraz był widoczny natychmiast

                # Logi pomyślnego załadowania obrazu
                self.log(f"Załadowano obraz: '{title[:50]}'")
                col += 1
                if col >= col_count:  # aktualizuje pozycję w siatce (col, row) i licznki (shown)
                    col = 0
                    row += 1
                shown += 1
                return shown < 9 # kończy w momencie wyświetlenia 9 obrazów

            # Obsługa błędów (obrazów)
            except requests.exceptions.HTTPError as e:
                self.log(f"Błąd HTTP przy ładowaniu obrazu '{title[:50]}': {e.response.status_code} - {e.response.reason}")
                return True
            except requests.exceptions.ConnectionError:
                self.log(f"Błąd połączenia przy ładaowaniu obrazu '{title[:50]}': Nie można połączyć się z serwerem.")
                return True
            except requests.exceptions.Timeout:
                self.log(f"Błąd: przekroczono limit czasu przy ładaowaniu obrazu '{title[:50]}'.")
                return True
            except requests.exceptions.RequestException as e:
                self.log(f"Błąd żądania przy ładowania obrazu '{title[:50]}': {str(e)}")
                return True
            except IOError as e:
                self.log(f"Błąd przetwarzania obrazu '{title[:50]}': {str(e)}")
                return True
            except Exception as e:
                self.log(f"Niespodziewany błąd przy ładowaniu obrazu '{title[:50]}': {str(e)}")
                return True

        # Planuje ładowanie obrazów jeden po drugim
        def process_next_image(index = 0):
            if index >= len(items) or not load_image(items[index]): # sprawdzanie czy "index" nie przekracza liczby elementów lub czy "load_image" zwraca False
                if loading_label.winfo_exists(): # jeśli zwraca False, usuwa etykietę "loading_label" (jeśli_istnieje) i pisze w logach zakończenie
                    loading_label.destroy()
                self.log("Zakończono ładowanie obrazów.")
                return
            self.root.after(10, process_next_image, index + 1) # w przeciwnym razie planuje ładowanie kolejnego obrazu za 10 ms

        # loguje rozpoczęcie wyświetlania
        self.log("Rozpoczęto ładowanie obrazów.")
        self.root.after(100, process_next_image) # opóżnia start o 100 ms, aby etykieta "Ładowanie..." była widoczna

    # Otwieranie nowego okna z obrazem
    # Otwiera nowe okno z pełnowymiarowym obrazkiem po kliknięciu miniatury
    def open_image_window(self, img_url):
        try:
            img_data = requests.get(img_url).content # pobiera dane obrazu
            image = Image.open(BytesIO(img_data)) # otwiera obraz

            win = tk.Toplevel(self.root) # towrzy nowe okno podrzędne
            win.title("Podgląd zdjęcia") # ustawia tytuł okna
            win.configure(bg = 'black') # dodaje czarne tło okna

            img_width, img_height = image.size
            # Skalowanie zdjęcia jeśli przekacza 1000 x 800 pikseli
            if img_width > 1000 or img_height > 800:
                image.thumbnail((1000, 800))

            photo = ImageTk.PhotoImage(image) # konwertuje obraz
            label = tk.Label(win, image=photo, bg = 'black') # wyświetla obraz w etykiecie
            label.image = photo  # zachowuje referęcję, aby uniknąć garbage collection
            label.pack() # umieszcza etykietę w oknie

        # obsługa błędów (obrazy w oknie)
        except requests.exceptions.HTTPError as e:
            self.log(f"Błąd HTTP przy ładowaniu obrazu: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.ConnectionError:
            self.log(f"Błąd połączenia przy otwieraniu obrazu: Nie można połączyć się z serwerem.")
        except requests.exceptions.Timeout:
            self.log(f"Błąd: przekroczono limit czasu przy otwieraniu obrazu.")
        except requests.exceptions.RequestException as e:
            self.log(f"Błąd żądania przy otwierania obrazu: {str(e)}")
        except IOError as e:
            self.log(f"Błąd przetwarzania obrazu w podglądzie: {str(e)}")
        except Exception as e:
            self.log(f"Niespodziewany błąd przy otwieraniu obrazu: {str(e)}")
        except Exception as e:
            self.log(f"Błąd przy otwieraniu obrazu: {str(e)}")

# Funkcja main i uruchomienie
def main():
    root = tk.Tk() # tworzy główne okno tkinter
    app = FetchNasaImagesApp(root) # włącza aplikację w oknie
    root.geometry("1200x800") # wielkość okna aplikacji
    root.mainloop() # pętla zadarzeń tkinter, obsługuje interakcje użytkownika

if __name__ == "__main__": # to zapewnia zę "main" uruchomi się tylko, jeśli skrypt jest uruchamiany bezpośrednio (nie jako moduł)
    main()
