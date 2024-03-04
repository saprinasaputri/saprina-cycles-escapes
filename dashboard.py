import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
# Set style seaborn
sns.set(style='dark')
# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by="dateday").agg({
        "count": "sum"
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by="dateday").agg({
        "casual": "sum"
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by="dateday").agg({
        "registered": "sum"
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by="season")[["registered", "casual"]].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df
# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df
# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df
# Load cleaned data
data_df = pd.read_csv("day_clean.csv")

datetime_columns = ["dateday"]
data_df.sort_values(by="dateday", inplace=True)
data_df.reset_index(inplace=True)
for column in datetime_columns:
    data_df[column] = pd.to_datetime(data_df[column])

# Filter data
min_date = data_df["dateday"].min()
max_date = data_df["dateday"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("Saprina Cycle Escapes Logo.jpg")
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Timeline",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = data_df[(data_df["dateday"] >= str(start_date)) & (data_df["dateday"] <= str(end_date))]
# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
# Dashboard
st.header("🚲Bike Rental Dashboard")
st.subheader("Daily Rentals")
col1, col2, col3 = st.columns(3)
with col1:
    daily_rent_casual = daily_casual_rent_df["casual"].sum()
    st.metric("Casual User", value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df["registered"].sum()
    st.metric("Registered User", value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df["count"].sum()
    st.metric("Total User", value= daily_rent_total)
##Bike rentals performance 
st.subheader("Bike Rentals Performance")
main_df["month"] = pd.Categorical(main_df["month"], categories=
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    ordered=True)

monthly_counts = main_df.groupby(by=["year", "month"]).agg({
    "count": "sum"
}).reset_index()
fig_bike_rentals, ax = plt.subplots(figsize=(24, 10))
palette=sns.color_palette("pastel")
sns.lineplot(
    data = monthly_counts,
    x = "month",
    y = "count",
    hue = "year",
    palette = palette,
    marker = "o"
)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title(f"Bike Rental Trends ({start_date} to {end_date})", fontsize=21)
plt.legend(title = "Year", loc = "upper right", fontsize = 16)
plt.gca().xaxis.grid(False)
st.pyplot(fig_bike_rentals)

## Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Weatherly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette='pastel',
    ax=ax
)
for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

##User performance
st.subheader("Users Performance")
metric_option = st.selectbox("Select Aggregation Type", ["sum", "max", "min", "mean"])

user_counts = main_df.groupby(by="year").agg({
    "casual": metric_option,
    "registered": metric_option
}).reset_index()

# Set the style
sns.set(style="whitegrid")

# Create a figure and axis
fig_users_performance, ax = plt.subplots(figsize=(24, 10))
# Plot the data using seaborn"s barplot
sns.barplot(data=user_counts, x="year", y="casual", color="skyblue", label="Casual Users")
sns.barplot(data=user_counts, x="year", y="registered", color="lightgoldenrodyellow", label="Registered Users", bottom=user_counts["casual"])

# Add label and title
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title(f"Comparison of Bike Rental between Casual and Registered Users ({metric_option})", fontsize=21)

# Add a legend
plt.legend(title = "User Type", loc = "upper right", fontsize = 16)

plt.grid(False)
st.pyplot(fig_users_performance)

# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='lightblue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='lightcoral',
    ax=ax
)
for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

##Season and Weather Rentals
st.subheader("Season and Weather Rentals")
fig_season_weather, ax = plt.subplots(figsize=(24, 10))
sns.barplot(
    x="season",
    y="count",
    hue="weather_cond",
    palette = ["purple","skyblue","pink"],
    data = main_df)

plt.title("Bike Rentals Based on Weather Conditions and Seasons", fontsize = 21)
plt.xlabel(None)
plt.ylabel(None)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize = 16)

st.pyplot(fig_season_weather)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Holiday, and Workingday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))
# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='count',
  data=weekday_rent_df,
  palette='pastel',
  ax=axes[0])

for index, row in enumerate(weekday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Bike Users based on Weekday')
axes[0].set_xlabel('Day of the Week')
axes[0].set_ylabel('Number of Bike Users')
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='count',
  data=holiday_rent_df,
  palette='pastel',
  ax=axes[1])

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Bike Users based on Holiday')
axes[1].set_xlabel('Holiday')
axes[1].set_ylabel('Number od Bike Users')
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette='pastel',
    ax=axes[2])

for index, row in enumerate(workingday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Bike Users based on Working Day')
axes[2].set_xlabel('Working Day')
axes[2].set_ylabel('Number of Bike Users')
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

##Workingday and Holiday Rentals
st.subheader("Workingday and Holiday Rentals")
fig_work_holiday, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

# Berdasarkan workingday
workingday_labels = ["Non-Workingday", "Workingday"]
ax[0].pie(main_df.groupby("workingday")["count"].sum(), 
          labels= workingday_labels,
          autopct='%1.1f%%',
          colors=["lightblue", "lightgreen"],
          textprops={'fontsize': 18})
ax[0].set_title("Percentage of Bike Rental by Workingday", fontsize=21)
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)

# Berdasarkan holiday
holiday_labels = ["Non-Holiday", "Holiday"]
ax[1].pie(main_df.groupby("holiday")["count"].sum(), 
          labels= holiday_labels, 
          autopct='%1.1f%%',
          colors=["lightblue", "lightgreen"],
          textprops={'fontsize': 18})
ax[1].set_title("Percentage of Bike Rental by Holiday", fontsize=21)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

plt.tight_layout()
st.pyplot(fig_work_holiday)

st.caption('Saprina Saputri M00D8D4KX3152')
