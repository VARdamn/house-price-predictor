import csv
import math
from random import randint
from random import uniform
from time import sleep

from fake_useragent import UserAgent
from requests import Session

from config import config
from src.logger import logger


class Cyan:

    def __init__(self) -> None:

        self.user_agent = UserAgent(os='windows', platforms='pc').chrome
        self.session = Session()
        self.session.headers = self.build_headers()

    def build_headers(self):
        return {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'cookie': config.CYAN_COOKIE,
            'origin': 'https://www.cian.ru',
            'priority': 'u=1, i',
            'referer': 'https://www.cian.ru/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': self.user_agent,
        }

    def _get_offers_paginated(self, page: int = 1):
        payload = {
            'jsonQuery': {
                '_type': 'flatrent',
                'engine_version': {'type': 'term', 'value': 2},
                'region': {'type': 'terms', 'value': [1]},
                'for_day': {'type': 'term', 'value': '!1'},
                'room': {'type': 'terms', 'value': [1, 2, 3, 4]},
                'page': {'type': 'term', 'value': page},
            }
        }

        res = self.session.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', json=payload)

        if res.status_code == 429:
            retry = randint(60, 90)
            logger.warning(f'Request failed with status {res.status_code}. Retrying in {retry} seconds')
            sleep(retry)
            res = self.session.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', json=payload)
            if res.status_code > 204:
                logger.error(f'Cannot parse offers from Cyan! Status: {res.status_code}, page: {page}')
        elif res.status_code > 204:
            logger.error(f'Cannot parse offers from Cyan! Status: {res.status_code}, page: {page}')

        data = res.json()
        offers = data.get('data', {}).get('offersSerialized', [])
        logger.info(f'Parsed {len(offers)} offers from {page} page...')
        return offers

    def __get_offers(self, count: int = 100):
        offers = []
        page = 1
        while len(offers) < count:
            offers.extend(self._get_offers_paginated(page=page))
            page += 1
            sleep(uniform(5, 12))

        logger.success(f'Successfully parsed {len(offers)} offers!')
        return offers

    def get_parsed_offers(self):
        parsed = []
        offers = self.__get_offers()

        for offer in offers:
            undergrounds = [d.get('time', math.inf) for d in offer.get('geo').get('undergrounds', [])]
            railways = [d.get('time', math.inf) for d in offer.get('geo').get('railways', []) if d.get('travelType') == 'byFoot']

            nearest_underground = min(undergrounds) if undergrounds else -1
            nearest_railway = min(railways) if railways else -1
            district = [
                d.get('shortName') or d.get('title')
                for d in offer.get('geo', {}).get('address', [])
                if d.get('geoType') == 'district' and d.get('type') == 'okrug'
            ]
            price = offer.get('bargainTerms', {}).get('priceRur', 0) or offer.get('bargainTerms', {}).get('price', -1)

            parsed.append(
                {
                    'creation_date': offer.get('creationDate') or -1,
                    'floor': offer.get('floorNumber') or -1,
                    'floors_count': offer.get('building', {}).get('floorsCount') or -1,
                    'area': float(offer.get('totalArea') or -1),
                    'living_area': float(offer.get('livingArea') or -1),
                    'kitchen_area': float(offer.get('kitchenArea') or -1),
                    'rooms_count': offer.get('roomsCount') or -1,
                    'has_furniture': offer.get('hasFurniture') or False,
                    'address': offer.get('geo', {}).get('userInput') or -1,
                    'district': -1 if not len(district) or not district[0] else district[0],
                    'nearest_underground': nearest_underground,
                    'nearest_railway': nearest_railway,
                    'price': price,
                    'balconies_count': offer.get('balconiesCount') or 0,
                    'is_seller_agent': offer.get('user', {}).get('isAgent', 0) or offer.get('user', {}).get('isSubAgent', -1),
                    'builduing_year': offer.get('building', {}).get('buildYear') or -1,
                    'cargo_lifts_count': offer.get('building', {}).get('cargoLiftsCount') or 0,
                    'passenger_lifts_count': offer.get('building', {}).get('passengerLiftsCount') or 0,
                    'parking': offer.get('building', {}).get('parking').get('type') if offer.get('building', {}).get('parking') else -1,
                }
            )

        return parsed

    def dump_to_csv(self, offers):
        headers = [
            'Дата создания объявления',
            'Этаж',
            'Кол-во этажей',
            'Площадь',
            'Жилая площадь',
            'Площадь кухни',
            'Кол-во комнат',
            'Наличие мебели',
            'Адрес',
            'Округ',
            'Ближайшее метро, мин.',
            'Ближайший вокзал, мин.',
            'Стоимость, мес.',
            'Кол-во балконов',
            'Продажа от агента',
            'Год постройки здания',
            'Кол-во грузовых лифтов',
            'Кол-во пассажирских лифтов',
            'Парковка',
        ]
        mapped_keys = [
            'creation_date',
            'floor',
            'floors_count',
            'area',
            'living_area',
            'kitchen_area',
            'rooms_count',
            'has_furniture',
            'address',
            'district',
            'nearest_underground',
            'nearest_railway',
            'price',
            'balconies_count',
            'is_seller_agent',
            'builduing_year',
            'cargo_lifts_count',
            'passenger_lifts_count',
            'parking',
        ]

        if len(headers) != len(mapped_keys):
            raise ValueError('Data and headers count is not matching!')

        with open(config.CYAN_CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows([[offer.get(key, '') for key in mapped_keys] for offer in offers])
        logger.success(f'Dumped {len(offers)} offers to csv!')
