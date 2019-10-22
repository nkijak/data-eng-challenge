''' module for defining common tasks to be triggered from various UIs '''
from datetime import datetime
from coin_market.backend.fetch import DailyCoinHistory, CoinAPIio
from coin_market.backend.db import DailyPriceListing


def _convert_price_for_db(asset_id, 
        time_period_start, 
        price_open, 
        price_close,
        price_high,
        price_low,
        volume_traded,
        trades_count,
        updated_at=None,
        **kwargs):
    ''' Data storage representation transformer of Coin historical data '''
    if not updated_at:
        updated_at = datetime.utcnow()
    return {
        'asset_id':  asset_id,
        'effective_date': time_period_start,
        'price_open': price_open,
        'price_high': price_high,
        'price_low': price_low,
        'price_close': price_close,
        'volume_traded': volume_traded,
        'trades_count': trades_count,
        'updated_at': updated_at.isoformat()
    }

def store_past_year_for(symbol, api_key, conn):
   ''' 
   fetches and stores the last years data for a symbol 

   conn - SQLAlchemy engine.connection to the database to store in
   '''
   dch = DailyCoinHistory(CoinAPIio(api_key))
   raw = dch.fetch_daily_prices(symbol)
   if not raw:
        raise Exception(f'no data found for {symbol}')
   data = [_convert_price_for_db(symbol, **d) for d in raw]
   result = conn.execute(DailyPriceListing.__table__.insert(), data).rowcount
   return result
   
