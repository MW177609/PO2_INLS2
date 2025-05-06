# Importuje bibliotekę Tkinter.
import tkinter as tk
# Importuje klasę datetime z modułu datetime, aby obsługiwać znaczniki czasu dla logów.
from datetime import datetime
# Importuje moduł messagebox z Tkinter, który służy do wyświetlania okien dialogowych z ostrzeżeniami lub błędami.
from tkinter import messagebox
# Importuje Image i ImageTk z biblioteki PIL (Python Imaging Library) do obsługi ładowania obrazów i ich konwersji na format zgodny z Tkinter.
from PIL import Image, ImageTk
# Importuje bibliotekę requests do wykonywania zapytań HTTP do API NASA Images.
import requests
# Importuje BytesIO z modułu io, aby obsługiwać dane binarne w pamięci (np. obrazy).
from io import BytesIO

# Klasa do centralnego zarządzania stylami
# Definiuje klasę StyleConfig, która centralizuje zarządzanie stylami wizualnymi aplikacji.
class StyleConfig:
    # Definiuje metodę inicjalizującą dla klasy StyleConfig.
    def __init__(self):
        # Ustawia kolor tła (bg_color).
        self.bg_color = "black"
        # Ustawia kolor tekstu i elementów pierwszoplanowych (fg_color).
        self.fg_color = "lime"
        # Ustawia kolor tła dla aktywnych elementów (np. po najechaniu myszą).
        self.active_bg = "black"
        # Ustawia kolor pierwszoplanowy dla aktywnych elementów.
        self.active_fg = "lime"
        # Ustawia rodzinę czcionek na "Arial".
        self.font_family = "Arial"
        # Ustawia rozmiar czcionki dla etykiet.
        self.font_size_label = 14
        # Ustawia rozmiar czcionki dla przycisków.
        self.font_size_button = 14
        # Ustawia rozmiar czcionki dla tytułów (np. pod obrazami) na 10.
        self.font_size_title = 10
        # Ustawia rozmiar czcionki dla tekstu "Ładowanie..." na 20.
        self.font_size_loading = 20
        # Tworzy krotkę dla czcionki etykiet, zawierającą rodzinę czcionek i rozmiar.
        self.label_font = (self.font_family, self.font_size_label)
        # Tworzy krotkę dla czcionki przycisków.
        self.button_font = (self.font_family, self.font_size_button)
        # Tworzy krotkę dla czcionki tytułów.
        self.title_font = (self.font_family, self.font_size_title)
        # Tworzy krotkę dla czcionki tekstu ładowania, dodając atrybut "bold" (pogrubienie).
        self.loading_font = (self.font_family, self.font_size_loading, "bold")
        # Ustawia szerokość obramowania dla elementów (np. przycisków) na 2 piksele.
        self.border_width = 2
        # Ustawia grubość podświetlenia (np. dla pól tekstowych) na 2 piksele.
        self.highlight_thickness = 2

    # Definiuje metodę update_styles, która aktualizuje style czcionek.
    def update_styles(self):
        # Aktualizuje czcionkę etykiet na podstawie bieżących wartości.
        self.label_font = (self.font_family, self.font_size_label)
        # Aktualizuje czcionkę przycisków.
        self.button_font = (self.font_family, self.font_size_button)
        # Aktualizuje czcionkę tytułów.
        self.title_font = (self.font_family, self.font_size_title)
        # Aktualizuje czcionkę tekstu ładowania.
        self.loading_font = (self.font_family, self.font_size_loading, "bold")

