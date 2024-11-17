from plotly import express as px
import pandas as pd
from datetime import datetime
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from plotly import graph_objects as go
import os

def plot_timeseries(data, x, y, title, x_title, y_title, file_path):
    if data[x].map(lambda x: isinstance(x, datetime)).all():
        data.set_index(x, inplace=True)
        data = data.resample('ME').count()
        data = data.reset_index()
        fig = px.line(data, x=x, y=y, title=title)
        fig.update_xaxes(title_text=x_title)
        fig.update_yaxes(title_text=y_title)
        fig.show()
        fig.write_html(file_path)
    else:
        print('Error: x-axis must be a datetime object')	


def plot_wordcloud(text, file_path):
    #create wordcloud
    wordcloud = WordCloud(
        width=1500, height=600,
        background_color='white',
        colormap="copper",
        contour_width=1,
        contour_color='brown',
        random_state=2
    ).generate(text)
    #save & load
    wordcloud.to_file(file_path)


def plot_timeseries_with_annotations(data, x, y, title, x_title, y_title, annotations, wordcloud_file_path=None):
    
    # Ensure data has the correct index and is reset
    data = data.reset_index()

    # Create figure
    fig = go.Figure()

    # Add word cloud image as a background if the file exists
    if wordcloud_file_path and os.path.exists(wordcloud_file_path):
        img = Image.open(wordcloud_file_path)
        fig.add_layout_image(
            dict(
                source=img,
                xref="paper", yref="paper",
                x=0, y=1,
                sizex=1, sizey=1,
                xanchor="left", yanchor="top",
                opacity=0.13,
                layer="below"
            )
        )
    if data[x].map(lambda x: isinstance(x, datetime)).all():
        data.set_index(x, inplace=True)
        data = data.resample('ME').count()
        data = data.reset_index()
    # Add line trace
    fig.add_trace(
        go.Scatter(
            x=data[x],
            y=data[y],
            mode='lines',
            line=dict(color='#8c564b'),
            name="Number of Edits"
        )
    )

    # Add scatter trace for data points with colorscale applied
    fig.add_trace(
        go.Scatter(
            x=data[x],
            y=data[y],
            mode='markers',
            marker=dict(
                color=data[y],  # Apply the numerical values as colors
                colorscale='rdbu',  # Define the colorscale
                showscale=True,  # Show the colorbar
                line=dict(width=0.5, color='black')
            ),
            name="Data Points"
        )
    )

    # Update layout with title, axes labels, and font styles
    fig.update_layout(
        title_text=title,
        title_x=0.5,
        xaxis=dict(title=x_title),
        yaxis=dict(title=y_title),
        title_font=dict(size=35),
        annotations=[
            dict(
                x=annotation["x"],
                y=annotation["y"],
                text=annotation["text"],
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                font=dict(size=15, color="#5D4037"),
                bgcolor="#CCA677"
            ) for annotation in annotations
        ],
        font_family="Raleway",
        font_color="#5D4037",
        width=1200,
        height=600
    )

    # Hide legend if needed
    fig.update_layout(showlegend=False)

    # Display the figure
    fig.show()


def create_bar_plot(df, categories, series, colors, title, yaxis_title, percent_change_base=None):
    """
    Creates a grouped bar plot with optional percent change annotations.

    Parameters:
    - df (pd.DataFrame): The data for plotting.
    - categories (str): The column representing categories on the x-axis.
    - series (list): List of column names to plot as bars.
    - colors (list): List of colors for each series.
    - title (str): The title of the plot.
    - yaxis_title (str): Label for the y-axis.
    - percent_change_base (dict): Base values for percent change calculation {series_name: base_value}.
    """
    def calculate_percent_change(before, after):
        if before == 0:
            return "N/A"
        return f"+{((after - before) / before * 100):.0f}%"

    fig = go.Figure()

    for i, col in enumerate(series):
        base_value = percent_change_base.get(col) if percent_change_base else None
        annotations = [
            f"{y}<br>({calculate_percent_change(base_value, y)})" if base_value and idx == 1 else y
            for idx, y in enumerate(df[col])
        ]
        
        fig.add_trace(
            go.Bar(
                name=col,
                x=df[categories],
                y=df[col],
                text=annotations,
                textposition='auto',
                marker_color=colors[i],
                opacity=0.95,
                width=0.3
            )
        )

    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24}
        },
        yaxis_title=yaxis_title,
        showlegend=True,
        legend={'orientation': 'h', 'y': -0.2},
        template='plotly_white',
        barmode='group',
        hoverlabel=dict(bgcolor="white"),
        margin=dict(t=50, b=50),
        height=500,
        font_family="Raleway",
        font_color="#5D4037",
    )
    return fig
