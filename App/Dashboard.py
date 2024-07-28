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
from glob import glob

from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import base64
import shutil
import pytz



class Dashboard():

    def __init__(self, session):
        self.session = session
        
        local_desc = 'dashboard'
        if local_desc not in self.session:
            self.local = {}
            self.session[local_desc] = self.local
        else:
            self.local = self.session[local_desc]
            
        if 'rename_flag' not in self.session:
          self.session['rename_flag'] = False

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
        st.rerun()
        
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
        
    def change_name(self, selected_file):
        new_file_path = os.path.splitext(selected_file)[0] + "_LFP.xlsx"
        
        os.rename(selected_file, new_file_path)
        
        self.local['change_name_success'] = new_file_path
        self.local.pop('show_xls')
        

    def load(self):
        st.title('Dashboard')
        
        def find_latest_excel_files(root_dir, n=5):
            files = glob(os.path.join(root_dir, '**', '*.xlsx'), recursive=True)
            files.sort(key=os.path.getmtime, reverse=True)
            # Filter out files with '_LFP' in their name
            filtered_files = [file for file in files if '_LFP' not in file]
            return filtered_files[:n]
        
        
        def format_path(path):
            return os.path.basename(os.path.normpath(path))
        
        # CSS zur Anpassung der Tabellen
        css = """
        <style>
            .dataframe table {
                width: 100% !important;
                table-layout: fixed !important;
            }
            .dataframe td, .dataframe th {
                font-size: smaller !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
            }
        </style>
        """
        
        # Einfügen des CSS in die Streamlit-App
        st.markdown(css, unsafe_allow_html=True)
        
        # Konfigurationsdatei laden
        with open("././config_data.json", 'r') as file:
            config = json.load(file)
        
        # Dropdown zur Auswahl des Hauptpfades (nur letzter Ordnername anzeigen)
        st.title("Excel Dateiauswahl")
        config_paths = {format_path(value): value for key, value in config.items()}
        main_path_key = st.selectbox("Wählen Sie einen Pfad aus", list(config_paths.keys()))
        main_path = config_paths[main_path_key]
        
        # Abrufen der Excel-Dateien
        if main_path:
            try:
                latest_files = find_latest_excel_files(main_path, n=5)
                if not latest_files:
                    st.error("Keine Excel-Dateien gefunden.")
                else:
                    # Dateien in klickbaren Boxen anzeigen
                    st.write("Wählen Sie eine der letzten 5 Excel-Dateien aus:")
                    for file in latest_files:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.button(os.path.basename(file)):
                                self.local["show_xls"] = file
                        with col2:
                            utc_plus_2 = pytz.timezone('Europe/Berlin')

                            # Display the file modification time in UTC+2
                            st.write(pd.to_datetime(os.path.getmtime(file), unit='s').tz_localize(pytz.utc).tz_convert(utc_plus_2).strftime('%Y-%m-%d %H:%M:%S %Z%z'))
            except Exception as e:
                st.error(f"Fehler beim Abrufen der Excel-Dateien: {e}")
        
        # Excel-Datei anzeigen
        if 'show_xls' in self.local:
            selected_file = self.local['show_xls']
            try:
                st.write(f"**Ausgewählte Datei:** {os.path.basename(selected_file)}")
                df = pd.read_excel(selected_file, header=None)
        
                st.write("**Organisatorische Informationen (B1-B4):**")
                st.table(df.iloc[1:4, 0:2])  # Korrigiert auf Spalte B (1) bis C (2)
        
                tolerances = df.iloc[1:4, 3:10]
                parallelität_min = df.iloc[2, 4]
                parallelität_max = df.iloc[3, 4]
                winkel_min = df.iloc[2, 5]
                winkel_max = df.iloc[3, 5]
                drall_min = df.iloc[2, 6]
                drall_max = df.iloc[3, 6]
                gesamtlaenge_min = df.iloc[2, 7]
                gesamtlaenge_max = df.iloc[3, 7]
                abisolierlaenge_links_min = df.iloc[2, 8]
                abisolierlaenge_links_max = df.iloc[3, 8]
                abisolierlaenge_rechts_min = df.iloc[2, 9]
                abisolierlaenge_rechts_max = df.iloc[3, 9]
                
                tolerances = {"Parallelit\u00e4t": {"min": parallelität_min, "max": parallelität_max}, "Winkel": {"min": winkel_min, "max": winkel_max}, "Drall": {"min": drall_min, "max": drall_max}, "Gesamtl\u00e4nge links": {"min": gesamtlaenge_min, "max": gesamtlaenge_max}, "Abisolierl\u00e4nge links": {"min": abisolierlaenge_links_min, "max": abisolierlaenge_links_max}, "Gesamtl\u00e4nge rechts": {"min": gesamtlaenge_min, "max": gesamtlaenge_max}, "Abisolierl\u00e4nge rechts": {"min": abisolierlaenge_rechts_min, "max": abisolierlaenge_rechts_max}}
                # Festlegen der Zeilen mit numerischen Werten
                st.write("**Messwerte (D1-J4):**")
                measurement_rows = [8, 10, 12, 14]  # Zeilen 7-16
                measurements = df.iloc[measurement_rows, 0:9]  # Messwerte aus den Spalten A bis I
                # Setze die Spaltenüberschriften
                headers = list(df.iloc[7, 0:9])  # Überschriften aus Zeile 7
                    
                
                
                if len(headers) == len(measurements.columns):
                    measurements.columns = headers
                else:
                    st.error(f"Length mismatch: Expected {len(measurements.columns)} elements, got {len(headers)} elements")
        
                # Transponiere die Messwerte-Tabelle
                transposed_measurements = measurements.transpose()
        
                # Funktion zum Anwenden der Färbung basierend auf Toleranzwerten
                def apply_coloring(measurements, tolerances):
                    def color_cells(val, row):
                        min_tol = tolerances.get(row, {}).get("min", float('-inf'))
                        max_tol = tolerances.get(row, {}).get("max", float('inf'))
                        if isinstance(val, (int, float)):
                            if val < min_tol or val > max_tol:
                                return 'background-color: red'
                            else:
                                return 'background-color: green'
                        else:
                            return ''
                    
                    styled_df = measurements.style.apply(lambda x: pd.Series(
                        [color_cells(x[col], x.name) if x.name in tolerances else '' for col in x.index], 
                        index=x.index), axis=1)
                    return styled_df
                
                # Apply coloring based on tolerance values to transposed measurements
                styled_transposed_df = apply_coloring(transposed_measurements, tolerances)
        
                st.table(styled_transposed_df)
                
                st.button('Datei umbenennen', on_click= self.change_name, kwargs={'selected_file': selected_file})
                
                st.markdown('---')
            except Exception as e:
                st.write(str(e))
                    
        if 'change_name_success' in self.local:
            st.success('File change successfull')
            
            st.write(str(self.local['change_name_success']))
                    
                    
               
            
