import DearPyGui_Markdown as dpgmd
import dearpygui.dearpygui as dpg


def load_times_new_roman(font_path='alox/engine/fonts'):
    dpgmd.set_font_registry(dpg.add_font_registry())

    font_size = 25
    default_font_path = f'{font_path}times.ttf'
    bold_font_path = f'{font_path}timesbd.ttf'
    italic_font_path = f'{font_path}timesi.ttf'
    italic_bold_font_path = f'{font_path}timesbi.ttf'

    default_font = dpgmd.set_font(
        font_size=font_size,
        default=default_font_path,
        bold=bold_font_path,
        italic=italic_font_path,
        italic_bold=italic_bold_font_path
    )

    return default_font
