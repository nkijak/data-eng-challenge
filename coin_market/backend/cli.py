import os
import fire
import coin_market.backend.db as db
import coin_market.backend.tasks as tasks

class CoinMarketBackend:
    ''' Tools for building the coin market backend '''
    def __init__(self,
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            schema='postgres'):
        sql_url = f'{schema}://{user}:{password}@{host}:{port}/coin_market'
        self.db = db.DBService(sql_url)

    def create_tables(self):
        ''' creates the required tables in the coin_market db '''
        self.db.create_tables()

    def drop_tables(self):
        ''' drops all known tables in coin_market db '''
        self.db.drop_tables()

    def load_historical_data(self, symbol, api_key=os.getenv('API_KEY')):
        ''' loads historical data for a given symbol up to a year ago '''
        try:
          count = tasks.store_past_year_for(symbol, api_key, self.db.connect())
          return f'Loaded {count} records'
        except Exception as e:
          return e

if __name__ == '__main__':
    fire.Fire(CoinMarketBackend)
