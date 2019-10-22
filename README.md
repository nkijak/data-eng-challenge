# Coin Market
### Assumptions
Assumes an empty postgres database named `coin_market` has been created with a user and proper permissions. 
```sql
create database coin_market
```

## Running Data pull
The following will build tables and populate.
```bash
python -m coin_market.cli create_tables
python -m coin_market.cli load_historical_data <symbol>
```
The above commands use the following ENV configuration along with flag arguments
| ENV         | flag     | description                 |
|-------------|----------|-----------------------------|
| API_KEY     |          | CoinAPIio api key           |
| DB_HOST     | --host   | db host                     |
| DB_PORT     | --port   | db port                     |
| DB_USER     | --user   | db user                     |
| DB_PASSWORD | --pass   | db password                 |
|             | --schema | db schema default: postgres |

### Example
Using default postgres user for ease
```bash
>>> psql
create database coin_market;
>>> \q
>>> export API_KEY=some-real-key
>>> export DB_PASSWORD=my-default-postgres-password
>>> export DB_USER=my-default-postgres-user
>>> python -m coin_market.cli create_tables
>>> python -m coin_market.cli load_historical_data BTC
Found 365 results
Loaded 365 records
```

## Running API
```bash
export SQLALCHEMY_DATABASE_URI=postgres://<user>:<pass>@<host>:<port>/coin_market
export FLASK_APP=coin_market/api/main.py python -m flask run
```
API spec available in [swagger.yml]

### Example
Continuing from above after db is loaded with same ENV set
```bash
>>> export SQLALCHEMY_DATABASE_URI=postgres://<user>:<pass>@<host>:<port>/coin_market
>>> FLASK_APP=coin_market/api/main.py python -m flask run
.... #lots of flask output
```

Different shell, using [HTTPie](https://httpie.org/)

```bash
>>> http localhost:5000/api/BTC/diff/2019-10-01/2019-10-02
{
    "diffs": [
        {
            "diff_close": 156.877210299999,
            "diff_high": 541.8724,
            "diff_low": -7164.32,
            "diff_open": -229.0172103,
            "diff_trades": -23899,
            "diff_volume": -10591.631587254,
            "effective_date": "2019-10-02"
        },
        {
            "diff_close": -93.3572102999988,
            "diff_high": -1495.4654,
            "diff_low": 7888.07,
            "diff_open": 119.244,
            "diff_trades": 50778,
            "diff_volume": 6647.014486094,
            "effective_date": "2019-10-01"
        }
    ],
    "end": "2019-10-02",
    "start": "2019-10-01",
    "symbol": "BTC"
}
```

## Development
```bash
pip install -r requirements.txt
pylint coin_market #automatically uses local .pylintrc, update rules here to share
pytest
```

## Known Issues
- [ ] Logging is terrible/non-existent
- [ ] CLI doesn't list environment vars in help and specific task help doesn't show DB connection flags
- [ ] Fetching historical results should check date and paginate, may have limit imposed by server
- [ ] Does not evaluate existing data or drop/truncate first. Blindly dumps new data in.
- [ ] Does not handle coin symbol errors -- happy path loading only
- [ ] API doesn't validate date entries or that they are ordered correctly (start < end)
- [ ] API doesn't take into account available dates i.e. start and/or end could be before actual available data dates
- [ ] No docker
