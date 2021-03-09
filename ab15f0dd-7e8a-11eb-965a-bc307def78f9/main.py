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
    context.stoppp = 0
    context.time1 = 0
    subscribe(context.symbol, '300s', count=context.period)         # 订阅行情


def on_bar(context, bars):
    if (context.now.hour == 14 and context.now.minute == 59) or (context.now.hour == 22 and context.now.minute == 59):
        return

    if context.time1 == context.now.day:
        return
        # order_close_all()
        # print('全部平仓')
        # context.count = 0
    # 获取通过subscribe订阅的数据
    prices = context.data(context.symbol, '300s', context.period, fields='close')
    # 利用talib库计算长短周期均线
    # short_avg = talib.SMA(prices.values.reshape(context.period), context.short)
    long_avg = talib.SMA(prices.values.reshape(context.period), context.long)

    # 查询持仓
    position_long = context.account().position(symbol=context.symbol, side=1)
    position_short = context.account().position(symbol=context.symbol, side=2)

    if long_avg[-1] > bars[-1]['close']:
        # 无多仓情况下，直接开空
        if not position_long and not position_short:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, '以市价单调空仓到仓位')

        # 有多仓情况下，先平多，再开空(开空命令放在on_order_status里面)
        else:
            if position_long:
                context.open_short = True

                if (bars[-1]['close'] - int(position_long.vwap)) < 0:
                    context.stoppp += 1
                else:
                    context.stoppp = 0

                # 以市价平多仓
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Close,
                             order_type=OrderType_Market)
                print(context.symbol, '以市价单平多仓')

    if long_avg[-1] < bars[-1]['close']:
        # 无空仓情况下，直接开多
        if not position_short and not position_long:
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, '以市价单调多仓到仓位')

        else:
            if position_short:
                context.open_long = True

                if (int(position_short.vwap) - bars[-1]['close']) < 0:
                    context.stoppp += 1
                else:
                    context.stoppp = 0

                # 以市价平空仓
                order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy,
                             position_effect=PositionEffect_Close, order_type=OrderType_Market)
                print(context.symbol, '以市价单平空仓')

    if context.stoppp > 2:
        context.time1 = context.now.day
        return

def on_order_status(context, order):
    # 查看下单后的委托状态
    status = order['status']
    # 成交命令的方向
    side = order['side']
    # 交易类型
    effect = order['position_effect']
    # 当平仓委托全成后，再开仓
    if status == 3:
        # 以市价开空仓，需等到平仓成功无仓位后再开仓
        # 如果无多仓且side=2（说明平多仓成功），开空仓
        if effect == 2 and side == 2 and context.open_short:
            context.open_short = False
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Sell, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, '以市价单调空仓到仓位')
        # 以市价开多仓,需等到平仓成功无仓位后再开仓
        # 如果无空仓且side=1（说明平空仓成功），开多仓
        if effect == 2 and side == 1 and context.open_long:
            context.open_long = False
            order_volume(symbol=context.symbol, volume=1, side=OrderSide_Buy, position_effect=PositionEffect_Open,
                         order_type=OrderType_Market)
            print(context.symbol, '以市价单调多仓到仓位')


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
        backtest_start_time='2020-09-01 09:00:00',
        backtest_end_time='2021-03-05 15:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=20000,
        backtest_commission_ratio=0.00005,
        backtest_slippage_ratio=0.00005)

