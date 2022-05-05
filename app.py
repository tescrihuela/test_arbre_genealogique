import dash_interactive_graphviz
import dash
import flask
from dash import Input, Output, State, html
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import webbrowser
import os.path

##################
# Création du serveur
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, title='Arbre généalogique')
app.config.suppress_callback_exceptions = True


initial_dot_source = """
digraph  {
node[style="filled"]
"François 1er"->"Henri II"
"Claude de France"->"Henri II"->"Charles IX"
"Catherine de Médicis"->"Charles IX"->"Lucie Duranton"
}
"""

app.layout = html.Div(
    [
        html.Div(
            dash_interactive_graphviz.DashInteractiveGraphviz(id="gv"),
            style=dict(flexGrow=1, position="relative"),
        ),
        html.Div(
            [
                html.H3("Selected element"),
                html.Div(id="selected"),
                html.H3("Dot Source"),
                dcc.Textarea(
                    id="input",
                    value=initial_dot_source,
                    style=dict(flexGrow=1, position="relative"),
                ),
                html.H3("Engine"),
                dcc.Dropdown(
                    id="engine",
                    value="dot",
                    options=[
                        dict(label=engine, value=engine)
                        for engine in [
                            "dot",
                            "fdp",
                            "neato",
                            "circo",
                            "osage",
                            "patchwork",
                            "twopi",
                        ]
                    ],
                ),
            ],
            style=dict(display="flex", flexDirection="column"),
        ),
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)


@app.callback(
    [Output("gv", "dot_source"), Output("gv", "engine")],
    [Input("input", "value"), Input("engine", "value")],
)
def display_output(value, engine):
    return value, engine


@app.callback(Output("selected", "children"), [Input("gv", "selected")], prevent_initial_call=True)
def show_selected(value):
    if os.path.exists(f"{value}.pdf"):
        read_pdf = webbrowser.open_new_tab(f"{value}.pdf")
    else:
        read_pdf = webbrowser.open_new_tab(f"python.pdf")
    return read_pdf, html.Div(value)


if __name__ == "__main__":
    app.run_server(debug=True)
