''' API service '''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class DailyPriceListings(db.Model):
    asset_id = db.Column(db.String, primary_key=True)
    effective_date = db.Column(db.Date, primary_key=True)
    price_open = db.Column(db.Float)
    price_high = db.Column(db.Float)
    price_low = db.Column(db.Float)
    price_close = db.Column(db.Float)
    volume_traded = db.Column(db.Float)
    trades_count = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime)

    @property
    def serialize(self):
        return {
                'symbol': self.asset_id,
                'effectiveDate': self.effective_date.isoformat(),
                'priceOpen': self.price_open,
                'priceHigh': self.price_high,
                'priceLow': self.price_low,
                'priceClose': self.price_close,
                'volumeTraded': self.volume_traded,
                'tradesCount': self.trades_count,
                'updatedAt': self.updated_at.isoformat()
                } 

@app.route('/api/<string:symbol>/diff/<start>/<end>', methods=['GET'])
def daily_diff(symbol, start, end):
    #FIXME validate start and end are dates
    #FIXME order start and end approprately
    with db.engine.connect() as con:
        rs = con.execute(text(diff_query), symbol=symbol, start=start, end=end).fetchall()
        if not rs:
            return {'message': f'symbol {symbol} is not available'}, 404
        records = [{'diffOpen': r['diff_open'],
                'diffHigh': r['diff_high'],
                'diffLow': r['diff_low'],
                'diffClose': r['diff_close'],
                'diffVolume': r['diff_volume'],
                'diffTrades': r['diff_trades'],
                'effectiveDate': r['effective_date'].isoformat()} for r in rs]
        
    return {'diffs': records,
        'symbol': symbol,
        'start': start,
        'end': end
        }

@app.route('/api/<string:symbol>/avg/<start>/<end>', methods=['GET'])
def daily_avg_hi_lo(symbol, start, end):
    #FIXME validate start and end are dates
    #FIXME order start and end approprately
    with db.engine.connect() as con:
        rs = con.execute(text(avg_query), symbol=symbol, start=start, end=end).first()
    if not rs:
        return {'message': f'symbol {symbol} is not available'}, 404
    return {"averageHigh": rs['avg_high'], 
            "averageLow": rs['avg_low'], 
            "symbol": symbol,
            "start": start,
            "end": end}

@app.route('/api/<string:symbol>/openings/<int:n>', methods=['GET'])
def best_opening(symbol, n):
    if n < 1 or n > 5:
        return {'message': f'n ({n}) must be between 1 and 5 inclusive'}, 400
    results = DailyPriceListings.query \
        .filter_by(asset_id=symbol) \
        .order_by(DailyPriceListings.price_open.desc()) \
        .limit(n)
    if results.count() == 0:
        return {'message': f'no results found for {symbol}'}, 404
    return {'best': [r.serialize for r in results]}

diff_query="""
with cte as (
    select price_open,
    LAG(price_open, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_open,
    price_high,
    LAG(price_high, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_high,
    price_low,
    LAG(price_low, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_low,
    price_close,
    LAG(price_close, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_close,
    volume_traded,
    LAG(volume_traded, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_volume,
    trades_count,
    LAG(trades_count, 1) OVER (PARTITION BY asset_id ORDER BY effective_date desc) as previous_trades,
    effective_date,
    asset_id
    FROM daily_price_listings
)
select 
price_open - previous_open as diff_open, 
price_high - previous_high as diff_high, 
price_low - previous_low as diff_low,
price_close - previous_close as diff_close,
volume_traded - previous_volume as diff_volume,
trades_count - previous_trades as diff_trades,
asset_id, 
effective_date 
from cte
where asset_id = :symbol
and effective_date BETWEEN :start and :end;
"""

avg_query="""
select
    avg(price_high) avg_high,
    avg(price_low) avg_low,
    asset_id
FROM daily_price_listings
WHERE asset_id = :symbol
AND effective_date BETWEEN :start AND :end
GROUP BY asset_id;
"""
