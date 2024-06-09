import argparse
import log
from rich import print
import dearpygui.dearpygui as dpg
import dpgthemeloader.dpgthemeloader as dpgtl
import engine
import platform

VERSION = "v0.0a"
PYTHON_VERSION = platform.python_version()

def redirect(html, style, engine_viewport):
    if html is list:
        return 1
    else:
        dpg.show_item("alox_loading_icon")
        dpg.delete_item(engine_viewport, children_only=True)
        dpg.bind_item_theme(engine_viewport, dpgtl.load_json_theme(style))
        HTML_res = engine.extract_html_elements(html)
        #print(HTML_res)
        engine.display_html_elements(HTML_res, engine_viewport)
        dpg.hide_item("alox_loading_icon")

def redirect_to(url, style, engine_viewport):
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://"+ url

    src = engine.get_html_source(url)
    if type(src) is list:
        code = src[0]
        reason = src[1]
        log.error(f"Failed to redirect to {url} ({code}), {reason}")
        dpg.delete_item("alox_engine_viewport", children_only=True)
        engine.dpgmd.add_text(f'# <center><font color="(0,0,0)">HTTPS {code}</font></center>', parent=engine_viewport)
        engine.dpgmd.add_text(f'<center><font size=16 color="(0,0,0)">{reason}</font></center>', parent=engine_viewport)
        if code == 404:
            engine.dpgmd.add_text(f'<center><font size=16 color="(0,0,0)">\n\n\nYou might not be connected to the internet or there are issues with your internet connection</font></center>', parent=engine_viewport)
    else:
        dpg.set_value("alox_url_input", url)
        redirect(src, style, engine_viewport)

def main():
    prs = argparse.ArgumentParser()
    prs.add_argument("-i", "--index", type=str, help="HTML source file to run natively")
    prs.add_argument("-t", "--theme", type=str, help="Load a JSON DPG theme")
    prs.add_argument("-s", "--style", type=str, help="Load a default JSON theme for engine_viewport")
    args = prs.parse_args()

    theme_path = "alox/ui/themes/ws_modern.json"
    html_path = "index.html"
    style_path = "alox/engine/temp.style.json"

    

    print(f"\\[Alox _engine_] \\[{VERSION}]")

    log.info("Parsing arguments from user")
    if args.theme: theme_path = args.theme
    if args.index: html_path = args.index
    if args.style: style_path = args.style
    log.ok(args)

    log.info("Starting AloxEngine GUI")
    dpg.create_context()

    dpg.bind_theme(dpgtl.load_json_theme(theme_path))
    log.ok(f"Binded JSON theme \\[{theme_path}]")

    log.info("Init HTML")
    engine.init_html()

    with dpg.window(label="AloxEngine", tag="alox_hwnd"):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Refresh", callback=lambda:redirect_to(dpg.get_value("alox_url_input"), style_path, "alox_engine_viewport"))
                dpg.add_separator()
                dpg.add_menu_item(label="Show font manager", callback=dpg.show_font_manager)
                dpg.add_menu_item(label="Show item registry", callback=dpg.show_item_registry)
                dpg.add_menu_item(label="Show style editor", callback=dpg.show_style_editor)
                dpg.add_menu_item(label="Exit Alox", shortcut="ALT+F4", callback=dpg.stop_dearpygui)

            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="Redirect to AloxEngine repository")
                dpg.add_separator()
                dpg.add_text(f"AloxEngine version {VERSION}")
                dpg.add_text(f"Python version {PYTHON_VERSION}")

            dpg.add_separator()
            dpg.add_button(label="<")
            dpg.add_button(label=">")
            dpg.add_input_text(hint="Enter a valid URL", tag="alox_url_input", on_enter=True, callback=lambda:redirect_to(dpg.get_value("alox_url_input"), style_path, "alox_engine_viewport"), width=-650)
            dpg.add_separator()
            dpg.add_loading_indicator(width=18, height=18, show=False, tag="alox_loading_icon")
            dpg.add_separator()
            dpg.add_text(default_value=html_path, tag="alox_title")

        dpg.add_child_window(tag="alox_engine_viewport", horizontal_scrollbar=True, width=-1, height=-1)

    dpg.set_primary_window("alox_hwnd", True)

    redirect(open(html_path, encoding="utf-8").read(), style_path, "alox_engine_viewport")
    
    
    log.info("Creating viewport")
    dpg.create_viewport(title="Alox", width=1365, height=800)
    dpg.show_viewport()
    dpg.setup_dearpygui()
    dpg.start_dearpygui()
    dpg.destroy_context()
    log.info("Hello after destroy context or stop dearpygui, dpg may shutten down")


if __name__ == "__main__":
    main()
