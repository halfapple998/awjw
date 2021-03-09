# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import talib


'''
本策略以SHFE.rb2101为交易标的，根据其一分钟(即60s频度）bar数据建立双均线模型，
短周期为20，长周期为60，当短期均线由上向下穿越长期均线时做空，
当短期均线由下向上穿越长期均线时做多,每次开仓前先平掉所持仓位，再开仓。
注：为了适用于仿真和实盘，在策略中增加了一个“先判断是否平仓成功再开仓”的判断逻辑，以避免出现未平仓成功，可用资金不足的情况。
回测数据为:SHFE.rb2101的60s频度bar数据
回测时间为:2020-04-01 09:00:00到2020-05-31 15:00:00
'''


def init(context):
    context.short = 50                                             # 短周期均线
    context.long = 210                                              # 长周期均线
    context.symbol = 'DCE.p2105'                                 # 订阅交易标的
    context.period = context.long + 1                              # 订阅数据滑窗长度
    context.open_long = False                                      # 开多单标记
    context.open_short = False                                     # 开空单标记
    subscribe(context.symbol, '300s', count=context.period)         # 订阅行情


def on_bar(context, bars):
    if context.now.hour == 14 and context.now.minute == 59:
        return
    # 获取通过subscribe订阅的数据
    prices = context.data(context.symbol, '300s', context.period, fields='close')
    # 利用talib库计算长短周期均线
    short_avg = talib.SMA(prices.values.reshape(context.period), context.short)
    long_avg = talib.SMA(prices.values.reshape(context.period), context.long)

    # 查询持仓
    position_long = context.account().position(symbol=context.symbol, side=1)
    position_short = context.account().position(symbol=context.symbol, side=2)

    if (long_avg[-1] > bars[-1]['close']) and (long_avg[-1] < short_avg[-1]):
        # 无多仓情况下，直接开空
        if not position_long and not position_short:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(bars[-1]['close'])
            print(context.symbol, '以市价单调空仓到仓位')

    if min(short_avg[-1], long_avg[-1]) < bars[-1]['close']:
        if position_short:
            # 以市价平空仓
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy,
                         position_effect=PositionEffect_Close, order_type=OrderType_Market)
            print(bars[-1]['close'])
            print(context.symbol, '以市价单平空仓')

    if long_avg[-1] < bars[-1]['close'] and (long_avg[-1] > short_avg[-1]):
        # 无空仓情况下，直接开多
        if not position_short and not position_long:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(bars[-1]['close'])
            print(context.symbol, '以市价单调多仓到仓位')

    if max(short_avg[-1], long_avg[-1]) > bars[-1]['close']:
        if position_long:
            # 以市价平多仓
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Close,
                         order_type=OrderType_Market)
            print(bars[-1]['close'])
            print(context.symbol, '以市价单平多仓')


if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''
    run(strategy_id='ab15f0dd-7e8a-11eb-965a-bc307def78f9',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='a560536039a194786d5f9d68949a5d97f8f22041',
        backtest_start_time='2020-07-01 09:00:00',
        backtest_end_time='2021-03-05 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=50000,
        backtest_commission_ratio=0.00005,
        backtest_slippage_ratio=0.00005)