# Definiuje klasę bazową NasaAppBase, używaną przez inne klasy w aplikacji.
class NasaAppBase:
    # Inicjalizuje klasę, przyjmując obiekt style_config i opcjonalny callback dla logów.
    def __init__(self, style_config, log_callback=None):
        # Przypisuje obiekt style_config do atrybutu style.
        self.style = style_config
        # Przypisuje funkcję callback dla logów do atrybutu log_callback.
        self.log_callback = log_callback

    # Definiuje metodę log do zapisywania wiadomości w logach.
    def log(self, message):
        # Sprawdza, czy funkcja callback dla logów istnieje.
        if self.log_callback:
            # Wywołuje funkcję callback, przekazując wiadomość.
            self.log_callback(message)

    # Definiuje metodę do obsługi błędów żądań HTTP, z domyślnym kontekstem "Operacja".
    def handle_request_errors(self, exception, context="Operacja"):
        # Sprawdza, czy wyjątek jest błędem HTTP.
        if isinstance(exception, requests.exceptions.HTTPError):
            # Loguje błąd HTTP z kodem statusu i powodem.
            self.log(f"Błąd HTTP w {context}: {exception.response.status_code} - {exception.response.reason}")
        # Sprawdza, czy wyjątek jest błędem połączenia.
        elif isinstance(exception, requests.exceptions.ConnectionError):
            # Loguje błąd połączenia.
            self.log(f"Błąd połączenia w {context}: Nie można połączyć się z serwerem.")
        # Sprawdza, czy wyjątek jest błędem przekroczenia czasu.
        elif isinstance(exception, requests.exceptions.Timeout):
            # Loguje błąd przekroczenia czasu.
            self.log(f"Błąd: Przekroczono limit czasu w {context}.")
        # Sprawdza, czy wyjątek jest ogólnym błędem żądania.
        elif isinstance(exception, requests.exceptions.RequestException):
            # Loguje ogólny błąd żądania
            self.log(f"Błąd żądania w {context}: {str(exception)}")
        # Obsługuje inne, niespodziewane wyjątki.
        else:
            # Loguje niespodziewany błąd.
            self.log(f"Niespodziewany błąd w {context}: {str(exception)}")

# Definiuje klasę LogPanel, dziedziczącą po NasaAppBase, do wyświetlania logów.
class LogPanel(NasaAppBase):
    # Inicjalizuje panel logów, przyjmując widget nadrzędny (parent) i obiekt style_config.
    def __init__(self, parent, style_config):
        # Wywołuje konstruktor klasy bazowej, przekazując style_config i metodę _log_to_text jako callback.
        super().__init__(style_config, self._log_to_text)
        # Przypisuje widget nadrzędny do atrybutu parent.
        self.parent = parent
        # Inicjalizuje atrybut text_widget jako None (później będzie to widget tekstowy).
        self.text_widget = None
        # Wywołuje metodę setup_ui do konfiguracji interfejsu.
        self.setup_ui()

    # Definiuje metodę setup_ui do tworzenia elementów interfejsu panelu logów.
    def setup_ui(self):
        # Tworzy etykietę z tekstem "Logi", ustawia czcionkę, kolory tła i tekstu, i umieszcza ją w interfejsie z odstępem 10 pikseli od góry.
        tk.Label(
            self.parent, text = "Logi", font = self.style.label_font,
            bg = self.style.bg_color, fg = self.style.fg_color
        ).pack(pady = (10, 0))

        # Tworzy widget tekstowy (tk.Text) o szerokości 40 znaków, zablokowanym stanie (tylko do odczytu), z ustawionymi kolorami tła, tekstu, kursora i podświetlenia.
        self.text_widget = tk.Text(
            self.parent, state = 'disabled', width = 40, bg = self.style.bg_color, fg = self.style.fg_color,
            insertbackground = self.style.fg_color, highlightbackground=  self.style.fg_color,
            highlightcolor = self.style.fg_color, highlightthickness = self.style.highlight_thickness
        )
        # Umieszcza widget tekstowy w interfejsie, wypełniając dostępną przestrzeń w obu kierunkach, z odstępami 10 pikseli.
        self.text_widget.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 10)

    # Definiuje metodę _log_to_text do zapisywania wiadomości w widgetcie tekstowym.
    def _log_to_text(self, message):
        # Pobiera aktualny czas i formatuje go jako ciąg w formacie "DD-MM-YYYY HH:MM:SS".
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        # Ustawia widget tekstowy w stan edytowalny, aby można było dodać tekst
        self.text_widget.configure(state = 'normal')
        # Wstawia wiadomość z timestampem na koniec widgetu tekstowego, dodając nową linię.
        self.text_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        # Przywraca widget tekstowy do stanu tylko do odczytu.
        self.text_widget.configure(state = 'disabled')
        # Przewija widget tekstowy, aby pokazać ostatnią dodaną linię.
        self.text_widget.see(tk.END)

