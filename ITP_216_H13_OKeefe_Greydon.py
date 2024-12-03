import pandas as pd
import matplotlib.pyplot as plt

# Greydon O'Keefe, gokeefe@usc.edu
# ITP 216, Fall 2024
# Section: 32081
# Assignment 13
# Description:
    # Climatology homework assignment


def main():
    # reading in the dataset
    df = pd.read_csv("jfk_weather.csv")

    # removing rows of data where the observed temp is null
    df = df[df["TAVG"].notnull()]

    # making a column for year: allows us to easily get the last 10 years
    df["YEAR"] = df["DATE"].str[:4]
    years_list = list(df["YEAR"].unique())

    # making a column for month: allows us to group by month
    df["MONTH_DAY"] = df["DATE"].str[-5:]
    df = df[df['MONTH_DAY'] != '02-29']  # drop leap years
    month_days_list = list(df["MONTH_DAY"].unique())

    df.sort_values(inplace=True, by='MONTH_DAY')

    # list of months to label the x-axis of both graphs
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # calculate historical average temperatures
    historical_avg = df.groupby("MONTH_DAY")["TAVG"].mean()

    # filter data by most recent 10 years
    recent_years = years_list[-10:]
    recent_data = df[df["YEAR"].isin(recent_years)]

    # set up plots
    fig, ax = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle("Yearly climatological data for city New York from 2014 to 2024", fontsize=14)

    # top plot
    for year in recent_years:
        year_data = recent_data[recent_data["YEAR"] == year]
        ax[0].plot(year_data["MONTH_DAY"], year_data["TAVG"], label=year)
    ax[0].set_title("Most recent 10 years")
    ax[0].set_xlabel("Month")
    ax[0].set_ylabel("temp (F)")
    ax[0].set_xticks([f"{month:02d}-01" for month in range(1, 13)])
    ax[0].set_xticklabels(month_list)
    ax[0].legend(title="Year")

    # bottom plot
    year_2021 = df[df["YEAR"] == "2019"]
    ax[1].bar(historical_avg.index, historical_avg, label="historical average", alpha=0.7, color="blue", width=1.0)
    ax[1].bar(year_2021["MONTH_DAY"], year_2021["TAVG"], label="2019", alpha=0.7, color="red", width=1.0)
    ax[1].set_title("Comparing current year and historical averages")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("temp (F)")
    ax[1].set_xticks([f"{month:02d}-01" for month in range(1, 13)])
    ax[1].set_xticklabels(month_list)
    ax[1].legend()

    plt.tight_layout(rect=(0.0, 0.0, 1.0, 1.0))
    plt.show()

if __name__ == '__main__':
    main()
