# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 22:31:03 2019

@author: shijo
"""

import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

from PIL import Image
import pytesseract
from wand.image import Image as Img
import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])


def parse_contents(contents, filename, date):
    with Img(filename=filename, resolution = 300) as img:
        img.compression_quality = 99
        img.save(filename='uploaded_file.jpg')
        demo = Image.open("uploaded_file.jpg")
        text = pytesseract.image_to_string(demo, lang = 'eng')
    #print(text)
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.H5("The OCR read words are below"),
        html.Div(text),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children




#demo = Image.open("example.png")
#text = pytesseract.image_to_string(demo, lang = 'eng')
#print(text)

#example = text
#def preprocess(sent):
#    sent = nltk.word_tokenize(sent)
#    sent = nltk.pos_tag(sent)
#    return sent


#sent = preprocess(example)
#print(sent)







if __name__ == '__main__':
    app.run_server(debug=True)