# Definiuje klasę SearchPanel, dziedziczącą po NasaAppBase, do obsługi wyszukiwania.
class SearchPanel(NasaAppBase):
    # Inicjalizuje panel wyszukiwania, przyjmując widget nadrzędny, obiekt style_config i funkcję callback dla wyszukiwania.
    def __init__(self, parent, style_config, search_callback):
        # Wywołuje konstruktor klasy bazowej, przekazując style_config.
        super().__init__(style_config)
        # Przypisuje widget nadrzędny do atrybutu parent.
        self.parent = parent
        # Przypisuje funkcję callback dla wyszukiwania do atrybutu search_callback.
        self.search_callback = search_callback
        # Tworzy zmienną Tkinter (StringVar) do przechowywania tekstu wprowadzonego w polu wyszukiwania.
        self.search_var = tk.StringVar()
        # Wywołuje metodę setup_ui do konfiguracji interfejsu.
        self.setup_ui()

    # Definiuje metodę setup_ui do tworzenia elementów interfejsu panelu wyszukiwania.
    def setup_ui(self):
        # Tworzy ramkę (tk.Frame) jako kontener dla elementów wyszukiwania, z czarnym tłem.
        frame = tk.Frame(self.parent, bg = self.style.bg_color)
        # Umieszcza ramkę w górnej części interfejsu, wypełniając przestrzeń w poziomie, z odstępem 10 pikseli od góry.
        frame.pack(side = tk.TOP, fill = tk.X, pady = (10, 0))

        # Tworzy wewnętrzną ramkę dla lepszego rozmieszczenia elementów.
        inner_frame = tk.Frame(frame, bg = self.style.bg_color)
        # Umieszcza wewnętrzną ramkę w centrum ramki nadrzędnej, z odstępem 5 pikseli.
        inner_frame.pack(anchor = "center", pady = 5)

        # Tworzy etykietę z tekstem "Podaj zapytanie: ", ustawia czcionkę i kolory, i umieszcza ją w siatce (wiersz 0, kolumna 0) z odstępem 10 pikseli po prawej.
        tk.Label(
            inner_frame, text = "Podaj zapytanie: ", font = self.style.label_font,
            bg = self.style.bg_color, fg = self.style.fg_color
        ).grid(row = 0, column = 0, padx = (0, 10))

        # Tworzy pole tekstowe (tk.Entry) powiązane ze zmienną search_var, o szerokości 30 znaków, z ustawionymi kolorami i czcionką, i umieszcza je w siatce (wiersz 0, kolumna 1).
        tk.Entry(
            inner_frame, textvariable = self.search_var, font = self.style.label_font, width = 30,
            bg = self.style.bg_color, fg = self.style.fg_color, insertbackground = self.style.fg_color
        ).grid(row = 0, column = 1, padx = (0, 10))

        # Tworzy przycisk z tekstem "Szukaj", przypisuje metodę _on_search jako akcję, ustawia style i umieszcza go w siatce (wiersz 0, kolumna 2).
        tk.Button(
            inner_frame, text = "Szukaj", command = self._on_search, font = self.style.button_font,
            bg = self.style.bg_color, fg = self.style.fg_color, activebackground = self.style.active_bg,
            activeforeground = self.style.active_fg, borderwidth = self.style.border_width
        ).grid(row = 0, column = 2)

        # Iteruje po krotkach definiujących wagi kolumn w siatce.
        for col, weight in [(0, 0), (1, 1), (2, 0)]:
            # Ustawia wagi dla kolumn siatki (kolumna 1 rozciąga się, kolumny 0 i 2 nie)
            inner_frame.grid_columnconfigure(col, weight = weight)

    # Definiuje metodę _on_search, wywoływaną po kliknięciu przycisku "Szukaj".
    def _on_search(self):
        # Pobiera tekst z pola wyszukiwania.
        query = self.search_var.get()
        # Sprawdza, czy pole wyszukiwania jest puste.
        if not query:
            # Loguje błąd, jeśli pole jest puste.
            self.log("Błąd: Wprowadź zapytanie wyszukiwania.")
            # Wyświetla okno dialogowe z ostrzeżeniem.
            messagebox.showwarning("Błąd", "Wprowadź zapytanie!")
            # Kończy metodę, jeśli pole jest puste.
            return
        # Wywołuje funkcję callback, przekazując zapytanie wyszukiwania.
        self.search_callback(query)

