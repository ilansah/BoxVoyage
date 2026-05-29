import json
import os


class JsonStorage:    
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def load(self) -> dict:
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save(self, data: dict) -> None:
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)  # create parent directory if missing
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)