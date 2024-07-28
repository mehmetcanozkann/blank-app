import streamlit as st
import os
from datetime import datetime as dt
from datetime import timedelta
from streamlit.components.v1 import html
import streamlit_antd_components as sac

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class LandingPage():

    def __init__(self, session):
        self.session = session
        
        local_desc = 'landingpage'
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
        st.title('LandingPage')
        
