from datetime import datetime
import requests
from dataclasses import dataclass

import json
import os
import subprocess

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
    CONFIG = json.load(f)

@dataclass
class WRImprovement:
    replay_id: int
    replay_time: int
    user_name: str
    replay_at: datetime
    track_name: str
    ReplayPath: str

    def DownloadReplay(self):
        url = f"{CONFIG['api']['base_url']}/recordgbx/{self.replay_id}"
        response = requests.get(url)

        if response.status_code == 200:
            os.makedirs(self.ReplayPath, exist_ok=True)
            with open(self.ReplayPath + "replay.gbx", "wb") as file:
                file.write(response.content)

    def playAgainst(self):
        if not os.path.exists(self.ReplayPath + "replay.gbx"):
            self.DownloadReplay()
        subprocess.run(['cmd', '/c', 'start', '', self.ReplayPath + "replay.gbx"], shell=True)

def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    formatted_time = (f"{hours:02}:" if hours > 0 else "") + (f"{minutes:02}:" if minutes > 0 else "") + f"{seconds:02}.{int(milliseconds/10):02}"
    return formatted_time