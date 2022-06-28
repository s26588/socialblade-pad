import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
import plotly.express as px

accounts_df = pd.read_csv('./accounts.csv', delimiter=';')

model = smf.ols(formula="earnings_min ~ C(country) + C(channel_type) + uploads + subs + views", data=accounts_df).fit()
print(model.summary())
print()

print("P values:", model.pvalues.values)
print("Coef:", model.params.values)
print("Std err:", model.bse.values)
print()
print(accounts_df.corr())
print()

px.imshow(accounts_df.corr(), color_continuous_scale="Agsunset", title="Correlation heatmap")

# H0: there is no significant difference between polish and german channels (earning_max)
polish_accounts_df = accounts_df[accounts_df.country == 'PL']["earnings_max"]
german_accounts_df = accounts_df[accounts_df.country == 'DE']["earnings_max"]

statistic, pvalue = stats.ttest_ind(a=polish_accounts_df, b=german_accounts_df)
alpha = 0.05
print(statistic, pvalue);

if pvalue < alpha:
  print("Reject H0 hypothesis")
  print("So there is significant difference")
else:
  print("Don't reject H0 hypothesis")
  print("So there is no significant difference")

print()

# H0: there is no significant difference between 20 (limit) most popular educational and entertaining channels (views)
education_accounts_df = accounts_df[accounts_df.channel_type == 'Education']["views"].sort_values(ascending=False)[0:20]
entertainment_accounts_df = accounts_df[accounts_df.channel_type == 'Entertainment']["views"].sort_values(ascending=False)[:20]
statistic, pvalue = stats.ttest_ind(a=education_accounts_df, b=entertainment_accounts_df)
alpha = 0.05
print(statistic, pvalue);

if pvalue < alpha:
  print("Reject H0 hypothesis")
  print("So there is significant difference")
else:
  print("Don't reject H0 hypothesis")
  print("So there is no significant difference")