import numpy as np
from sly_sdk.sly_logger import logger


class ChannelExtractor:
    def __init__(self, app):
        self.app = app
        self._view = None

    def _ensure_view_exists(self, view_idx:int = 0):
        if self._view is None:
            views = self.app.get_ordered_initialized_views()
            if not views:
                logger.error("No views available")
                return None
            if len(views) <= view_idx:
                logger.error(f"View index {view_idx} is out of range")
                return None
            self._view = views[view_idx]
        return self._view

    def _get_channel_names(self, img_np):
        channel_names = []
        if img_np.shape[2] == 4:  # RGBA
            channel_names = ["Red", "Green", "Blue", "Alpha"]
        elif img_np.shape[2] == 3:  # RGB
            channel_names = ["Red", "Green", "Blue"]
        elif img_np.shape[2] == 1:  # Grayscale
            channel_names = ["Gray"]
        else:
            channel_names = [f"Channel {i+1}" for i in range(img_np.shape[2])]
        return channel_names

    def _update_channel_view(self, view_id, channel_name, channel_data, width, height):
        try:
            channel_img = np.zeros((height, width, 4), dtype=np.uint8)
            channel_idx = {"R": 0, "G": 1, "B": 2}[channel_name]
            channel_img[:, :, channel_idx] = channel_data
            channel_img[:, :, 3] = 255

            self.app.set_view_image_data(view_id, channel_img)
        except Exception as e:
            logger.error(f"Error updating channel view for {channel_name}: {e}")

    def update_combined_image(self):
        try:
            image_id = self.app.get_current_image_id()
            if self.app.state["imagePixelsDataImageId"] != image_id:
                self.app.state["imagePixelsData"] = self.app.get_image_data_by_id(image_id)
                if self.app.state["imagePixelsData"] is None:
                    logger.error("Failed to get current image")
                    return
                self.app.state["imagePixelsDataImageId"] = image_id

            img_np = self.app.state["imagePixelsData"]
            print(f"Image id: {image_id}")
            print(f"Image shape: {img_np.shape}")

            h, w = img_np.shape[0], img_np.shape[1]
            combined_img = np.zeros((h, w, 4), dtype=np.uint8)
            active_channels = self.app.state["active_channels"]
            
            for channel_name, is_active in active_channels.items():
                print(f"Channel name: {channel_name}, is_active: {is_active}")
                if is_active:
                    channel_idx = {"R": 0, "G": 1, "B": 2}[channel_name]
                    combined_img[:, :, channel_idx] = img_np[:, :, channel_idx]
            
            combined_img[:, :, 3] = 255

            view = self._ensure_view_exists()
            if view is None:
                return

            self.app.set_view_image_data(view.id, combined_img)
        except Exception as e:
            logger.error(f"Error updating combined image: {e}")

    def extract_channel(self, channel_name):
        try:
            img_np = self.app.get_current_image()
            if img_np is None:
                logger.error("Failed to get current image")
                return

            h, w = img_np.shape[0], img_np.shape[1]
            view = self._ensure_view_exists()
            if view is None:
                return

            channel_data = img_np[:, :, {"R": 0, "G": 1, "B": 2}[channel_name]]
            self._update_channel_view(channel_name, channel_data, w, h)
        except Exception as e:
            logger.error(f"Error extracting channel {channel_name}: {e}")

    def extract_all_channels(self):
        try:
            image_id = self.app.get_current_image_id()
            recreate_views = False
            if self.app.state["imagePixelsDataImageId"] != image_id:
                recreate_views = True
                self.app.state["imagePixelsData"] = self.app.get_image_data_by_id(image_id)
                if self.app.state["imagePixelsData"] is None:
                    logger.error("Failed to get current image")
                    return
                self.app.state["imagePixelsDataImageId"] = image_id

            img_np = self.app.state["imagePixelsData"]
            print(f"Current image id: {image_id}")
            print(f"Image shape: {img_np.shape}")

            channel_names = self._get_channel_names(img_np)
            print(f"Channel names: {channel_names}")

            self.app.create_views(2, 2, [image_id] * 4, recreate_views)
            views = self.app.get_ordered_initialized_views()

            h, w = img_np.shape[0], img_np.shape[1]

            for channel_name, view in zip(["R", "G", "B"], views[1:]):
                channel_data = img_np[:, :, {"R": 0, "G": 1, "B": 2}[channel_name]]
                self._update_channel_view(view.id, channel_name, channel_data, w, h)
        except Exception as e:
            logger.error(f"Error extracting all channels: {e}")

    def update_view_with_channel(self, channel_name, view_idx:int = 0):
        try:
            image_id = self.app.get_current_image_id()
            if self.app.state["imagePixelsDataImageId"] != image_id:
                self.app.state["imagePixelsData"] = self.app.get_image_data_by_id(image_id)
                if self.app.state["imagePixelsData"] is None:
                    logger.error("Failed to get current image")
                    return
                self.app.state["imagePixelsDataImageId"] = image_id

            img_np = self.app.state["imagePixelsData"]
            print(f"Current image id: {image_id}")
            print(f"Image shape: {img_np.shape}")

            h, w = img_np.shape[0], img_np.shape[1]
            channel_data = img_np[:, :, {"R": 0, "G": 1, "B": 2}[channel_name]]
            channel_img = np.zeros((h, w, 4), dtype=np.uint8)
            channel_idx = {"R": 0, "G": 1, "B": 2}[channel_name]
            channel_img[:, :, channel_idx] = channel_data
            channel_img[:, :, 3] = 255

            view = self._ensure_view_exists(view_idx)
            if view is None:
                return

            self.app.set_view_image_data(view.id, channel_img)
        except Exception as e:
            logger.error(f"Error updating view with channel {channel_name}: {e}")
