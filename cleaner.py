import pandas as pd

accounts_df = pd.read_csv('./accounts_dirty.csv', delimiter=';')

def uploads_to_num(upload_str: str):
  uploads_formatted = upload_str.replace(',', '');
  return int(uploads_formatted)

accounts_df['uploads'] = accounts_df['uploads_str'].apply(uploads_to_num)


def subs_to_num(subs_str: str):
  subs_formatted = subs_str.replace('M', '');
  return int(float(subs_formatted) * 1000000)

accounts_df['subs'] = accounts_df['subs_str'].apply(subs_to_num)


def views_to_num(views_str: str):
  views_formatted = views_str.replace(',', '');
  return int(views_formatted)

accounts_df['views'] = accounts_df['views_str'].apply(views_to_num)


def min_earnings_to_num(earnings: str):
  earnings_formatted = earnings.split('  -  ')[0].replace('$', '');
  if 'K' in earnings_formatted:
    return int(float(earnings_formatted.replace('K', '')) * 1000)
  elif 'M' in earnings_formatted:
    return int(float(earnings_formatted.replace('M', '')) * 1000000)
  else:
    return int(earnings_formatted)

def max_earnings_to_num(earnings: str):
  earnings_formatted = earnings.split('  -  ')[1].replace('$', '');
  if 'K' in earnings_formatted:
    return int(float(earnings_formatted.replace('K', '')) * 1000)
  elif 'M' in earnings_formatted:
    return int(float(earnings_formatted.replace('M', '')) * 1000000)
  else:
    return int(earnings_formatted)

accounts_df['earnings_min'] = accounts_df['earnings'].apply(min_earnings_to_num)
accounts_df['earnings_max'] = accounts_df['earnings'].apply(max_earnings_to_num)


accounts_df = accounts_df[['name', 'uploads', 'subs', 'views', 'channel_type', 'country', 'earnings_min', 'earnings_max']]

accounts_df.to_csv('accounts.csv', sep=';', index=False)