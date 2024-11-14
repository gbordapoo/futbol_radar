#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 12:29:33 2023

@author: gustavoborda
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

from io import BytesIO


from mplsoccer import Radar, FontManager, grid, grid_dimensions

st.set_page_config(page_title='Performance Field - Radar',
                    page_icon="flag_chile",
                    layout = 'wide')


uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    excel_data = pd.ExcelFile(uploaded_file)
    sheet_names = excel_data.sheet_names

    selected_sheet = st.selectbox("Select a sheet", sheet_names)

    if selected_sheet:
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

        

        players = df['Jugador'].tolist()
# selected_player = st.selectbox("Select a player", players)

        headers_row = list(df.columns[1:])
# selected_values = st.multiselect("Select values from Row 1", headers_row)
    
        
        ####### added for getting the png file #######
        
        # Assuming you have a dataframe named 'df'
        # Add a new row with the average values
        average_row = df.mean(axis=0)
        # Set the 'Jugador' column of the average row to 'Promedio'
        average_row['Jugador'] = 'Promedio'
        df = df.append(average_row, ignore_index=True)

        ###############################################

        ########### SideBar

        def add_logo(logo_path, width, height):
            """Read and return a resized logo"""
            logo = Image.open(logo_path)
            modified_logo = logo.resize((width, height))
            return modified_logo
        
        st.sidebar.image(add_logo(logo_path="performancefield_logo.jpeg", width=150, height=120)) 
        
        st.sidebar.header('Filters:')

        select_player1 = st.sidebar.selectbox(
            "Select Player 1:",
            options=df['Jugador'].unique()
        )
        
        select_player2 = st.sidebar.selectbox(
            "Select the Player 2:",
            options=df['Jugador'].unique()
        )

        select_column = st.sidebar.multiselect(
            "Select the columns to include in the Radar:",
            options = list(df.columns[1:])
        )
        
        
        
        
        ##### Debug
        #st.write(select_column)
        #st.write(select_player)
        #####
        
        
        st.dataframe(df)

        # Read the Excel file and extract the value of cell C2
        value1 = select_player1
        value2 = select_player2
        
        options = [value1, value2]
        
        # # selecting rows based on condition
        df = df[df['Jugador'].isin(options)].reset_index()
        
       # st.dataframe(df)
        
        items = select_column
        
        #st.dataframe(items)
        
        items_with_jugador = ['Jugador'] + items
        df = df.filter(items=items_with_jugador, axis =1)
        
        #st.dataframe(df)
        
        # # get parameter

        params = list(df.columns)
        params = params[1:]   # get rid of the player column

        # # get minimum and maximum values of 

        # # add ranges to list of tuple pairs
        ranges = []
        a_values = []
        b_values = []
        
        # #for cicle to get the data and save it

        for x in params:
            a = min(df[params][x])
            a = a - (a*.25)
            
            b = max(df[params][x])
            b = b + (b*0.25)
            
            ranges.append((a,b))

        for x in range(len(df['Jugador'])):
            if df['Jugador'][x] == value1:
                a_values = df.iloc[x].values.tolist()
            if df['Jugador'][x] == value2:
                b_values = df.iloc[x].values.tolist()
                
        #st.write(a)
       # st.write(b)
        
        # # erases the name of the player
                 
        a_values = a_values[1:]
        b_values = b_values[1:]

        # define one array with the values

        values = [a_values,b_values]

        # sets the low and the high values for each param

        low = [tup[0] for tup in ranges]
        high = [tup[1] for tup in ranges]
        
        ##############################################################################
        # Instantiate the Radar Class
        # ---------------------------
        # We will instantiate a ``Radar`` object with the above parameters so that we can re-use it
        # several times.

        radar = Radar(params, low, high,
                      #lower_is_better=lower_is_better,
                      # whether to round any of the labels to integers instead of decimal places
                      round_int=[False]*len(params),
                      num_rings=4,  # the number of concentric circles (excluding center circle)
                      # if the ring_width is more than the center_circle_radius then
                      # the center circle radius will be wider than the width of the concentric circles
                      ring_width=1, center_circle_radius=1)

        ##############################################################################
        # Load some fonts
        # ---------------
        # We will use mplsoccer's ``FontManager`` to load some fonts from Google Fonts.
        # We borrowed the FontManager from the excellent
        # `ridge_map library <https://github.com/ColCarroll/ridge_map>`_.
        URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
                'SourceSerifPro-Regular.ttf')
        serif_regular = FontManager(URL1)
        URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
                'SourceSerifPro-ExtraLight.ttf')
        serif_extra_light = FontManager(URL2)
        URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
                'RubikMonoOne-Regular.ttf')
        rubik_regular = FontManager(URL3)
        URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
        robotto_thin = FontManager(URL4)
        URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                'RobotoSlab%5Bwght%5D.ttf')
        robotto_bold = FontManager(URL5)

        ##############################################################################

        # # Set the DPI and figure size
        dpi = 300
        
        #width = st.sidebar.slider("plot width", 0.1, 2500., 3.)
        #height = st.sidebar.slider("plot height", 0.1, 2500., 1.)

        # creating the figure using the grid function from mplsoccer:
        fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                        title_space=0, endnote_space=0, grid_key='radar', axis=False)
        
        #width, height = grid_dimensions(1, figwidth=width, figheight=height,
         #                                       nrows=1, ncols=1,
         #                                       max_grid=1,  space=0)


        color_1 = 'red'
        color_2 = 'blue'

        # plot radar
        radar.setup_axis(ax=axs['radar'])  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='white', edgecolor='gray')
        radar_output = radar.draw_radar_compare(a_values, b_values, ax=axs['radar'],
                                                kwargs_radar={'facecolor': color_1, 'alpha': 0.6},
                                                kwargs_compare={'facecolor': color_2, 'alpha': 0.6})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25,
                                               fontproperties=robotto_thin.prop)
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25,
                                               fontproperties=robotto_thin.prop)
        axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                             c=color_1, edgecolors=color_1, marker='o', s=50, zorder=2)
        axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                             c=color_2, edgecolors=color_2, marker='o', s=50, zorder=2)

        # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
        # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
        endnote_text = axs['endnote'].text(0.99, 0.5, 'Viz by: @gbordapoo / @performancefield', fontsize=15,
                                           fontproperties=robotto_thin.prop, ha='right', va='center')
        title1_text = axs['title'].text(0.01, 0.65, value1, fontsize=25, color=color_1,
                                        fontproperties=robotto_bold.prop, ha='left', va='center')
        title2_text = axs['title'].text(0.01, 0.25, '', fontsize=20,
                                        fontproperties=robotto_thin.prop,
                                        ha='left', va='center', color=color_1)
        title3_text = axs['title'].text(0.99, 0.65, value2, fontsize=25,
                                        fontproperties=robotto_bold.prop,
                                        ha='right', va='center', color=color_2)
        title4_text = axs['title'].text(0.99, 0.25, '', fontsize=20,
                                        fontproperties=robotto_thin.prop,
                                        ha='right', va='center', color=color_2)
        
        #fig.set_size_inches(10, 6)  # Set your desired width and height here
        
        # buf = BytesIO()
        # fig.savefig(buf, format="png")
        # st.image(buf)
        
        
        
        #st.pyplot(fig)
        # Save the figure to a BytesIO object as PNG
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)  # Reset the buffer to the beginning

# Display the saved image using st.image()
        st.image(buf, caption='', use_column_width=True)

# Create a download button for the image
    st.download_button(
        label="Download Image",
        data=buf,
        file_name="radar_" + value1 + "_" + value2 + ".png",
        mime="image/png"
        )
        
        

