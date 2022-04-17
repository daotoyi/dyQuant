# dyQuant
Private Quant.

## dyrun

PyQt5 Entrance.

## monitor

Main programe dyQuant/monitor.

- schedule run
- test mode run
- judge trade date/time 
- thread monitor
- multi monitor terminal
  - WeChat
  - QQ
  - SMS
  - Mail
  - Toast
  - IFTTT


### moniStrategy

Strategy used for monitor.

- stocks
  - ak.stock_zh_a_spot_em
- futures
  - ak.futures_zh_spot
- options
  - classsify options category
  - financial
    - ak.option_cffex_hs300_daily_sina
    - ak.option_cffex_hs300_spot_sina
    - ak.option_sse_codes_sina
    - ak.option_sse_spot_price_sina
    - ak.option_sse_minute_sina
    - ak.option_sse_daily_sina
  - commodity
    - ak.option_current_em
    - ak.option_commodity_hist_sina

## underlying

Underlying list, Strict json formate.

## pyQt5Template

The interface framework imitating vnpy.