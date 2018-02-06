"""
Component that will perform image classification via a REST API.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/image_processing.rest_api/
"""
import requests
import logging
import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)


CONF_URL = 'url'
CONF_FILE_PATH = 'file_path'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.string,
    vol.Required(CONF_FILE_PATH): cv.isfile,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the folder sensor."""
    classifier = Classification(
        config.get(CONF_URL), config.get(CONF_FILE_PATH))
    add_devices([classifier], True)


class Classification(Entity):
    """Perform a classification via the rest API."""

    ICON = 'mdi:file'

    def __init__(self, url, file_path):
        """Initialize the classification object."""
        self._url = url
        self._file_path = file_path   # Need to check its a valid path
        self._name = "Rest_classifier"
        self._state = None
        self._data = {}
        self.process_image()
        return

    def process_image(self):
        """Perform image processing."""
        image = open(self._file_path, "rb").read()
        payload = {"image": image}
        response = requests.post(self._url, files=payload).json()
        if response["success"]:
            self._state = response['predictions'][0]['label']
            self._data = {e['label']: round(e['probability'], 3) for e in response['predictions']}
        else:
            self._state = "Request failed"
            self._data = {}
        return

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def state_attributes(self):
        """Return device specific state attributes."""
        return self._data

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
