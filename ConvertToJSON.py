import json
from abc import ABC, abstractmethod


class ToJSON(ABC):
	@abstractmethod
	def write(self):
		pass


class TuiToJSON(ToJSON):
	def write(self, data):
		with open('Tui.json', 'w') as file:
			file.write(json.dumps(data, indent=4, ensure_ascii=False))


class SharaToJSON(ToJSON):
	def write(self, data):
		with open('MebelShara.json', 'w') as file:
			file.write(json.dumps(data, indent=4, ensure_ascii=False))

