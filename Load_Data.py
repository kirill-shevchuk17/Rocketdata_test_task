import requests
from abc import ABC, abstractmethod
import pandas as pd


class Data(ABC):
	@abstractmethod
	def save(self):
		pass


class DataTui(Data):
	def __init__(self, url):
		self.url = url

	def save(self):
		r = requests.get(self.url)
		r.encoding = 'utf-8'
		with open('tuiru.json', 'w') as f:
			f.write(r.text)


class DataShara(Data):
	def __init__(self, url):
		self.url = url

	def save(self):
		r = requests.get(self.url)
		with open('mebelshara.html', 'w') as f:
			f.write(r.text)
