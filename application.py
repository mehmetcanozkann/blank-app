import streamlit as st
#from st_on_hover_tabs import on_hover_tabs
import os

from utils.hover_component import on_hover_tabs
from App.Dashboard import Dashboard
from App.LandingPage import LandingPage
from App.settings import Settings

#os.environ["HTTP_PROXY"]= "127.0.0.1:3128"  #"172.19.160.1:8080"
#os.environ["HTTPS_PROXY"]= "127.0.0.1:3128" #"172.19.160.1:8080"

os.environ["THIS_V"] = '0.0.8'
os.environ["THIS_DT"] = '23.01.2024'

class App():
    def __init__(self, setup):
        self.session = st.session_state
        self.selection = None
        
        hide_menu_style = """
            <style>s
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_menu_style, unsafe_allow_html=True)
        st.markdown('<style>' + open('./assets/style.css').read() + '</style>', unsafe_allow_html=True)
        st.markdown(f'''
                    <style>
                        .reportview-container .main .block-container {{
                            padding-top: 0rem;
                            padding-right: 10rem;
                            padding-left: 1rem;
                            padding-bottom: 10rem;
                        }}
                    </style>
                    ''', unsafe_allow_html=True,
        )
        
        if setup['landingpage']:
            self.session.current_page = 'landingpage'
            self.tab_settings ={'names': ['landingpage','dashboard','settings'],
                                'icons':['dashboard',  'view_in_ar', 'account_circle']
                                }
        else:
            self.session.current_page = 'dashboard'
            self.tab_settings = {'names': ['dashboard', 'settings'],
                                'icons': ['analytics', 'display_settings']
                                    }
            
            
        #Global Appearance
        st.markdown('<style>' + open('./assets/navbar.css').read() + '</style>', unsafe_allow_html=True)
        
        with open("./assets/global_layout.css") as f:
            css_header = f.read()
                                                                 
        st.markdown("""<div class="supergraphic"> </div>""", unsafe_allow_html=True)
        st.markdown(f"<style>{css_header}</style>", unsafe_allow_html=True)
        

    def run(self):

        with st.sidebar:
            tabs = on_hover_tabs(tabName=self.tab_settings['names'], iconName=self.tab_settings['icons'], default_choice=0)
        
        if self.selection != tabs and self.session.current_page:
            self.session['redirect'] = tabs

        #selection by button clicks
        if 'redirect' in self.session:
            self.selection = self.session['redirect']
            self.session.pop('redirect')
        
        #redirect to selected page
        if self.selection == "landingpage":
            LandingPage(session=self.session)
        elif self.selection == "dashboard":
            Dashboard(session = self.session)
        elif self.selection == "settings":
            Settings(session = self.session)
            
            
if __name__ == "__main__":
    st.set_page_config(
        page_title="MFI Data Apps",
        page_icon=":ballot box:", 
        layout="wide",
        menu_items={
            'Get Help': 'https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=805365928',
            'Report a bug': "https://inside-docupedia.bosch.com/confluence/pages/viewpage.action?pageId=805365928",
            'About': "# Easter Egg"
        }
    )
    
    setup = {'landingpage': False}
    app = App(setup)
    app.run()
