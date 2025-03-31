import numpy as np
from sly_sdk.sly_logger import logger


class ChannelExtractor:
    def __init__(self, app):
        self.app = app
        self._view = None

    def _ensure_view_exists(self):
        if self._view is None:
            views = self.app.get_ordered_initialized_views()
            if not views:
                logger.error("No views available")
                return None
            self._view = views[0]
        return self._view

    def _update_channel_view(self, channel_name, channel_data, width, height):
        try:
            channel_img = np.zeros((height, width, 4), dtype=np.uint8)
            channel_idx = {"R": 0, "G": 1, "B": 2}[channel_name]
            channel_img[:, :, channel_idx] = channel_data
            channel_img[:, :, 3] = 255

            view = self._ensure_view_exists()
            if view is None:
                return
                
            self.app.set_view_image_data(view.id, channel_img)
        except Exception as e:
            logger.error(f"Error updating channel view for {channel_name}: {e}")

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
            if self.app.state["imagePixelsDataImageId"] != image_id:
                self.app.state["imagePixelsData"] = self.app.get_image_data_by_id(image_id)
                if self.app.state["imagePixelsData"] is None:
                    logger.error("Failed to get current image")
                    return
                self.app.state["imagePixelsDataImageId"] = image_id
            
            img_np = self.app.state["imagePixelsData"]
            print(f"Current image id: {image_id}")
            print(f"Image shape: {img_np.shape}")

            self.app.create_group_views([image_id] * 4)

            h, w = img_np.shape[0], img_np.shape[1]
            view = self._ensure_view_exists()
            if view is None:
                return

            for channel_name in ["R", "G", "B"]:
                channel_data = img_np[:, :, {"R": 0, "G": 1, "B": 2}[channel_name]]
                self._update_channel_view(channel_name, channel_data, w, h)
        except Exception as e:
            logger.error(f"Error extracting all channels: {e}")

    def update_view_with_channel(self, channel_name):
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

            view = self._ensure_view_exists()
            if view is None:
                return
                
            self.app.set_view_image_data(view.id, channel_img)
        except Exception as e:
            logger.error(f"Error updating view with channel {channel_name}: {e}")
