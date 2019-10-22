import json
from datetime import datetime
import coin_market.backend.tasks as task

def test_convert_price_for_db():
    record = {
        "time_period_start": "2018-10-22T00:00:00.0000000Z",
        "time_period_end": "2018-10-23T00:00:00.0000000Z",
        "time_open": "2018-10-22T00:00:00.0000000Z",
        "time_close": "2018-10-22T23:59:59.6450000Z",
        "price_open": 6405.81,
        "price_high": 8700,
        "price_low": 5702.94,
        "price_close": 6407.65,
        "volume_traded": 550030.792748313,
        "trades_count": 116661
        }
    now = datetime.now()
    expected = {
            'asset_id': 'TEST',
            'effective_date': '2018-10-22T00:00:00.0000000Z',
            'price_open': 6405.81,
            'price_high': 8700,
            'price_low': 5702.94,
            'price_close': 6407.65,
            'volume_traded': 550030.792748313,
            'trades_count': 116661,
            'updated_at': now.isoformat()
            }
    actual = task._convert_price_for_db('TEST', updated_at=now, **record)
    assert actual == expected


