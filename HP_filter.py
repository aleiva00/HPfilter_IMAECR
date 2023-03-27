##########################################################################
#      PACKAGES
##########################################################################

# Data Mgmt
import pandas as pd

# Viz
import matplotlib.pyplot as plt
import seaborn as sns

# Stats & Math
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Operational/Format
import locale
from dateutil.relativedelta import relativedelta
import os

# Set time format as the local PC
locale.setlocale(locale.LC_TIME, '')


##########################################################################
#      HP FILTER & TAYLOR RULE
##########################################################################


# Read the DB with date as the index
df=pd.read_excel(r'C:/Users/Ale Leiva/Documents/GitHub/HPfilter_IMAECR/BD_TAYLOR.xlsx', index_col=("Fecha"))

# Use statsmodel to apply the hp filter in the IMAE and extract the cycle and trend
cycle, trend = sm.tsa.filters.hpfilter(df["IMAE_SA"], 129600 )

#Save the trend and cycle in the main DB
df["trend"]=trend
df["gap"]=cycle


# Fit OLS regression and save coefficients
model = smf.ols('TPM_MONTHLY ~ IPC_percent + gap', data=df).fit()
coef_INF = model.params['IPC_percent']
coef_GAP = model.params['gap']


##########################################################################
#      PLOTTING
##########################################################################

# Visualize results

#Make a copy of the main DB
df_plot=df.copy()

#Filter the start and end dates we want to visualize
startDate=df_plot.last_valid_index()+ relativedelta(years=-15) #Primera fecha
endDate=df_plot.last_valid_index()  #Última fecha
df_plot = df_plot.loc[startDate : endDate,:] 



# PLOTTING .............................................................
fig=plt.figure(figsize=(10, 6))

ax = fig.add_subplot()
plt.plot(df_plot.index, df_plot["TPM_MONTHLY"], label="TPM", color="green")
plt.plot(df_plot.index, model.fittedvalues, label="Taylor", color="black")


#Poner legend en upper left
plt.legend(loc="lower left")


#Poner ultimo punto del grafico
last_y_value=df_plot["TPM_MONTHLY"].iloc[-1]
last_x_value=endDate
ax.annotate(f'{last_y_value:.1f}',xy=(last_x_value,last_y_value), xycoords='data',xytext=(6,0), textcoords='offset points', fontsize=11)
plt.scatter(last_x_value, last_y_value, s=50, marker='o', facecolors='green', edgecolors='green')


#Poner ultimo punto del grafico
last_y_value2=model.fittedvalues.iloc[-1]
last_x_value2=endDate
ax.annotate(f'{last_y_value2:.1f}',xy=(last_x_value2,last_y_value2), xycoords='data',xytext=(6,0), textcoords='offset points', fontsize=11)
plt.scatter(last_x_value2, last_y_value2, s=50, marker='o', facecolors='black', edgecolors='black')



#SAVE FIGURE AS PDF--------------------------------------------
my_path= r"C:/Users/Ale Leiva/Documents/GitHub/HPfilter_IMAECR"
fig.savefig(os.path.join(my_path, 'TPM vs Taylor.png'), format="png", bbox_inches='tight')
#----------------------------------------------------------------
