import customtkinter as ctk
import tkinter as tk
import requests
import os
import shutil
import webbrowser
import subprocess

# Configuration de base CustomTkInter avec accent personnalisé violet
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Use a default theme

# Chemins où les thèmes et scripts seront sauvegardés
user_folder = os.path.expanduser("~")  # Récupère le dossier utilisateur actuel
themes_folder = os.path.join(user_folder, "AppData", "Roaming", "breeze", "themes")
scripts_folder = os.path.join(user_folder, "AppData", "Roaming", "breeze", "scripting", "scripts")

# Modifier la couleur d'accent en violet
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.CTkButton._fg_color = "purple"

# Fonction pour obtenir les fichiers dans un dossier du repo GitHub
def get_files_from_repo(repo_url, folder_name):
    print(f"Fetching files from {repo_url}/{folder_name}")
    api_url = f"{repo_url}/contents/{folder_name}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        files = response.json()
        file_names = [file['name'] for file in files if file['name'].endswith('.toml')]
        print(f"Found files: {file_names}")
        return file_names, files  # Return file names and complete file info
    else:
        print(f"Error fetching files. Status code: {response.status_code}")
        status_label.configure(text=f"Error fetching files from {folder_name}.")
        return [], []

# Fonction pour télécharger un fichier spécifique depuis le repo GitHub
def download_file(file_info, dest_folder):
    download_url = file_info['download_url']
    file_name = file_info['name']
    print(f"Downloading {file_name} from {download_url}")

    response = requests.get(download_url)
    if response.status_code == 200:
        os.makedirs(dest_folder, exist_ok=True)
        file_path = os.path.join(dest_folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {file_name} to {file_path}")
        status_label.configure(text=f"Downloaded: {file_name}")
    else:
        print(f"Error downloading {file_name}. Status code: {response.status_code}")
        status_label.configure(text=f"Error downloading {file_name}.")

# Fonction pour lister les fichiers dans le Listbox pour les thèmes
def list_themes(repo_url):
    print("Listing themes...")
    theme_listbox.delete(0, tk.END)
    file_names, file_infos = get_files_from_repo(repo_url, "themes")
    
    for file_name in file_names:
        theme_listbox.insert(tk.END, file_name)

    # Store file info for future download reference
    theme_listbox.file_infos = file_infos  # Attach the complete file information to the Listbox

# Fonction pour lister les fichiers dans le Listbox pour les scripts
def list_scripts(repo_url):
    print("Listing scripts...")
    script_listbox.delete(0, tk.END)
    file_names, file_infos = get_files_from_repo(repo_url, "scripts")
    
    for file_name in file_names:
        script_listbox.insert(tk.END, file_name)

    # Store file info for future download reference
    script_listbox.file_infos = file_infos  # Attach the complete file information to the Listbox

# Fonction pour télécharger les thèmes sélectionnés
def download_selected_themes():
    try:
        selected_idxs = theme_listbox.curselection()
        if selected_idxs:
            for idx in selected_idxs:
                selected_file_info = theme_listbox.file_infos[idx]
                download_file(selected_file_info, themes_folder)
        else:
            print("No theme selected.")
            status_label.configure(text="No theme selected.")
    except tk.TclError:
        print("Error during theme selection.")
        status_label.configure(text="Error during theme selection.")

# Fonction pour télécharger les scripts sélectionnés
def download_selected_scripts():
    try:
        selected_idxs = script_listbox.curselection()
        if selected_idxs:
            for idx in selected_idxs:
                selected_file_info = script_listbox.file_infos[idx]
                download_file(selected_file_info, scripts_folder)
        else:
            print("No script selected.")
            status_label.configure(text="No script selected.")
    except tk.TclError:
        print("Error during script selection.")
        status_label.configure(text="Error during script selection.")

# Ouvrir les dossiers thèmes et scripts
def open_themes_directory():
    path = os.path.realpath(themes_folder)
    subprocess.Popen(f'explorer "{path}"')

def open_scripts_directory():
    path = os.path.realpath(scripts_folder)
    subprocess.Popen(f'explorer "{path}"')

# Ouvrir les repositories GitHub
def open_github_themes_repo():
    webbrowser.open("https://github.com/planetwiide/breeze-themes")

def open_github_scripts_repo():
    webbrowser.open("https://github.com/planetwiide/breeze-scripts")

# Interface principale
app = ctk.CTk()
app.geometry("690x900")
app.title("〆 v1.0.1 © @planetwiide | breeze-hub 〆")

# Ajout de l'icône
app.iconbitmap("ico.png")

# Label principal
label = ctk.CTkLabel(app, text="々 breeze hub 々", font=("Arial", 20))
label.pack(pady=10)

# Boutons pour lister les fichiers dans le répertoire GitHub
theme_button = ctk.CTkButton(app, text="list themes", command=lambda: list_themes("https://api.github.com/repos/planetwiide/breeze-themes"))
theme_button.pack(pady=10)

script_button = ctk.CTkButton(app, text="list scripts", command=lambda: list_scripts("https://api.github.com/repos/planetwiide/breeze-scripts"))
script_button.pack(pady=10)

# Listbox pour afficher les thèmes du repo (multiselection)
theme_label = ctk.CTkLabel(app, text="themes", font=("Arial", 16))
theme_label.pack(pady=5)
theme_listbox = tk.Listbox(app, height=10, selectmode=tk.MULTIPLE)
theme_listbox.pack(pady=10)

# Bouton pour télécharger les thèmes sélectionnés
download_theme_button = ctk.CTkButton(app, text="download selected themes", command=download_selected_themes)
download_theme_button.pack(pady=5)

# Listbox pour afficher les scripts du repo (multiselection)
script_label = ctk.CTkLabel(app, text="scripts", font=("Arial", 16))
script_label.pack(pady=5)
script_listbox = tk.Listbox(app, height=10, selectmode=tk.MULTIPLE)
script_listbox.pack(pady=10)

# Bouton pour télécharger les scripts sélectionnés
download_script_button = ctk.CTkButton(app, text="download selected scripts", command=download_selected_scripts)
download_script_button.pack(pady=5)

# Boutons pour ouvrir les répertoires locaux
open_themes_button = ctk.CTkButton(app, text="open your installed themes directory", command=open_themes_directory)
open_themes_button.pack(pady=5)

open_scripts_button = ctk.CTkButton(app, text="open your installed scripts directory", command=open_scripts_directory)
open_scripts_button.pack(pady=5)

# Boutons pour ouvrir les repositories GitHub
open_themes_repo_button = ctk.CTkButton(app, text="open themes github", command=open_github_themes_repo)
open_themes_repo_button.pack(pady=5)

open_scripts_repo_button = ctk.CTkButton(app, text="open scripts github", command=open_github_scripts_repo)
open_scripts_repo_button.pack(pady=5)

# Label de crédit
credit_label = ctk.CTkLabel(app, text="2024 © planetwiide, mit lisence", font=("Arial", 14))
credit_label.pack(pady=10)

# Label de statut
status_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
status_label.pack(pady=10)

# Lancer l'application
app.mainloop()
