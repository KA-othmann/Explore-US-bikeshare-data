import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    city = ""
    month = ""
    day = ""
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        except ValueError:
            continue
        if city in CITY_DATA:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        try:
            month = input("Which month - January, February, March, April, May, June or All?\n").lower()
        except ValueError:
            continue
        if month in months:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    week_days = ['wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'monday', 'tuesday', 'all']
    while True:
        try:
            day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All?\n").lower()
        except ValueError:
            continue
        if day in week_days:
            break

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city],skip_blank_lines=True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # create hour and week day columns
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def most_common(df, value):
    """
    Returns the most common value from a DataFrame.
    It checks whether we applied a filter for certain values and return the mode as the most common value
    Input: (DataFrame) df - the name of the dataframe
            (str) value - the value you want to compute the mode for
    Output: prints the most common value
    """
    if len(df[value].unique()) > 1:
        popular_value = df[value].mode()
        print(f"The most common {value} is: {popular_value[0]}")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common(df, "month")

    # TO DO: display the most common day of week
    most_common(df, "day_of_week")

    # TO DO: display the most common start hour
    most_common(df, 'hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common(df, "Start Station")

    # TO DO: display most commonly used end station
    most_common(df, "End Station")

    # TO DO: display most frequent combination of start station and end station trip
    df["Start Station to End Station"] = "From " + df["Start Station"] + " to " + df["End Station"]
    most_common(df, "Start Station to End Station")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"The total travel time is: {total_travel_time / 86400} day(s)")

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"The mean travel time is: {mean_travel_time / 60} minute(s)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("The counts of user types:\n", user_types)
    try:
        # Display counts of gender
        genders = df["Gender"].value_counts()
        print("The counts of gender:\n", genders)
        # Display earliest, most recent, and most common year of birth
    except KeyError:
        print("")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    view_display= input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while view_display.lower() == "yes" and start_loc < df.shape[0]-5 :
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you want to see the next 5 rows of data: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

        

if __name__ == "__main__":
    main()
