import json
from abc import ABC
from abc import abstractmethod

import requests


class SlackMessage():
    slack_url = "your slack url"

    def __init__(self):
        pass

    def send(self, template):
        requests.post(
            SlackMessage.slack_url,
            data=template.data,
            headers={"Content-type": "application/json"}
        )


class SlackMessageTemplate(ABC):
    @abstractmethod
    def data(self):
        pass


class NotiTemplate(SlackMessageTemplate):
    def __init__(self, pretext, text):
        self._data_dict = {
            "attachments": [
                {
                    "pretext": pretext,
                    "text": text,
                    "color": "#87CEFA"
                    }
            ]
        }
        self._data = json.dumps(self._data_dict)

    @property
    def data(self):
        return self._data
