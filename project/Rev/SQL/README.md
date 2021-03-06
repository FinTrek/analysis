# SQL 


## SQL Fiddle Demo  
- http://sqlfiddle.com/#!17/541e0/1


## File 
- GBP_spend_user_largest_rate.sql : transaction in GBP with largest timestamp  
- GBP_spend_user_latest_rate.sql : transaction in GBP with latest exchange rate smaller/equal than  transaction timestamp  

## Demo 
```bash 
# demo of GBP_spend_user_largest_rate.sql
psql> 
WITH lastest_exchange_ts AS
  (SELECT from_currency,
          to_currency,
          max(ts) AS ts
   FROM exchange_rates
   WHERE to_currency = 'GBP'
   GROUP BY from_currency,
            to_currency),
     lastest_exchange AS
  (SELECT e.from_currency AS from_currency,
          e.rate AS rate
   FROM exchange_rates e
   INNER JOIN lastest_exchange_ts l ON e.from_currency = l.from_currency
   AND e.to_currency = l.to_currency
   AND e.ts = l.ts),
     trans_GBP AS
  (SELECT t.user_id AS user_id,
          t.ts AS ts,
          l.from_currency AS currency,
          t.amount*l.rate AS amount_GBP
   FROM transactions t
   INNER JOIN lastest_exchange l ON l.from_currency = t.currency ),
     trans_in_GBP AS
  ( SELECT user_id,
           ts,
           currency,
           amount AS amount_gbp
   FROM transactions
   WHERE currency = 'GBP' )

  
  SELECT *
  FROM trans_GBP
  UNION ALL
  SELECT *
  FROM trans_in_GBP
  ORDER BY user_id, ts 


psql> 
user_id	ts	currency	amount_gbp
1	2018-04-01T00:00:00Z	EUR	3.969
1	2018-04-01T01:00:00Z	EUR	13.689
1	2018-04-01T01:30:00Z	USD	2.17
1	2018-04-01T20:00:00Z	EUR	3.969
2	2018-04-01T00:30:00Z	USD	1.519
2	2018-04-01T01:20:00Z	USD	0.279
2	2018-04-01T01:40:00Z	USD	20.77
2	2018-04-01T18:00:00Z	EUR	20.169
3	2018-04-01T18:01:00Z	GBP	2
4	2018-04-01T00:01:00Z	USD	1.24
4	2018-04-01T00:01:00Z	GBP	2



```


```bash
# demo of GBP_spend_user_latest_rate.sql 
psql> 

WITH exchange_ts AS
  (SELECT ts,
          from_currency,
          to_currency,
          rate
   FROM exchange_rates
   WHERE to_currency = 'GBP'),
     exchange_ts_ AS
  (SELECT *,
          lag(ts, -1, '2019-01-01T00:00:00Z') OVER (PARTITION BY from_currency,
                                                                 to_currency
                                                    ORDER BY ts) AS ts_lag
   FROM exchange_rates
   WHERE to_currency = 'GBP' ),
     trans_GBP AS
  (SELECT t.user_id AS user_id,
          t.ts AS ts,
          t.currency AS currency,
          t.amount*e.rate AS amount_GBP
   FROM transactions t
   INNER JOIN exchange_ts_ e ON e.from_currency = t.currency
   AND (t.ts >= e.ts
        AND e.ts_lag > t.ts) ),
     trans_in_GBP AS
  (SELECT user_id,
          ts,
          currency,
          amount AS amount_gbp
   FROM transactions
   WHERE currency = 'GBP' )
SELECT *
FROM trans_GBP
UNION ALL
SELECT *
FROM trans_in_GBP
ORDER BY user_id,
         ts


psql>


user_id ts  currency  amount_gbp
1 2018-04-01T00:00:00Z  EUR 4.1895
1 2018-04-01T01:00:00Z  EUR 14.4495
1 2018-04-01T01:30:00Z  USD 2.17
1 2018-04-01T20:00:00Z  EUR 3.969
2 2018-04-01T00:30:00Z  USD 2.254
2 2018-04-01T01:20:00Z  USD 0.279
2 2018-04-01T01:40:00Z  USD 20.77
2 2018-04-01T18:00:00Z  EUR 20.169
3 2018-04-01T18:01:00Z  GBP 2
4 2018-04-01T00:01:00Z  USD 1.84
4 2018-04-01T00:01:00Z  GBP 2





```