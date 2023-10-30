from shiny import App, render, ui
from pathlib import Path
import json 
import random 
import itertools

www_dir = Path(__file__).parent / "www"

app_ui = ui.page_fluid(
    ui.h2("Shopping List"),
    ui.input_action_button("rand", "Randomize!"),
    ui.h3("Recipes for the Week"),
    ui.output_ui("r_list", class_ = "text-left"),
    ui.h3("Ingredients"),
    ui.output_ui("s_list", class_ = "text-left"),
)

def randomizer():
    pass

def ui_generator(data, category):
    ui_list = [ui.strong(category)]
    items_list = [data[k]["ingredients"][category] for k in data]
    flat_items = [item for sublist in items_list for item in sublist if item is not ""]
    for idx, j in enumerate(flat_items): 
        if idx == 0:
            ui_list.append(ui.HTML("<br>"))
        ui_list.append(j), 
        ui_list.append(ui.HTML("<br>"))
    ui_list.append(ui.hr())
    return(ui_list)


def flatten(l):
    m = list(itertools.chain(*l))
    return m
    



def server(input, output, session):
    f = open(Path(www_dir, "recipes.json"))
    data = json.load(f)

    @output
    @render.ui
    def r_list():
        out_list = []
        for k in data:
            out_list.append(k)
            out_list.append(ui.HTML("<br>"))
        out = ui.TagList(*out_list)
        return out


    @output
    @render.ui
    def s_list():
        categories = ["Meats", "Vegetables", "Cheese and milk", "Other"]
        out_list = []
        for k in categories: 
            out_list.append(ui_generator(data, k))
        out_list = flatten(out_list)
        
        out = ui.TagList(*out_list)
        return out


app = App(app_ui, server, static_assets=www_dir)
