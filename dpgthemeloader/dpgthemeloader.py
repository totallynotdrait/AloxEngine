import dearpygui.dearpygui as dpg
import json

def load_json_theme(jsonfile, category=dpg.mvThemeCat_Core):
    """
    Creates a theme and it adds theme styles, colors in base of the defined JSON file.

    Args:
        jsonfile        Defines a valid JSON file.
        category        Defines in what category should the theme style or color be.
    Returns:
        Union[int, str]
    """
    file = open(jsonfile, "r")
    read_con = json.load(file)
    _theme = dpg.add_theme()


    for comp in read_con:
        attr = read_con.get(comp, {})
        with dpg.theme_component(getattr(dpg, comp), parent=_theme):
            for i in attr:
                if "mvThemeCol" in i:
                    dpg.add_theme_color(getattr(dpg, i), attr[i], category=category)
                elif "mvStyleVar" in i:
                    if isinstance(attr[i], list):
                        dpg.add_theme_style(getattr(dpg, i), *attr[i], category=category)
                    else:
                        dpg.add_theme_style(getattr(dpg, i), attr[i], category=category)
    return _theme
