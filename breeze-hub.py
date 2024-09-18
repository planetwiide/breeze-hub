import customtkinter as ctk
import tkinter as tk
import requests
import os
import shutil
import webbrowser
import subprocess

# configure customtkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # set default theme to dark blue

# define paths for themes and scripts storage
user_folder = os.path.expanduser("~")  # get current user folder
themes_folder = os.path.join(user_folder, "AppData", "Roaming", "breeze", "themes")
scripts_folder = os.path.join(user_folder, "AppData", "Roaming", "breeze", "scripting", "scripts")

# change the accent color to purple
ctk.CTkButton._fg_color = "purple"

# function to get files from a specified GitHub repository folder
def get_files_from_repo(repo_url, folder_name):
    print(f"fetching files from {repo_url}/{folder_name}")
    api_url = f"{repo_url}/contents/{folder_name}"  # construct API URL
    response = requests.get(api_url)
    
    if response.status_code == 200:
        files = response.json()
        # filter for .toml and .js files
        file_names = [file['name'] for file in files if file['name'].endswith('.toml') or file['name'].endswith('.js')]
        print(f"found files: {file_names}")
        return file_names, files  # return file names and complete file info
    else:
        print(f"error fetching files. status code: {response.status_code}")
        status_label.configure(text=f"error fetching files from {folder_name}.")
        return [], []

# function to download a specific file from the GitHub repository
def download_file(file_info, dest_folder):
    download_url = file_info['download_url']
    file_name = file_info['name']
    print(f"downloading {file_name} from {download_url}")

    response = requests.get(download_url)
    if response.status_code == 200:
        os.makedirs(dest_folder, exist_ok=True)  # create destination folder if it doesn't exist
        file_path = os.path.join(dest_folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)  # write file content
        print(f"downloaded {file_name} to {file_path}")
        status_label.configure(text=f"downloaded: {file_name}")
    else:
        print(f"error downloading {file_name}. status code: {response.status_code}")
        status_label.configure(text=f"error downloading {file_name}.")

# function to list themes in the listbox
def list_themes(repo_url):
    print("listing themes...")
    theme_listbox.delete(0, tk.END)  # clear the listbox
    file_names, file_infos = get_files_from_repo(repo_url, "themes")
    
    for file_name in file_names:
        theme_listbox.insert(tk.END, file_name)  # insert file names into the listbox

    theme_listbox.file_infos = file_infos  # attach file info for future reference

# function to list scripts in the listbox
def list_scripts():
    print("listing scripts...")
    script_listbox.delete(0, tk.END)  # clear the listbox
    repo_url = "https://api.github.com/repos/planetwiide/breeze-scripts"  # define repo URL
    file_names, file_infos = get_files_from_repo(repo_url, "scripts")
    
    for file_name in file_names:
        script_listbox.insert(tk.END, file_name)  # insert file names into the listbox

    script_listbox.file_infos = file_infos  # attach file info for future reference

# function to download selected themes
def download_selected_themes():
    try:
        selected_idxs = theme_listbox.curselection()  # get selected indices
        if selected_idxs:
            for idx in selected_idxs:
                selected_file_info = theme_listbox.file_infos[idx]
                download_file(selected_file_info, themes_folder)  # download each selected theme
        else:
            print("no theme selected.")
            status_label.configure(text="no theme selected.")
    except tk.TclError:
        print("error during theme selection.")
        status_label.configure(text="error during theme selection.")

# function to download selected scripts
def download_selected_scripts():
    try:
        selected_idxs = script_listbox.curselection()  # get selected indices
        if selected_idxs:
            for idx in selected_idxs:
                selected_file_info = script_listbox.file_infos[idx]
                download_file(selected_file_info, scripts_folder)  # download each selected script
        else:
            print("no script selected.")
            status_label.configure(text="no script selected.")
    except tk.TclError:
        print("error during script selection.")
        status_label.configure(text="error during script selection.")

# function to open the themes directory in explorer
def open_themes_directory():
    path = os.path.realpath(themes_folder)
    subprocess.Popen(f'explorer "{path}"')

# function to open the scripts directory in explorer
def open_scripts_directory():
    path = os.path.realpath(scripts_folder)
    subprocess.Popen(f'explorer "{path}"')

# function to open the GitHub themes repository in a web browser
def open_github_themes_repo():
    webbrowser.open("https://github.com/planetwiide/breeze-themes")

# function to open the GitHub scripts repository in a web browser
def open_github_scripts_repo():
    webbrowser.open("https://github.com/planetwiide/breeze-scripts")

# main application interface
app = ctk.CTk()
app.configure(bg='black')  # set background color
app.geometry("690x900")  # set window size
app.title("〆 v1.0.1 © @planetwiide | breeze-hub 〆")  # set window title

# main label
label = ctk.CTkLabel(app, text="々 breeze hub 々", font=("Arial", 20))
label.pack(pady=10)

# buttons to list files from GitHub
theme_button = ctk.CTkButton(app, text="list themes", command=lambda: list_themes("https://api.github.com/repos/planetwiide/breeze-themes"), fg_color="#1d0057", hover_color="#3c2a7d")
theme_button.pack(pady=10)

script_button = ctk.CTkButton(app, text="list scripts", command=list_scripts, fg_color="#1d0057", hover_color="#3c2a7d")
script_button.pack(pady=10)

# listbox for themes
theme_label = ctk.CTkLabel(app, text="themes", font=("Arial", 16))
theme_label.pack(pady=5)
theme_listbox = tk.Listbox(app, height=10, width=50, selectmode=tk.MULTIPLE, bg="#2b2b2b", fg="white")  # multi-selection listbox
theme_listbox.pack(pady=10)

# button to download selected themes
download_theme_button = ctk.CTkButton(app, text="download selected themes", command=download_selected_themes, fg_color="#1d0057", hover_color="#3c2a7d")
download_theme_button.pack(pady=5)

# listbox for scripts
script_label = ctk.CTkLabel(app, text="scripts", font=("Arial", 16))
script_label.pack(pady=5)
script_listbox = tk.Listbox(app, height=10, width=50, selectmode=tk.MULTIPLE, bg="#2b2b2b", fg="white")  # multi-selection listbox
script_listbox.pack(pady=10)

# button to download selected scripts
download_script_button = ctk.CTkButton(app, text="download selected scripts", command=download_selected_scripts, fg_color="#1d0057", hover_color="#3c2a7d")
download_script_button.pack(pady=5)

# buttons to open local directories
open_themes_button = ctk.CTkButton(app, text="open themes directory", command=open_themes_directory, fg_color="#1d0057", hover_color="#3c2a7d")
open_themes_button.pack(pady=5)

open_scripts_button = ctk.CTkButton(app, text="open scripts directory", command=open_scripts_directory, fg_color="#1d0057", hover_color="#3c2a7d")
open_scripts_button.pack(pady=5)

# buttons to open GitHub repositories
open_themes_repo_button = ctk.CTkButton(app, text="open themes github", command=open_github_themes_repo, fg_color="#1d0057", hover_color="#3c2a7d")
open_themes_repo_button.pack(pady=5)

open_scripts_repo_button = ctk.CTkButton(app, text="open scripts github", command=open_github_scripts_repo, fg_color="#1d0057", hover_color="#3c2a7d")
open_scripts_repo_button.pack(pady=5)

# credit label
credit_label = ctk.CTkLabel(app, text="2024 © planetwiide", font=("Arial", 14))
credit_label.pack(pady=10)

# status label
status_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
status_label.pack(pady=10)

# start the application
app.mainloop()
