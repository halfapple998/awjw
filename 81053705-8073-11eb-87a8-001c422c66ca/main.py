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
    context.short = 50  # 短周期均线
    context.long = 210  # 长周期均线
    context.symbol = 'SHFE.rb2101'  # 订阅交易标的
    context.period = context.long + 1  # 订阅数据滑窗长度
    context.open_long = False  # 开多单标记
    context.open_short = False  # 开空单标记
    subscribe(context.symbol, '300s', count=context.period)  # 订阅行情


def on_bar(context, bars):
    # 获取通过subscribe订阅的数据
    prices = context.data(context.symbol, '300s', context.period, fields='close')

    # 利用talib库计算长短周期均线
    short_avg = talib.SMA(prices.values.reshape(context.period), context.short)
    long_avg = talib.SMA(prices.values.reshape(context.period), context.long)

    # 查询持仓
    position_long = context.account().position(symbol=context.symbol, side=1)
    position_short = context.account().position(symbol=context.symbol, side=2)

    if short_avg[-2] > short_avg[-1] and bars[0].close <= short_avg[-1]:

        if not position_long:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, 'kk')

        else:
            context.open_short = True

            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Close,
                         order_type=OrderType_Market)
            print(context.symbol, 'pd')

    if bars[0].close <= min(long_avg[-1], short_avg[-1]) and short_avg[-1] < short_avg[-2]:

        if not position_short and not position_long:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, 'kk')

        else:
            if position_long:
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Close,
                             order_type=OrderType_Market)
                print(context.symbol, 'pd')
            if not position_short:
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                             order_type=OrderType_Market)
                print(context.symbol, 'kk')

    elif bars[0].close >= max(long_avg[-1], short_avg[-1]) and short_avg[-1] > short_avg[-2]:
        if not position_short or not position_long:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, 'kd')

        else:
            if position_short:
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy,
                             position_effect=PositionEffect_Close, order_type=OrderType_Market)
                print(context.symbol, 'pk')
            if not position_long:
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy, position_effect=PositionEffect_Open,
                             order_type=OrderType_Market)
                print(context.symbol, 'kd')
    elif bars[0].close >= short_avg[-1]:
        if position_short:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy,
                         position_effect=PositionEffect_Close, order_type=OrderType_Market)
            print(context.symbol, 'pk')
    elif bars[0].close <= short_avg[-1]:
        if position_short:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Close,
                         order_type=OrderType_Market)
            print(context.symbol, 'pd')


if __name__ == '__main__':
    '''
        strategy_id策略ID,由系统生成
        filename文件名,请与本文件名保持一致
        mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID,可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
    '''
    run(strategy_id='81053705-8073-11eb-87a8-001c422c66ca',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='a560536039a194786d5f9d68949a5d97f8f22041',
        backtest_start_time='2020-04-01 09:00:00',
        backtest_end_time='2020-05-31 15:00:00',
        backtest_adjust=ADJUST_NONE,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)
