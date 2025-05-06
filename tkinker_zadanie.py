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
    def __init__(self, parent, style_config):
        super().__init__(style_config, self._log_to_text)
        self.parent = parent
        self.text_widget = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self.parent, text="Logi", font=self.style.label_font,
            bg=self.style.bg_color, fg=self.style.fg_color
        ).pack(pady=(10, 0))

        self.text_widget = tk.Text(
            self.parent, state='disabled', width=40, bg=self.style.bg_color, fg=self.style.fg_color,
            insertbackground=self.style.fg_color, highlightbackground=self.style.fg_color,
            highlightcolor=self.style.fg_color, highlightthickness=self.style.highlight_thickness
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _log_to_text(self, message):
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_widget.configure(state='disabled')
        self.text_widget.see(tk.END)

# Panel wyszukiwania
class SearchPanel(NasaAppBase):
    def __init__(self, parent, style_config, search_callback):
        super().__init__(style_config)
        self.parent = parent
        self.search_callback = search_callback
        self.search_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.parent, bg=self.style.bg_color)
        frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

        inner_frame = tk.Frame(frame, bg=self.style.bg_color)
        inner_frame.pack(anchor="center", pady=5)

        tk.Label(
            inner_frame, text="Podaj zapytanie: ", font=self.style.label_font,
            bg=self.style.bg_color, fg=self.style.fg_color
        ).grid(row=0, column=0, padx=(0, 10))

        tk.Entry(
            inner_frame, textvariable=self.search_var, font=self.style.label_font, width=30,
            bg=self.style.bg_color, fg=self.style.fg_color, insertbackground=self.style.fg_color
        ).grid(row=0, column=1, padx=(0, 10))

        tk.Button(
            inner_frame, text="Szukaj", command=self._on_search, font=self.style.button_font,
            bg=self.style.bg_color, fg=self.style.fg_color, activebackground=self.style.active_bg,
            activeforeground=self.style.active_fg, borderwidth=self.style.border_width
        ).grid(row=0, column=2)

        for col, weight in [(0, 0), (1, 1), (2, 0)]:
            inner_frame.grid_columnconfigure(col, weight=weight)

    def _on_search(self):
        query = self.search_var.get()
        if not query:
            self.log("Błąd: Wprowadź zapytanie wyszukiwania.")
            messagebox.showwarning("Błąd", "Wprowadź zapytanie!")
            return
        self.search_callback(query)

# Siatka obrazów
class ImageGrid(NasaAppBase):
    def __init__(self, parent, style_config, log_callback):
        super().__init__(style_config, log_callback)
        self.parent = parent
        self.images_frame = tk.Frame(self.parent, bg=self.style.bg_color)
        self.images_frame.pack(fill=tk.BOTH, expand=True)
        self.images = []

    def clear_images(self):
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        self.images.clear()

    def display_images(self, items, root):
        col_count = 3
        row = col = shown = 0
        loading_label = tk.Label(
            root, text="Ładowanie...", font=self.style.loading_font,
            fg=self.style.fg_color, bg=self.style.bg_color
        )
        loading_label.place(relx=0.5, rely=0.5, anchor="center")
        root.update()

        def load_image(item):
            nonlocal row, col, shown
            links = item.get("links", [])
            data = item.get("data", [])
            if not links or not data:
                self.log("Pominięto element: Brak linków lub danych.")
                return True

            img_url = links[0].get("href")
            title = data[0].get("title", "Brak tytułu")
            if not img_url:
                self.log("Pominięto element: Brak linku obrazu.")
                return True

            self.log(f"Ładowanie obrazu '{title[:50]}' ({img_url})")
            try:
                img_data = requests.get(img_url).content
                image = Image.open(BytesIO(img_data))
                image.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(image)
                self.images.append(photo)

                img_container = tk.Frame(self.images_frame, bg=self.style.bg_color)
                img_container.grid(row=row, column=col, padx=5, pady=5)

                img_button = tk.Button(
                    img_container, image=photo, command=lambda url=img_url: self._open_image_window(url),
                    bg=self.style.fg_color, activebackground=self.style.fg_color,
                    borderwidth=self.style.border_width, highlightthickness=self.style.highlight_thickness,
                    highlightbackground=self.style.fg_color, highlightcolor=self.style.fg_color,
                    cursor="hand2"
                )
                img_button.pack()

                title_label = tk.Label(
                    img_container, text=title[:50] + "..." if len(title) > 50 else title,
                    font=self.style.title_font, bg=self.style.bg_color, fg=self.style.fg_color
                )
                title_label.pack()

                self.images_frame.update()
                self.log(f"Załadowano obraz: '{title[:50]}'")
                col += 1
                if col >= col_count:
                    col = 0
                    row += 1
                shown += 1
                return shown < 9
            except Exception as e:
                self.handle_request_errors(e, f"ładowaniu obrazu '{title[:50]}'")
                return True

        def process_next_image(index=0):
            if index >= len(items) or not load_image(items[index]):
                if loading_label.winfo_exists():
                    loading_label.destroy()
                self.log("Zakończono ładowanie obrazów.")
                return
            root.after(10, process_next_image, index + 1)

        self.log("Rozpoczęto ładowanie obrazów.")
        root.after(100, process_next_image)

    def _open_image_window(self, img_url):
        try:
            img_data = requests.get(img_url).content
            image = Image.open(BytesIO(img_data))
            win = tk.Toplevel(self.parent)
            win.title("Podgląd zdjęcia")
            win.configure(bg=self.style.bg_color)

            img_width, img_height = image.size
            if img_width > 1000 or img_height > 800:
                image.thumbnail((1000, 800))

            photo = ImageTk.PhotoImage(image)
            label = tk.Label(win, image=photo, bg=self.style.bg_color)
            label.image = photo
            label.pack()
        except Exception as e:
            self.handle_request_errors(e, "otwieraniu obrazu")

# Główna klasa aplikacji
class FetchNasaImagesApp(NasaAppBase):
    def __init__(self, root):
        self.style = StyleConfig()
        super().__init__(self.style)
        self.root = root
        self.root.title("NASA Image Search")
        self.base_url = "https://images-api.nasa.gov/search"
        self.root.configure(bg=self.style.bg_color)
        self.search_panel = SearchPanel(self.root, self.style, self.search_images)
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.style.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg=self.style.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(main_frame, width=300, bg=self.style.bg_color)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_panel = LogPanel(right_frame, self.style)
        self.image_grid = ImageGrid(left_frame, self.style, self.log_panel.log)

    def search_images(self, query):
        self.image_grid.clear_images()
        self.log(f"Wyszukiwanie: {query}")

        try:
            params = {'q': query, 'media_type': 'image'}
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()
            items = data.get("collection", {}).get("items", [])
            if not items:
                self.log("Brak wyników dla danego wyszukiwania.")
                return

            self.log(f"Znaleziono {len(items)} wyników. Wyświetlam maksymalnie 9 obrazów.")
            self.image_grid.display_images(items, self.root)
        except Exception as e:
            self.handle_request_errors(e, "wyszukiwaniu")

def main():
    root = tk.Tk()
    app = FetchNasaImagesApp(root)
    root.geometry("1200x800")
    root.mainloop()

if __name__ == "__main__":
    main()