# Definiuje klasę ImageGrid, dziedziczącą po NasaAppBase, do wyświetlania siatki obrazów.
class ImageGrid(NasaAppBase):
    # Inicjalizuje siatkę obrazów, przyjmując widget nadrzędny, obiekt style_config i funkcję callback dla logów.
    def __init__(self, parent, style_config, log_callback):
        # Wywołuje konstruktor klasy bazowej, przekazując style_config i log_callback.
        super().__init__(style_config, log_callback)
        # Przypisuje widget nadrzędny do atrybutu parent.
        self.parent = parent
        # Tworzy ramkę dla obrazów z czarnym tłem.
        self.images_frame = tk.Frame(self.parent, bg=self.style.bg_color)
        # Umieszcza ramkę, wypełniając dostępną przestrzeń w obu kierunkach.
        self.images_frame.pack(fill=tk.BOTH, expand=True)
        # Inicjalizuje pustą listę do przechowywania obiektów ImageTk.PhotoImage.
        self.images = []

    # Definiuje metodę clear_images do czyszczenia siatki obrazów.
    def clear_images(self):
        # Iteruje po wszystkich widgetach w ramce obrazów.
        for widget in self.images_frame.winfo_children():
            # Usuwa każdy widget z ramki.
            widget.destroy()
        # Czyści listę przechowywanych obrazów.
        self.images.clear()

    # Definiuje metodę display_images, która wyświetla obrazy na podstawie listy elementów (items) i głównego okna (root).
    def display_images(self, items, root):
        # Ustawia liczbę kolumn w siatce na 3.
        col_count = 3
        # Inicjalizuje zmienne do śledzenia wierszy, kolumn i liczby wyświetlanych obrazów.
        row = col = shown = 0
        # Tworzy etykietę z tekstem "Ładowanie..." i odpowiednimi stylami.
        loading_label = tk.Label(
            root, text = "Ładowanie...", font = self.style.loading_font,
            fg = self.style.fg_color, bg = self.style.bg_color
        )
        # Umieszcza etykietę w centrum okna.
        loading_label.place(relx = 0.5, rely = 0.5, anchor = "center")
        # Aktualizuje główne okno, aby wyświetlić etykietę.
        root.update()

        # Definiuje wewnętrzną funkcję load_image do ładowania pojedynczego obrazu.
        def load_image(item):
            # Deklaruje zmienne row, col i shown jako nonlocal, aby móc je modyfikować.
            nonlocal row, col, shown
            # Pobiera listę linków z elementu, domyślnie pustą listę.
            links = item.get("links", [])
            # Pobiera listę danych z elementu, domyślnie pustą listę.
            data = item.get("data", [])
            # Sprawdza, czy istnieją linki i dane.
            if not links or not data:
                # Loguje pominięcie elementu, jeśli brak linków lub danych.
                self.log("Pominięto element: Brak linków lub danych.")
                # Zwraca True, aby kontynuować przetwarzanie.
                return True

            # Pobiera URL obrazu z pierwszego linku.
            img_url = links[0].get("href")
            # Pobiera tytuł z pierwszych danych, domyślnie "Brak tytułu".
            title = data[0].get("title", "Brak tytułu")
            # Sprawdza, czy istnieje URL obrazu.
            if not img_url:
                # Loguje pominięcie elementu, jeśli brak URL.
                self.log("Pominięto element: Brak linku obrazu.")
                # Zwraca True, aby kontynuować.
                return True

            # Loguje rozpoczęcie ładowania obrazu, obcinając tytuł do 50 znaków.
            self.log(f"Ładowanie obrazu '{title[:50]}' ({img_url})")
            # Rozpoczyna blok obsługi wyjątków dla ładowania obrazu.
            try:
                # Pobiera dane obrazu za pomocą żądania HTTP.
                img_data = requests.get(img_url).content
                # Otwiera obraz z danych binarnych w pamięci.
                image = Image.open(BytesIO(img_data))
                # Skaluje obraz do miniatury o maksymalnych wymiarach 200x200 pikseli.
                image.thumbnail((200, 200))
                # Konwertuje obraz na format zgodny z Tkinter.
                photo = ImageTk.PhotoImage(image)
                # Dodaje obraz do listy images.
                self.images.append(photo)

                # Tworzy ramkę dla obrazu i jego tytułu.
                img_container = tk.Frame(self.images_frame, bg = self.style.bg_color)
                # Umieszcza ramkę w siatce w odpowiednim wierszu i kolumnie.
                img_container.grid(row = row, column = col, padx = 5, pady = 5)

                # Tworzy przycisk z obrazem, który po kliknięciu otwiera pełne zdjęcie, ustawia style i kursor.
                img_button = tk.Button(
                    img_container, image = photo, command = lambda url = img_url: self._open_image_window(url),
                    bg = self.style.fg_color, activebackground = self.style.fg_color,
                    borderwidth = self.style.border_width, highlightthickness = self.style.highlight_thickness,
                    highlightbackground = self.style.fg_color, highlightcolor = self.style.fg_color,
                    cursor = "hand2"
                )
                # Umieszcza przycisk w ramce.
                img_button.pack()

                # Tworzy etykietę z tytułem obrazu (obciętym do 50 znaków, jeśli dłuższy), ustawia style.
                title_label = tk.Label(
                    img_container, text = title[:50] + "..." if len(title) > 50 else title,
                    font = self.style.title_font, bg = self.style.bg_color, fg = self.style.fg_color
                )
                # Umieszcza etykietę pod obrazem.
                title_label.pack()

                # Aktualizuje ramkę obrazów, aby wyświetlić nowy obraz.
                self.images_frame.update()
                # Loguje zakończenie ładowania obrazu.
                self.log(f"Załadowano obraz: '{title[:50]}'")
                # Zwiększa licznik kolumn.
                col += 1
                # Sprawdza, czy osiągnięto maksymalną liczbę kolumn.
                if col >= col_count:
                    # Resetuje kolumnę do 0.
                    col = 0
                    # Zwiększa licznik wierszy.
                    row += 1
                # Zwiększa licznik wyświetlanych obrazów.
                shown += 1
                # Zwraca True, jeśli wyświetlono mniej niż 9 obrazów, w przeciwnym razie False.
                return shown < 9
            # Łapie wszelkie wyjątki podczas ładowania obrazu.
            except Exception as e:
                # Obsługuje błędy, logując je z kontekstem.
                self.handle_request_errors(e, f"ładowaniu obrazu '{title[:50]}'")
                # Zwraca True, aby kontynuować przetwarzanie.
                return True

        # Definiuje funkcję process_next_image do iteracyjnego przetwarzania obrazów.
        def process_next_image(index=0):
            # Sprawdza, czy przetworzono wszystkie elementy lub czy należy zakończyć.
            if index >= len(items) or not load_image(items[index]):
                # Sprawdza, czy etykieta "Ładowanie..." nadal istnieje.
                if loading_label.winfo_exists():
                    # Usuwa etykietę "Ładowanie...".
                    loading_label.destroy()
                    #Loguje zakończenie ładowania.
                self.log("Zakończono ładowanie obrazów.")
                # Kończy funkcję.
                return
            # Planuje wywołanie funkcji dla kolejnego obrazu po 10 ms.
            root.after(10, process_next_image, index + 1)

        # Loguje rozpoczęcie ładowania obrazów.
        self.log("Rozpoczęto ładowanie obrazów.")
        # Planuje rozpoczęcie przetwarzania obrazów po 100 ms.
        root.after(100, process_next_image)

    # Definiuje metodę _open_image_window do otwierania pełnego obrazu w nowym oknie.
    def _open_image_window(self, img_url):
        # Rozpoczyna blok obsługi wyjątków.
        try:
            # Pobiera dane pełnego obrazu.
            img_data = requests.get(img_url).content
            # Otwiera obraz z danych binarnych.
            image = Image.open(BytesIO(img_data))
            # Tworzy nowe okno (Toplevel) do wyświetlenia obrazu.
            win = tk.Toplevel(self.parent)
            # Ustawia tytuł okna na "Podgląd zdjęcia".
            win.title("Podgląd zdjęcia")
            # Ustawia czarne tło dla okna.
            win.configure(bg = self.style.bg_color)

            # Pobiera wymiary obrazu.
            img_width, img_height = image.size
            # Sprawdza, czy obraz jest większy niż 1000x800 pikseli.
            if img_width > 1000 or img_height > 800:
                # Skaluje obraz do maksymalnych wymiarów 1000x800.
                image.thumbnail((1000, 800))

            # Konwertuje obraz na format Tkinter.
            photo = ImageTk.PhotoImage(image)
            # Tworzy etykietę z obrazem i czarnym tłem.
            label = tk.Label(win, image = photo, bg = self.style.bg_color)
            # Przypisuje obraz do atrybutu etykiety, aby uniknąć garbage collection.
            label.image = photo
            # Umieszcza etykietę w oknie.
            label.pack()
        # Łapie wszelkie wyjątki podczas otwierania obrazu.
        except Exception as e:
            # Obsługuje błędy, logując je z kontekstem.
            self.handle_request_errors(e, "otwieraniu obrazu")

