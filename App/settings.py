import streamlit as st
import os
from datetime import datetime as dt
from datetime import timedelta
from streamlit.components.v1 import html
import streamlit_antd_components as sac

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json


class Settings():

    def __init__(self, session):
        self.session = session
        
        local_desc = 'settingAs'
        if local_desc not in self.session:
            self.local = {}
            self.session[local_desc] = self.local
        else:
            self.local = self.session[local_desc]

        st.markdown(
            """
            <style>
            .block-container .css-12oz5g7{
                padding-top: 1rem;
                padding-right: 12rem;
                padding-left: 12rem;
                padding-bottom: 5rem;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )
        
        st.markdown(
            """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """,
            unsafe_allow_html=True,
        )

        self.session.current_page= local_desc
        
        content = st.empty()
        with content.container():
            self.load()
    
    def redirect(self, page):
        self.session['redirect'] = page
        st.experimental_rerun()
        
    def redirect_carry(self, page, data):
        self.session['redirect'] = page
        
        self.session['redirect_carry'] = {'status':'success', 'data': data}
        #st.rerun()        

        
    def open_page(self, url):
        open_script= """
            <script type="text/javascript">
                window.open('%s', '_blank').focus();
            </script>
        """ % (url)
        html(open_script)

    def load(self):
        st.title('Settings')
        
        CONFIG_FILE = "././config_data.json"  # Fester Pfad zur Konfigurationsdatei im selben Verzeichnis
        
        # Funktion zum Laden der Konfigurationsdatei
        def load_config():
            if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
                with open(CONFIG_FILE, "r") as config_file:
                    return json.load(config_file)
            else:
                return {}
        
        # Funktion zum Speichern der Konfigurationsdatei
        def save_config(config):
            with open(CONFIG_FILE, "w") as config_file:
                json.dump(config, config_file)
        
        # Funktion zum Extrahieren des letzten Ordners aus einem Verzeichnispfad
        def get_last_folder(path):
            return os.path.basename(path.rstrip('/'))
        
        # Anwendung
        config = load_config()
        
        st.write("Geben Sie bis zu 6 Verzeichnispfade ein, um sie zu speichern.")
        
        folder_paths = []
        for i in range(1, 7):
            folder_path = st.text_input(f"Verzeichnispfad {i}:", config.get(f"path{i}", ""))
            folder_paths.append(folder_path)
        
        # Initialisiere den Passwortzustand, wenn er nicht bereits existiert
        if "password_input" not in st.session_state:
            st.session_state["password_input"] = ""
        
        if "message" not in st.session_state:
            st.session_state["message"] = ""
        if "message_type" not in st.session_state:
            st.session_state["message_type"] = ""
        
        # Passwortfeld anzeigen
        password = st.text_input("Passwort eingeben:", type="password")
        
        if st.button("Speichern"):
            if password:
                if password == "dein_passwort":  # Ersetze 'dein_passwort' durch das tatsächliche Passwort
                    config = {f"path{i+1}": folder_paths[i] for i in range(6)}
                    save_config(config)
                    st.session_state["message"] = "Passwort korrekt! Konfiguration gespeichert!"
                    st.session_state["message_type"] = "success"
                else:
                    st.session_state["message"] = "Passwort nicht korrekt! Konfiguration konnte nicht gespeichert werden."
                    st.session_state["message_type"] = "error"
                # Passwortfeld leeren durch Neuinitialisierung
                st.session_state["password_input"] = ""
                st.experimental_rerun()  # Anwendung neu laden, um das Passwortfeld zu leeren
            else:
                st.warning("Bitte geben Sie ein Passwort ein.")
        
        if st.session_state["message"]:
            if st.session_state["message_type"] == "success":
                st.success(st.session_state["message"])
            elif st.session_state["message_type"] == "error":
                st.error(st.session_state["message"])
            # Zurücksetzen der Nachricht, nachdem sie angezeigt wurde
            st.session_state["message"] = ""
            st.session_state["message_type"] = ""
        
        st.markdown("**Aktuelle Konfiguration:**")
        for i in range(6):
            path = config.get(f'path{i+1}', '')
            if path:  # Nur wenn der Pfad nicht leer ist
                last_folder = get_last_folder(path)
                st.write(f"Verzeichnispfad {i+1}: {last_folder}")
                
        
        """
        CONFIG_FILE = "././config_data.json"  # Fester Pfad zur Konfigurationsdatei im selben Verzeichnis

        if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
            with open(CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
        else:
            config = {}
            st.write("Aktuelle Konfiguration:")
        st.write("Geben Sie bis zu 6 Verzeichnispfade ein, um sie zu speichern.")
        
        folder_paths = []
        for i in range(1, 7):
            folder_path = st.text_input(f"Verzeichnispfad {i}", config.get(f"path{i}", ""))
            folder_paths.append(folder_path)
        
        # Initialisiere den Passwortzustand, wenn er nicht bereits existiert
        if "password_input" not in st.session_state:
            st.session_state["password_input"] = ""
        
        # Passwortfeld anzeigen
        password = st.text_input("Passwort eingeben", type="password")
        
        if st.button("Speichern"):
            if password:
                if password == "dein_passwort":  # Ersetze 'dein_passwort' durch das tatsächliche Passwort
                    config = {f"path{i+1}": folder_paths[i] for i in range(6)}
                    with open(CONFIG_FILE, "w") as config_file:
                        json.dump(config, config_file)
                    st.success("Passwort korrekt! Konfiguration gespeichert!")
                    # Passwortfeld leeren durch Neuinitialisierung
                    password = ""
                else:
                    st.error("Passwort nicht korrekt! Konfiguration konnte nicht gespeichert werden.")
                    # Passwortfeld leeren durch Neuinitialisierung
                    password = ""
            else:
                st.warning("Bitte geben Sie ein Passwort ein.")
        
        st.write("Aktuelle Konfiguration:")
        for i in range(6):
            st.write(f"Verzeichnispfad {i+1}: {config.get(f'path{i+1}', 'Nicht konfiguriert')}")
        """
