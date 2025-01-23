import dash
from dash import html, dcc, Input, Output, State
import dash_uploader as du
import os
from flask import Flask
import ai

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

du.configure_upload(app, UPLOAD_FOLDER, use_upload_id=False)

# App layout
app.layout = html.Div(
    style={
        "backgroundColor": "#f9f9f9",
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "textAlign": "center",
        "maxWidth": "600px",
        "margin": "0 auto",
        "borderRadius": "10px",
        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
    },
    children=[
        html.H1(
            "Object Identifier",
            style={"color": "#4CAF50", "marginBottom": "10px"},
        ),
        html.P(
            "Upload an image to identify the object and its usage.",
            style={"color": "#666", "fontSize": "16px"},
        ),
        du.Upload(
            id="uploader",
            text="Drag and drop or click to upload",
            max_files=1,
        ),
        html.Div(
            id="uploaded-file-path",
            style={
                "marginTop": "10px",
                "color": "#333",
                "fontWeight": "bold",
                "fontSize": "14px",
            },
        ),
        html.Button(
            "Submit",
            id="submit-btn",
            n_clicks=0,
            disabled=True,
            style={
                "marginTop": "20px",
                "padding": "10px 20px",
                "backgroundColor": "#4CAF50",
                "color": "#fff",
                "border": "none",
                "borderRadius": "5px",
                "cursor": "pointer",
                "fontSize": "16px",
            },
        ),
        dcc.Loading(
            id="loading",
            type="circle",
            children=html.Div(
                id="output",
                style={
                    "marginTop": "30px",
                    "padding": "20px",
                    "backgroundColor": "#fff",
                    "borderRadius": "10px",
                    "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                    "textAlign": "left",
                },
            ),
        ),
    ],
)

@app.callback(
    [Output("uploaded-file-path", "children"), Output("submit-btn", "disabled")],
    [Input("uploader", "isCompleted")],
    [State("uploader", "fileNames")],
)
def update_uploaded_file(is_completed, file_names):
    if is_completed and file_names:
        uploaded_file = file_names[0]
        return f"Uploaded File: {uploaded_file}", False
    return "", True

@app.callback(
    Output("output", "children"),
    [Input("submit-btn", "n_clicks")],
    [State("uploader", "fileNames")],
)
def process_file(n_clicks, file_names):
    if n_clicks > 0 and file_names:
        uploaded_file = file_names[0]
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file)

        try:
            uploaded_file_obj = ai.upload_to_gemini(file_path, mime_type="image/jpeg")
            
            model = ai.model
            response = model.generate_content([
                "What object is this? Describe how it might be used",
                "Object: ",
                uploaded_file_obj,
                "Description: ",
            ])

            formatted_text = format_response(response.text)
            return html.Div([html.H3("Result:", style={"color": "#4CAF50"}), formatted_text])
        except Exception as e:
            return html.Div([html.H3("Error:", style={"color": "red"}), html.Pre(str(e))])

    return ""

def format_response(response_text):
    """
    Format the response text with support for bold text and lists.
    """
    formatted_elements = []
    for line in response_text.split("\n"):
        if line.startswith("*"):
            formatted_elements.append(html.Li(line[1:].strip()))
        elif line.startswith("**") and line.endswith("**"):
            formatted_elements.append(html.Strong(line[2:-2]))
        else:
            formatted_elements.append(html.P(line.strip()))
    return html.Ul(formatted_elements, style={"color": "#333", "lineHeight": "1.5"})

if __name__ == "__main__":
    app.run_server(debug=True)
