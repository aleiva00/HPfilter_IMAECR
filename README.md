# HP Filter & Taylor Rule CRI

# Intro
This is a short project that utilizes the statsmodels package to apply the Hodrick-Prescott (HP) filter to the IMAE indicator from Costa Rica. The objective is to obtain the output gap, which is the difference between the actual level of economic output and its potential level. This output gap will be used to estimate Taylor's rule, which is a widely used monetary policy rule that links changes in the interest rate to changes in the output gap and inflation. By comparing the estimated interest rate using Taylor's rule to the actual monetary policy rate, we can gain insight into whether the central bank's monetary policy is aligned with the rule or not.

# Steps
First we import the packages we're going to use:
```
# Data Mgmt
import pandas as pd

# Viz
import matplotlib.pyplot as plt

# Stats & Math
import statsmodels.api as sm
import statsmodels.formula.api as smf

```
After that, we read the database with pandas. In this case I used the column of dates ('Fecha') as the index since it then will make it easier to plot the results with the matplotlib package.

```
df=pd.read_excel(r'BD_TAYLOR.xlsx', index_col=("Fecha"))
```
Then, we apply the HP filter with the statsmodel package:
```
cycle, trend = sm.tsa.filters.hpfilter(df["IMAE_SA"], 129600 )

df["trend"]=trend
df["gap"]=cycle
```
This code uses the hpfilter() function from the statsmodels package to apply the Hodrick-Prescott (HP) filter to a time series of the IMAE indicator, which measures the monthly economic activity in Costa Rica. The function takes two arguments: the first argument (df["IMAE_SA"]) is the time series to be filtered, and the second argument (129600) is the smoothing parameter or lambda value used in the HP filter.

The HP filter separates a time series into two components: the trend and the cycle. The trend is the long-term behavior of the series, while the cycle represents short-term fluctuations around the trend. The output of hpfilter() function are two arrays, cycle and trend, representing the filtered values of the cycle and trend components of the original time series.

The code then saves the trend and cycle components in the main data frame (df) by creating two new columns named "trend" and "gap", respectively. These columns will be used to estimate Taylor's rule and to compare it with the actual monetary policy rate.

After that, the final step is to estimate the Taylor's Rule using OLS. 



```
model = smf.ols('TPM_MONTHLY ~ IPC_percent + gap', data=df).fit()
coef_INF = model.params['IPC_percent']
coef_GAP = model.params['gap']
```
This code uses the ols() function from the statsmodels.formula.api module to fit a linear regression model to the data in the df DataFrame. The model relates the monthly monetary policy rate (TPM_MONTHLY) to two predictor variables: the percentage change in the consumer price index (IPC_percent) and the output gap (gap).

The fit() method is used to estimate the model coefficients using the least squares method. The code then extracts the estimated coefficients of the IPC_percent and gap variables from the params attribute of the fitted model and stores them in the variables coef_INF and coef_GAP, respectively. These coefficients will be used to evaluate how well the estimated interest rate using Taylor's rule matches the actual monetary policy rate.



# Results
![TPM vs Taylor](https://user-images.githubusercontent.com/82245658/227847747-21497b7f-7185-4d52-9d26-fb42844fdde7.png)
After graphing the results, it appears that there is a notable alignment between the Taylor criterion and the monetary policy decisions of the Central Bank of Costa Rica (BCCR). This finding suggests that it could be worthwhile to closely monitor the Taylor criterion as a means of anticipating the BCCR's decisions or understanding the reasoning behind its monetary policy choices. It is important to note, however, that this methodology serves as an indicator and is not a perfect predictor. There are econometric limitations associated with these types of methodologies, which have been the subject of criticism in the economic academic literature. Despite these limitations, this approach has a favorable cost ratio to implement as an indicator and provides valuable information for analyzing the country's monetary environment with just a few simple steps.
