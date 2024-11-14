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
from mplsoccer import Radar

# Set page config for Streamlit
st.set_page_config(page_title='Performance Field - Radar',
                   page_icon="flag_chile",
                   layout='wide')

# Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    excel_data = pd.ExcelFile(uploaded_file)
    sheet_names = excel_data.sheet_names
    selected_sheet = st.selectbox("Select a sheet", sheet_names)

    if selected_sheet:
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)

        # Get list of players and filter data
        players = df['Jugador'].tolist()

        # Select columns for Radar chart
        headers_row = list(df.columns[1:])

        # Calculate average row (promedio)
        average_row = df.select_dtypes(include=['number']).mean(axis=0)
        average_row['Jugador'] = 'Promedio'
        df = pd.concat([df, pd.DataFrame([average_row])], ignore_index=True)  # Use concat instead of append

        # Sidebar for user filters
        def add_logo(logo_path, width, height):
            """Read and return a resized logo"""
            logo = Image.open(logo_path)
            return logo.resize((width, height))

        st.sidebar.image(add_logo("performancefield_logo.jpeg", width=150, height=120)) 
        st.sidebar.header('Filters:')
        
        select_player1 = st.sidebar.selectbox("Select Player 1:", options=df['Jugador'].unique())
        select_player2 = st.sidebar.selectbox("Select Player 2:", options=df['Jugador'].unique())
        select_column = st.sidebar.multiselect("Select the columns to include in the Radar:", options=list(df.columns[1:]))

        st.dataframe(df)

        # Filter dataframe for selected players
        df = df[df['Jugador'].isin([select_player1, select_player2])].reset_index(drop=True)

        # Filter selected columns
        columns_to_include = ['Jugador'] + select_column
        df_filtered = df[columns_to_include]

        # Get parameters for the radar chart (without 'Jugador' column)
        params = df_filtered.columns[1:]

        # Define min/max ranges for each parameter
        ranges = [(min(df_filtered[param]) - min(df_filtered[param]) * 0.25, 
                   max(df_filtered[param]) + max(df_filtered[param]) * 0.25) 
                  for param in params]

        # Get player values for radar chart
        player1_values = df_filtered[df_filtered['Jugador'] == select_player1].iloc[0, 1:].values
        player2_values = df_filtered[df_filtered['Jugador'] == select_player2].iloc[0, 1:].values

        # Extract min/max values for radar axis scaling
        low = [r[0] for r in ranges]
        high = [r[1] for r in ranges]

        # Initialize radar chart
        radar = Radar(params, low, high, num_rings=4, ring_width=1, center_circle_radius=1)

        # Create the plot with simplified layout
        fig, ax = plt.subplots(figsize=(14, 10))  # Adjust the figure size directly without grid

        color_1 = 'red'
        color_2 = 'blue'

        # Plot radar chart
        radar.setup_axis(ax=ax)
        radar.draw_circles(ax=ax, facecolor='white', edgecolor='gray')
        radar_output = radar.draw_radar_compare(player1_values, player2_values, ax=ax,
                                                kwargs_radar={'facecolor': color_1, 'alpha': 0.6},
                                                kwargs_compare={'facecolor': color_2, 'alpha': 0.6})

        # Draw range and parameter labels with default font
        radar.draw_range_labels(ax=ax, fontsize=15)  # Set a readable font size
        radar.draw_param_labels(ax=ax, fontsize=15)

        # Add title and endnote text with default font
        ax.text(0.01, 0.65, select_player1, fontsize=18, color=color_1, ha='left', va='center')
        ax.text(0.99, 0.65, select_player2, fontsize=18, color=color_2, ha='right', va='center')
        #ax.text(0.99, 0.5, 'Viz by: @gbordapoo / @performancefield', fontsize=12,
                ha='right', va='center')

        # Save the figure to a BytesIO object as PNG
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)  # Reset the buffer to the beginning

        # Display the radar chart image
        st.image(buf, caption='', use_column_width=True)

        # Create a download button for the image
        st.download_button(
            label="Download Image",
            data=buf,
            file_name=f"radar_{select_player1}_{select_player2}.png",
            mime="image/png"
        )
