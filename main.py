import requests
from Load_Data import DataTui, DataShara
from bs4 import BeautifulSoup
import json
from ConvertToJSON import TuiToJSON, SharaToJSON


tui_url = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
shara_url = 'https://www.mebelshara.ru/contacts'


def load_json():
	with open('tuiru.json', 'r') as f:
		json_data = json.load(f)
		return list(json_data.values())[0]


def tui_to_dict():
	file = load_json()
	tui = []
	for i in file:
		phones = []
		for phone in i.get('phones'):
			phones.append(phone.get('phone'))

		saturday = i.get("hoursOfOperation").get('saturday')
		sunday = i.get("hoursOfOperation").get('sunday')

		working_hours = []

		working_in_workdays = "пн - пт " + i.get("hoursOfOperation").get('workdays').get('startStr') + " до " + i.get(
			"hoursOfOperation").get('workdays').get('endStr')
		working_hours.append(working_in_workdays)
		if saturday.get('isDayOff') is True:
			working_in_weekdays = 'сб-вс выходной'
		else:
			if sunday.get('isDayOff') is True:
				working_in_weekdays = 'сб ' + saturday.get('startStr') + ' вс выходной'
			else:
				working_in_weekdays = 'сб-вс ' + saturday.get('startStr')
		working_hours.append(working_in_weekdays)

		store = {}
		store['address'] = i.get('address')
		store['latlon'] = [i.get('latitude'), i.get('longitude')]
		store['name'] = i.get('name')
		store['phones'] = phones
		store['working_hours'] = working_hours
		tui.append(store)
	return tui


def shara_to_dict():
	html = open('mebelshara.html', 'r').read()
	soup = BeautifulSoup(html, 'lxml')
	cities = soup.find_all('div', {'class': 'city-item'})
	shara = []
	for city in cities:
		town = city.find('h4', {'class': 'js-city-name'}).extract()
		shops = city.find_all('div', {'class': 'shop-list-item'})
		store = {}
		for shop in shops:
			store['address'] = town.text + ", " + shop['data-shop-address']
			store['latlon'] = [shop['data-shop-latitude'], shop['data-shop-longitude']]
			store['name'] = 'Мебель Шара'
			store['phones'] = shop['data-shop-phone']
			store['working-hours'] = "пн-вс " + shop['data-shop-mode2']
			shara.append(store)
	return shara


def main():
	tui_data = DataTui(tui_url)
	tui_data.save()

	shara_data = DataShara(shara_url)
	shara_data.save()

	tui = tui_to_dict()
	shara = shara_to_dict()

	tui_write_on_json = TuiToJSON()
	tui_write_on_json.write(data=tui)

	shara_write_on_json = SharaToJSON()
	shara_write_on_json.write(data=shara)


if __name__ == '__main__':
	main()
