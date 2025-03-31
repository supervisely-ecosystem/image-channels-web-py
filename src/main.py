from supervisely.app.widgets import Button, Container
from sly_sdk.webpy.app import WebPyApplication
from src.channel_extractor import ChannelExtractor


button = Button("Extract RGB", widget_id="extract_button")
button_r = Button("Extract R", widget_id="extract_r_button")
button_g = Button("Extract G", widget_id="extract_g_button")
button_b = Button("Extract B", widget_id="extract_b_button")
layout = Container(widgets=[button, button_r, button_g, button_b], widget_id="extract_layout")
app = WebPyApplication(layout=layout)

import sys
if sys.platform == 'emscripten':
    if not "init" in app.state:
        app.state["init"] = True
        app.state["imagePixelsDataImageId"] = None
        app.state["imagePixelsData"] = None

channel_extractor = ChannelExtractor(app)

@button.click
def extract_rgb():
    channel_extractor.extract_all_channels()

@button_r.click
def extract_r():
    channel_extractor.update_view_with_channel("R")

@button_g.click
def extract_g():
    channel_extractor.update_view_with_channel("G")

@button_b.click
def extract_b():
    channel_extractor.update_view_with_channel("B")
