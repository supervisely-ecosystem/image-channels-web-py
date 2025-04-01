from supervisely.app.widgets import Button, Container, Checkbox
from sly_sdk.webpy.app import WebPyApplication
# from sly_sdk.app.widgets.button.button import Button
# from sly_sdk.app.widgets.container.container import Container
# from sly_sdk.app.widgets.checkbox.checkbox import Checkbox
from src.channel_extractor import ChannelExtractor


checkbox_r = Checkbox("Red", checked=True, widget_id="checkbox_r")
checkbox_g = Checkbox("Green", checked=True, widget_id="checkbox_g")
checkbox_b = Checkbox("Blue", checked=True, widget_id="checkbox_b")

button_update = Button("Update Image", widget_id="update_button")
checkbox_container = Container(widgets=[checkbox_r, checkbox_g, checkbox_b], widget_id="checkbox_container")
layout = Container(widgets=[checkbox_container, button_update], widget_id="main_layout")

app = WebPyApplication(layout=layout)

import sys
if sys.platform == 'emscripten':
    if not "init" in app.state:
        app.state["init"] = True
        app.state["imagePixelsDataImageId"] = None
        app.state["imagePixelsData"] = None
        app.state["active_channels"] = {"R": True, "G": True, "B": True}

channel_extractor = ChannelExtractor(app)

@checkbox_r.value_changed
def on_r_change(is_checked):
    app.state["active_channels"]["R"] = is_checked
    channel_extractor.update_combined_image()

@checkbox_g.value_changed
def on_g_change(is_checked):
    app.state["active_channels"]["G"] = is_checked
    channel_extractor.update_combined_image()

@checkbox_b.value_changed
def on_b_change(is_checked):
    app.state["active_channels"]["B"] = is_checked
    channel_extractor.update_combined_image()

@button_update.click
def update_image():
    print(f"Active channels: {app.state['active_channels']}")
    channel_extractor.update_combined_image()
