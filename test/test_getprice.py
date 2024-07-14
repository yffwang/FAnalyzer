import Ashare as Ash
import pandas as pd

# 设置显示最多 100 行 20 列
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 20)

df = Ash.get_price('sh601988', frequency='1d', count=300)
# df.sort_index(ascending=True, inplace=True)

df['MA5'] = df['close'].rolling(window=5).mean()
df['MA10'] = df['close'].rolling(window=10).mean()

df_trimmed = df.drop(index=df.index[:9])

hasbuy = False
boughtPrice = 0.00
for i in range(len(df_trimmed)):
    pre_day = df_trimmed.iloc[i - 1] if i > 0 else None
    today = df_trimmed.iloc[i]
    next_day = df_trimmed.iloc[i + 1] if i < len(df_trimmed) - 1 else None

    if pre_day is None:
        continue
    if next_day is None:
        break

    if not hasbuy and today['MA10'] <= today['MA5'] <= today['close'] and pre_day['MA10'] > pre_day['MA5']:
        print('[' + today['day'].strftime('%Y-%m-%d') + ']' + '买入价格为', next_day['open'], ' 当日价格区间',
              next_day['low'], '-', next_day['high'], '\n')
        boughtPrice = next_day['open']
        hasbuy = True

    if hasbuy and today['MA10'] > today['MA5']:
        percentage = ((next_day['open'] - boughtPrice) / boughtPrice) * 100
        formatted_percentage = f"{percentage:.2f}"
        print('[' + today['day'].strftime('%Y-%m-%d') + ']' + '卖出价格为', next_day['open'], ' 当日价格区间',
              next_day['low'], '-', next_day['high'], f"获得利润为 {formatted_percentage}% \n")
        boughtPrice = 0.00
        hasbuy = False

print('中国银行日线行情\n', df)
