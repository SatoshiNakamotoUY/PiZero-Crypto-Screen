import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import itertools

from config.builder import Builder
from config.config import config
from logs import logger
from presentation.observer import Observable

SCREEN_REFRESH_INTERVAL = 9600
DATETIME_FORMAT = "%Y-%m-%dT%H:%M"


def get_dummy_data():
    logger.info('Generating dummy data')



def fetch_prices(token):
    logger.info('Fetching prices')
    url = f'https://api.coingecko.com/api/v3/coins/{token}/ohlc?vs_currency={config.currency}&days={config.days}'
    req = Request(url)
    data = urlopen(req).read()
    external_data = json.loads(data)
    prices = [entry[1:] for entry in external_data]
    return prices


def main():
    logger.info('Initialize')

    data_sink = Observable()
    builder = Builder(config)
    builder.bind(data_sink)
    coins = config.cryptocurrencies.split(',')
    refresh_bucket = 0

    try:
        for coin in itertools.cycle(coins):
            try:
                if refresh_bucket > SCREEN_REFRESH_INTERVAL:
                    data_sink.screenrefresh_observers()
                    refresh_bucket = 0
                prices = [entry[1:] for entry in get_dummy_data()] if config.dummy_data else fetch_prices(coin.split(':')[0])
                data_sink.update_observers(coin.split(':')[1], prices)
                refresh_bucket = refresh_bucket + config.refresh_interval
                time.sleep(config.refresh_interval)
            except (HTTPError, URLError) as e:
                logger.error(str(e))
                time.sleep(5)
    except IOError as e:
        logger.error(str(e))
    except KeyboardInterrupt:
        logger.info('Exit')
        data_sink.screenrefresh_observers()
        data_sink.close()
        exit()


if __name__ == "__main__":
    main()
