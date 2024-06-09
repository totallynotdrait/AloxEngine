"""
Alox Engine

HTML Parser for Alox

(This message should not be a string when compiled, not really a problem but annoying)
"""
from rich import print
from bs4 import BeautifulSoup
import dearpygui.dearpygui as dpg
import log, requests
import DearPyGui_Markdown as dpgmd
import wget
from PIL import Image
import numpy as np
import py_mini_racer, urllib

#TODO: IMPLEMENT AT LEAST DT AND START CSS

html_headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
html_paragraph = ['p']
html_hyperlink = ['a']
html_separator = ['hr', "br"]
html_image = ['img', "svg"]
html_containers = ['div']
html_import = ['link', "script"]
html_button = ['button']
html_text_input = ['textarea', 'input']
html_h = ['html', 'head', 'body']

not_alox_compatible = ["link", "svg", "path", "span"]
times_new_roman = None
js_ctx = py_mini_racer.MiniRacer()

def get_js_source(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        log.error(f"Error retrieving JS source: {e}")
        return None

def evaluate_external_js(js_ctx, script_src, base_url):
    # Construct the full URL for the external script
    script_url = urllib.parse.urljoin(base_url, script_src)
    # Retrieve the external JS source code
    js_source = get_js_source(script_url)
    if js_source:
        # Evaluate the external JS source code
        js_ctx.eval(js_source)

def get_html_source(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            log.error(f"HTTP 403 Forbidden: Access is denied. {e}")
        else:
            log.error(f"HTTP error occurred: {e}")
        return [response.status_code, e]
    except requests.exceptions.ConnectionError as e:
        log.error(f"Connection Error: {e}")
        return [400, e]
    except requests.exceptions.Timeout as e:
        log.error(f"Timeout Error: {e}")
        return [408, e]
    except requests.exceptions.RequestException as e:
        log.error(f"An error occurred: {e}")
        return [400, e]

def set_title(title):
    dpg.set_value("alox_title", title)

def init_html(font_path="alox/engine/fonts/"):
    global times_new_roman, tahoma
    """
    init_html
    ===================================
    Initialize the default font (Times New Roman) with DearPyGui-Markdown.
    Call this after create_context.
    """
    dpgmd.set_font_registry(dpg.add_font_registry())   

    tahoma_font_size = 13
    tahoma_font_path = f'{font_path}tahoma.ttf'
    tahomabd_font_path = f'{font_path}tahoma.ttf'
    italic_font_path = f'{font_path}timesi.ttf'
    italic_bold_font_path = f'{font_path}timesbi.ttf'

    tahoma = dpgmd.set_font(
        font_size=tahoma_font_size,
        default=tahoma_font_path,
        bold=tahomabd_font_path,
        italic=italic_font_path,
        italic_bold=italic_bold_font_path
    )  

    font_size = 25
    default_font_path = f'{font_path}times.ttf'
    bold_font_path = f'{font_path}timesbd.ttf'
    italic_font_path = f'{font_path}timesi.ttf'
    italic_bold_font_path = f'{font_path}timesbi.ttf'
    
    times_new_roman = dpgmd.set_font(
        font_size=font_size,
        default=default_font_path,
        bold=bold_font_path,
        italic=italic_font_path,
        italic_bold=italic_bold_font_path
    ) 

def web_image(url, path="alox/engine/temp/"):
    filename = wget.download(url, out=path)
    picture = Image.open(filename)
    h, w = picture.size
    buffer = np.array(picture.convert("RGBA"), dtype=np.uint8) / 255.0

    return [int(w), int(h), buffer]

def add_text(value, tag, attr, parent="alox_engine_viewport"):
    if tag == "h1": h = dpgmd.add_text(f"# <font size=32 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "h2": h = dpgmd.add_text(f"## <font size=24 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "h3": h = dpgmd.add_text(f"### <font size=18 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "h4": h = dpgmd.add_text(f"#### <font size=16 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "h5": h = dpgmd.add_text(f"##### <font size=13 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "h6": h = dpgmd.add_text(f"###### <font size=10 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "p": h = dpgmd.add_text(f"<font size=16 color='(0,0,0)'>{value}</font>", parent=parent); dpg.bind_item_font(h, times_new_roman)
    if tag == "a": h = dpgmd.add_text(f"[<font size=16 color='(0,0,0)'>{value}</font>]({attr["href"]})", parent=parent); dpg.bind_item_font(h, times_new_roman)


def render_html(html_element, engine_viewport="alox_engine_viewport"):
    if isinstance(html_element, dict):
        tag = html_element['tag']
        val = html_element.get('val', '')
        attr = html_element.get('attributes', '')
        children = html_element['children']
        print(html_element)
        
        if tag == "head":
            for i in children:
                if i['tag'] == "title":
                    set_title(i.get('val', ''))
        elif tag == "body":
            for i in children:
                render_html(i)
        elif tag == "div":
            with dpg.group(parent=engine_viewport) as grp:
                for i in children:
                    render_html(i, engine_viewport=grp)
        elif tag in html_headers:
            add_text(val, tag, attr, parent=engine_viewport)
        elif tag in html_paragraph:
            add_text(val, tag, attr, parent=engine_viewport)
        elif tag in html_hyperlink:
            add_text(val, tag, attr, parent=engine_viewport)
        elif tag == "center":
            with dpg.group(horizontal=True, parent=engine_viewport) as grp:
                for i in children:
                    render_html(i, engine_viewport=grp)
        elif tag == "img":
            if attr['src'].startswith("http"):
                wimg = web_image(attr['src'])
                with dpg.texture_registry():
                    wimg = dpg.add_dynamic_texture(wimg[1], wimg[0], wimg[2])
                dpg.add_image(wimg, parent=engine_viewport)
            else:
                w, h, buffer = web_image(dpg.get_value("alox_url_input")+"/"+attr['src'])
                with dpg.texture_registry():
                    wimg = dpg.add_dynamic_texture(h, w, buffer)
                dpg.add_image(wimg, parent=engine_viewport)
        elif tag == "button":
            h = dpg.add_button(label=val, parent=engine_viewport)
            dpg.bind_item_font(h, tahoma)
        elif tag == "input":
            h = dpg.add_input_text(label=val, parent=engine_viewport)
            dpg.bind_item_font(h, tahoma)

def extract_html_elements(html_content):
    def add_elements(element):
        if element.name is not None:  # Ignore non-tag elements
            element_text = ''.join(element.find_all(text=True, recursive=False)).strip()
            attributes = {attr: value for attr, value in element.attrs.items()}
            element_dict = {
                'tag': element.name,
                'val': element_text,
                'attributes': attributes,
                'children': []
            }
            for child in element.children:
                child_element = add_elements(child)
                if child_element:
                    element_dict['children'].append(child_element)
            return element_dict
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    root = soup.find()
    return add_elements(root)
    


def display_html_elements(html_res, engine_viewport):
    for child in html_res['children']:
        render_html(child, engine_viewport)