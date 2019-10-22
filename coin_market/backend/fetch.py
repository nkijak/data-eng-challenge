''' module for doing data collection '''
from datetime import datetime, timedelta
from typing import List, Dict
import requests

class DailyCoinHistory:
  ''' Daily Coin History Fetch Mechanism from a given coin service '''
  def __init__(self, coinservice):
    self.coinservice = coinservice

  def fetch_daily_prices(self, symbol: str, days_ago: timedelta=timedelta(days=365)) -> List[Dict]:
    ''' Gets daily prices from days_ago or by default ~1 year ago '''
    now = datetime.now()
    start = now - days_ago
    prices = self.coinservice.fetch_daily_prices(symbol, since=start)
    return prices
    
     



class CoinAPIio:
  ''' implmentation of coin service that uses CoinAPIio specifically '''
  def __init__(self, api_key, url_base='https://rest.coinapi.io'):
    self.url_base = url_base
    self.headers = {'X-CoinAPI-Key': api_key}

  def fetch_daily_prices(self, symbol: str, since: datetime) -> List[Dict]:
    ''' grabs historical OHLCV information for coin denoted by symbol ''' 
    url =f'{self.url_base}/v1/ohlcv/{symbol.upper()}/USD/history?period_id=1DAY&time_start={since.strftime("%Y-%m-%dT%H:%M:%S")}&limit=400'
    response = requests.get(url, headers=self.headers)
    if response.status_code == 200:
        try:
            data = response.json()
            print(f'found {len(data)} results')
            return data
        except ValueError as ve:
            # TODO deal with bad json
            print('value error ', ve)
            return []
    else:
        # TODO raise error about fetch
      print(f'failed to get a good response ->{response.status_code}:{response.content}')
      return []


  