# Definiuje główną klasę aplikacji, dziedziczącą po NasaAppBase.
class FetchNasaImagesApp(NasaAppBase):
    # Inicjalizuje aplikację, przyjmując główne okno Tkinter (root).
    def __init__(self, root):
        # Tworzy instancję StyleConfig i przypisuje ją do atrybutu style.
        self.style = StyleConfig()
        # Wywołuje konstruktor klasy bazowej, przekazując style.
        super().__init__(self.style)
        # Przypisuje główne okno do atrybutu root.
        self.root = root
        # Ustawia tytuł głównego okna na "NASA Image Search".
        self.root.title("NASA Image Search")
        # Ustawia bazowy URL API NASA Images.
        self.base_url = "https://images-api.nasa.gov/search"
        # Ustawia czarne tło dla głównego okna.
        self.root.configure(bg = self.style.bg_color)
        # Tworzy instancję SearchPanel, przekazując główne okno, style i metodę search_images jako callback.
        self.search_panel = SearchPanel(self.root, self.style, self.search_images)
        # Wywołuje metodę setup_ui do konfiguracji interfejsu.
        self.setup_ui()

    # Definiuje metodę setup_ui do tworzenia głównego układu interfejsu.
    def setup_ui(self):
        # Tworzy główną ramkę z czarnym tłem.
        main_frame = tk.Frame(self.root, bg = self.style.bg_color)
        # Umieszcza ramkę, wypełniając dostępną przestrzeń.
        main_frame.pack(fill = tk.BOTH, expand = True)

        # Tworzy lewą ramkę dla siatki obrazów.
        left_frame = tk.Frame(main_frame, bg = self.style.bg_color)
        # Umieszcza lewą ramkę po lewej stronie, wypełniając przestrzeń, z odstępami 10 pikseli.
        left_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True, padx = 10, pady = 10)

        # Tworzy prawą ramkę dla logów o szerokości 300 pikseli.
        right_frame = tk.Frame(main_frame, width = 300, bg = self.style.bg_color)
        # Umieszcza prawą ramkę po prawej stronie, wypełniając przestrzeń w pionie.
        right_frame.pack(side = tk.RIGHT, fill = tk.Y)

        # Tworzy instancję LogPanel w prawej ramce.
        self.log_panel = LogPanel(right_frame, self.style)
        # Tworzy instancję ImageGrid w lewej ramce, przekazując funkcję logowania.
        self.image_grid = ImageGrid(left_frame, self.style, self.log_panel.log)

    # Definiuje metodę search_images do wyszukiwania obrazów na podstawie zapytania.
    def search_images(self, query):
        # Czyści siatkę obrazów.
        self.image_grid.clear_images()
        # Loguje rozpoczęcie wyszukiwania z podanym zapytaniem.
        self.log(f"Wyszukiwanie: {query}")

        # Rozpoczyna blok obsługi wyjątków dla wyszukiwania.
        try:
            # Tworzy słownik parametrów żądania (zapytanie i typ mediów: obraz).
            params = {'q': query, 'media_type': 'image'}
            # Wykonuje żądanie GET do API NASA z parametrami.
            response = requests.get(self.base_url, params = params)
            # Zgłasza wyjątek, jeśli żądanie zwróci błąd HTTP.
            response.raise_for_status()

            # Parsuje odpowiedź JSON na słownik Pythona.
            data = response.json()
            # Pobiera listę elementów z odpowiedzi, domyślnie pustą listę.
            items = data.get("collection", {}).get("items", [])
            # Sprawdza, czy lista elementów jest pusta.
            if not items:
                # Loguje brak wyników.
                self.log("Brak wyników dla danego wyszukiwania.")
                # Kończy metodę, jeśli brak wyników.
                return

            # Loguje liczbę znalezionych wyników i informację o limicie 9 obrazów.
            self.log(f"Znaleziono {len(items)} wyników. Wyświetlam maksymalnie 9 obrazów.")
            # Wyświetla obrazy w siatce, przekazując elementy i główne okno.
            self.image_grid.display_images(items, self.root)
        # Łapie wszelkie wyjątki podczas wyszukiwania.
        except Exception as e:
            # Obsługuje błędy, logując je z kontekstem.
            self.handle_request_errors(e, "wyszukiwaniu")

# Definiuje główną funkcję main do uruchamiania aplikacji.
def main():
    # Tworzy główne okno Tkinter.
    root = tk.Tk()
    # Tworzy instancję aplikacji FetchNasaImagesApp, przekazując główne okno.
    FetchNasaImagesApp(root)
    # Ustawia rozmiar okna na 1200x800 pikseli.
    root.geometry("1200x800")
    # Uruchamia główną pętlę Tkinter, która obsługuje zdarzenia GUI.
    root.mainloop()

# Sprawdza, czy skrypt jest uruchamiany bezpośrednio (a nie importowany jako moduł).
if __name__ == "__main__":
    # Wywołuje funkcję main do uruchomienia aplikacji.
    main()