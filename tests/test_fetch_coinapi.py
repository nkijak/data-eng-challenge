from unittest.mock import patch
from datetime import datetime
from coin_market.backend.fetch import CoinAPIio
import coin_market.backend.fetch
import json

def test_fetch_daily_prices():
    with patch('coin_market.backend.fetch.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'application/json'}
        mock_get.return_value.json = lambda: [{}]
        api = CoinAPIio('api-key', url_base='broken_for_safety')
        actual = api.fetch_daily_prices('BTC', datetime.now())
        assert [{}] == actual

def test_fetch_daily_prices_formats_request_properly():
    with patch('coin_market.backend.fetch.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type': 'application/json'}
        mock_get.return_value.json = lambda: [{}]
        api = CoinAPIio('api-key', url_base='broken_for_safety')
        when = datetime(year=1970, month=1, day=1, hour=0, minute=0)
        api.fetch_daily_prices('btc', when)
        mock_get.assert_called_with(
                f'broken_for_safety/v1/ohlcv/BTC/USD/history?period_id=1DAY&time_start=1970-01-01T00:00:00&limit=400', 
                headers={'X-CoinAPI-Key': 'api-key'})

    

