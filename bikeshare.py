import time
import pandas as pd
import numpy as np

from datetime import timedelta

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

df = pd.read_csv(CITY_DATA['chicago'])
print(df.head(7))


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    validity = False

    while True:
        # won't need try / catch because we're dealing with strings anyways
        # (and converting the prompt to strings anyway)
        # try:
        #     city = str(input("Type in city name: ").strip().lower())
        # except ValueError:
        #     print("Sorry, I'm looking for a string type")

        city = str(
            input("\nPick a city (chicago, new york city, washington): ").strip().lower())

        if city not in ("chicago", "new york city", "washington"):
            print("\nInvalid Response. Please try again")
            continue
        else:
            print("\nIt looks like you want to see data for: '{}' ".format(city.title()))
            validity = str(input(
                "Is that correct? Type 'y' to continue and 'n' to restart: \n").strip().lower())
            if validity == 'y':
                break
            else:
                get_filters()

    # criteria = str(input("Would you like to filter the data by month, day, both or not at all? Type 'None' for no time filter").strip().lower())

    # if criteria not in ("month", "day", "both")
    while True:
        month = str(
            input("\nType in name of month to filter by (i.e. January): ").strip().lower())

        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print(
                "\nInvalid. Please type in month name (or \"all\" to select every month)")
            continue
        else:
            print("\nIt looks like you want to filter by: '{}' ".format(month.title()))
            validity_m = str(input(
                "Is that correct? Type 'y' to continue and 'n' to restart: \n").strip().lower())
            if validity_m == 'y':
                break
            else:
                get_filters()

    while True:
        day = str(
            input("\nType in name of day to filter by (i.e. Monday): ").strip().lower())

        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"):
            print("Invalid. Please type in valid day (or \"all\" to select every day)")
            continue
        else:
            print("\nIt looks like you want to filter by: '{}' ".format(day.title()))
            validity_d = str(input(
                "Is that correct? Type 'y' to continue and 'n' to restart: \n").strip().lower())
            if validity_d == 'y':
                break
            else:
                get_filters()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or "all" to apply no month filter
       (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
       df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month / day of week / Hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        # indexing from 0
        month = months.index(month) + 1

        # month returns a number after getting input from the function argument
        # this is because (dt.month) returns a number

        # In the following statement: (df['month'] == month), df['month'] is assigned a number (bc month is number from above)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Use df.mode() to compute most often data --> outputs it as a tabular data with row 0
    # and then access it with indexing (ie [0])

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.mode.html

    # look_up dictionary
    look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
               '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_in_string = look_up[str(popular_month)]
    print("The most common month is: ", month_in_string)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('The most common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station was: {}".format(start_station))

    # display most commonly used end station

    end_station = df['End Station'].mode()[0]
    print("Most commonly used end station was: {}".format(end_station))

    # display most frequent combination of start station and end station trip

    # outputs dtype: int64 --> if I try to slice into it ex) pair[0], I get one number!
    # thus must use the form below (table form)
    pair = df.groupby(['Start Station', 'End Station']
                      ).size().sort_values(ascending=False)

    # outputs a table (with different dtypes per column) --> I think the reset_index makes the datatype into a table
    pair_2 = df.groupby(['Start Station', 'End Station']
                        ).size().reset_index(name="counts")
    pair_final = df.groupby(['Start Station', 'End Station']).size(
    ).sort_values(ascending=False).reset_index(name="counts")

    frequent_start_pair = pair_final['Start Station'][0]
    frequent_end_pair = pair_final['End Station'][0]

    print("The start station for most frequent combination is {} and the end station is {}".format(
        frequent_start_pair, frequent_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # from the load_data function, df is already given as filtered
    # (meaning that the rows are shortened (less than the total number of rows in a dataframe))
    # thus only need to find the TOTAL SUM of the column 'DURATION'

    # https://stackoverflow.com/questions/41286569/get-total-of-pandas-column
    # display total travel time

    # import timedelta!!! s
    total_travel_time = df['Trip Duration'].sum()

    # use timedelta function to output duration
    # yet for some reason, timedelta() doesn't accept int32,64 as valid dtype
    # thus need to cast it as float

    t2 = total_travel_time.astype('float64', copy=False)
    time_in_duration = timedelta(seconds=t2)
    print("The total travel time in seconds is: {} which converts to {} in duration ".format(
        total_travel_time, time_in_duration))

    # display mean travel time

    # Refereence:
    # https://stackoverflow.com/questions/31037298/pandas-get-column-average-mean

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time is: '{}' ".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    # Display counts of gender
    # tried to use try / except block but udacity thread pointed me towards if statement to generalize!
    # Reference: https://study-hall.udacity.com/rooms/community:nd104:645596-project-328/community:thread-11448949055-512760?contextType=room
    # https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers

    # df.columns returns the list of column index in DataFrame
    # if "Gender" isn't included in that list, then execute code, otherwise print statement
    if "Gender" in df.columns:
        gender_count = df["Gender"].value_counts()

        # to count null values
        # Reference: https://stackoverflow.com/questions/26266362/how-to-count-the-nan-values-in-a-column-in-pandas-dataframe
        nan_values = df["Gender"].isna().sum()

        print("\nCounts by Gender: \n{}\n \n*Note: there were '{}' NaN values for gender column".format(gender_count, nan_values))
    else:
        print("No such column exists in this dataset")

    # Display earliest, most recent, and most common year of birth

    if "Birth Year" in df.columns:

        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(
            earliest, most_recent, most_common))

    else:
        print("\nNo column named 'Birth Year' exists in this dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()