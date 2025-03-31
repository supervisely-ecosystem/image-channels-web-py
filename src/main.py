import numpy as np
from supervisely.app.widgets import Button, Container
from sly_sdk.webpy.app import WebPyApplication


button = Button("Extract RGB", widget_id="extract_button")
layout = Container(widgets=[button], widget_id="extract_layout")
app = WebPyApplication(layout=layout)


def create_channel_canvas(height, width, channel_name):
    from js import document

    canvas = document.createElement("canvas")
    canvas.width = width
    canvas.height = height
    canvas.style.margin = "10px"
    canvas.id = f"channel_{channel_name}"
    return canvas


@button.click
def extract_rgb():
    from js import ImageData, document
    from pyodide.ffi import create_proxy

    state = app.state
    img_np: np.ndarray = app.get_current_image()
    h, w = img_np.shape[0], img_np.shape[1]
    if not hasattr(state, "channel_container"):
        container = document.createElement("div")
        container.style.display = "flex"
        container.style.flexDirection = "row"
        container.style.justifyContent = "center"
        container.style.alignItems = "center"
        container.id = "channel_container"
        document.body.appendChild(container)
        state.channel_container = container

    if not hasattr(state, "channel_canvases"):
        state.channel_canvases = {
            "R": create_channel_canvas(h, w, "R"),
            "G": create_channel_canvas(h, w, "G"),
            "B": create_channel_canvas(h, w, "B"),
        }
        for canvas in state.channel_canvases.values():
            state.channel_container.appendChild(canvas)

    img_arr = img_np
    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]
    channels = {"R": r, "G": g, "B": b}
    for channel_name, channel_data in channels.items():
        channel_img = np.zeros((h, w, 4), dtype=np.uint8)
        if channel_name == "R":
            channel_img[:, :, 0] = channel_data
        elif channel_name == "G":
            channel_img[:, :, 1] = channel_data
        else:
            channel_img[:, :, 2] = channel_data
        channel_img[:, :, 3] = 255

        channel_canvas = state.channel_canvases[channel_name]
        channel_ctx = channel_canvas.getContext("2d")
        channel_pixels = create_proxy(channel_img.flatten())
        channel_buf = channel_pixels.getBuffer("u8clamped")
        channel_img_data = ImageData.new(channel_buf.data, w, h)
        channel_ctx.putImageData(channel_img_data, 0, 0)
        channel_pixels.destroy()
        channel_buf.release()
