import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
def invalid_input_msg():
    print('<**> That is not a valid selection.  Please try again. <**>\n')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # This function is here just for testing purposes.

    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

    city = ''
    while city not in cities:
        city = input("Enter the city name you'd like to analyze.  Your options are Chicago, New York City, and Washington\n --> ").lower()
        if city not in cities:
            invalid_input_msg()
    print("\nYou've chosen to analyze {}.".format(city))

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in months:
        month = input("What month would you like to analyze.  Input 'all' for all of them.\n --> ").lower()
        if month not in months:
            invalid_input_msg()
    print("\nYou've chosen to filter by {}.".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in days:
        day = input("What day of the week would you like to analyze.  Input 'all' for all of them.\n --> ").title()
        if day not in days:
            invalid_input_msg()
    print("\nYou've chosen to filter by {}.".format(day))

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Create dataframe from csv file
    df = pd.read_csv(CITY_DATA[city])

    #Convert start time to datetime and extract month, day, and hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    #Filter by month and day if desired
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    #days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'All':
        #day = days.index(day) + 1
        df = df[df['Day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The most popular month is {}.'.format(most_common_month))

    # display the most common day of week
    most_common_dow = df['Day_of_week'].mode()[0]
    print('The most popular day of the week is {}.'.format(most_common_dow))

    # display the most common start hour
    most_common_time = df['Hour'].mode()[0]
    print('The most common start hour is {}.'.format(most_common_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    max_start = df['Start Station'].mode()[0]
    print('The station with the most departures was {}.'.format(max_start))

    # display most commonly used end station
    max_end = df['End Station'].mode()[0]
    print('the number one destination was {}.'.format(max_end))

    # display most frequent combination of start station and end station trip
    group_trips = df.groupby(['Start Station', 'End Station'])
    max_trips = group_trips.size().sort_values(ascending=False).head(1)
    print('The most popular trip starts and ends at {}.'.format(max_trips))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is {}.'.format(total_time))

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print('The average travel time is {}.'.format(average_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Statistics:')
    print(df['User Type'].value_counts())

    if city == 'washington':
        print('Gender statistics not available.')
        print('Birth year statistics not available.')
    else:
        # Display counts of gender
        print('\nGender data:')
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nBirth year data:')
        print('The most common birth year is {}.'.format(df['Birth Year'].mode()[0]))
        print('The most recent birth year is {}.'.format(df['Birth Year'].max()))
        print('The earliest birth year is {}.'.format(df['Birth Year'].min()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    # If the user desires they can display five rows of raw data.
    see_raw = input('\nWould you like to view 5 rows of data? (yes / no):\n --> ').lower()
    if see_raw == 'yes':
        index = 0
        while (index < df['Start Time'].count() and see_raw != 'no'):
            print(df.iloc[index:index+5])
            index += 5
            see_more = input('\nWould you like to seen an additional 5 rows? (yes / no):\n --> ').lower()
            if see_more != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()