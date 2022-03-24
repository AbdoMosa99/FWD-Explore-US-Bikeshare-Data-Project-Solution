from datetime import datetime, timedelta
import time
from typing import Callable
import pandas as pd


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv',
}


MONTHS = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'Aug': 8,
    'Sept': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


DAYS = {
    'Sat': 1,
    'Sun': 2,
    'Mon': 3,
    'Tue': 4,
    'Wed': 5,
    'Thu': 6,
    'Fri': 7,
}


def week_monday_to_saturday(day: int) -> int:
    """Convert a day from Monday-start format to Saturday-start format!
        From Monday = 0
        To Saturday = 1
    """
    return (day + 2) % 7 + 1


def get_key_from_value(dictionary, value):
    """For a given dict, get the key of the 'value' parameter."""
    return list(dictionary.keys())[
        list(dictionary.values()).index(value)
    ]


def convert_hour_24_to_12(hour24: int) -> str:
    """Converts a 24 hour represented as int e.g. 17
        to a 12 hour string e.g. "5 PM"
    """
    am_or_pm = "PM" if hour24 >= 12 else "AM"
    hour12 = hour24 - 12 if hour24 > 12 else hour24
    hour12 = 12 if hour12 == 0 else hour12
    return f"{hour12} {am_or_pm}"


def timedelta_to_str(time_d: timedelta) -> str:
    """A function that takes a timedelta object
        returns its custom string representation."""
    days = time_d.days
    left_seconds = time_d.seconds
    hours = left_seconds // (60 * 60)
    left_seconds = left_seconds % (60 * 60)
    mins = left_seconds // 60

    if days:
        return f"{days} days, {hours} hours, and {mins} minutes"
    elif hours:
        return f"{hours} hours and {mins} minutes"
    else:
        return f"{mins} minutes"


def get_data_entry(prompt: str, validation_func: Callable):
    """A function that keeps asking the user for some input 
    until it's valid then returns that input."""
    while True:
        entry = input(prompt)
        if validation_func(entry):
            return entry
        else:
            print("\nInvalid Input! Try Again.\n")


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
    city = get_data_entry(
        prompt=(
            "\nChoose which city to analyze.\n"
            " - 1 for Chicago\n"
            " - 2 for New York\n"
            " - 3 for Washignton\n"
            "> "
        ),
        validation_func=lambda city: city in ("1", "2", "3"),
    )
    city = list(CITY_DATA.keys())[int(city)-1]

    # get user input for month (all, january, february, ... , june)
    month = get_data_entry(
        prompt=(
            "\nChoose which month to analyze.\n"
            f"  {list(MONTHS.keys())}\n"
            "  Or press enter to get the whole year.\n"
            "> "
        ),
        validation_func=lambda mo: mo == "" or mo in MONTHS.keys(),
    )
    if month == "":
        month = "all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_data_entry(
        prompt=(
            "\nChoose which day to analyze.\n"
            f"  {list(DAYS.keys())}\n"
            "  Or press enter to get the whole week.\n"
            "> "
        ),
        validation_func=lambda d: d == "" or d in DAYS.keys(),
    )
    if day == "":
        day = "all"

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
    start_time = time.time()
    print("\nLoading data...\n")

    df = pd.read_csv(CITY_DATA[city])

    # format date data into datetime objects
    df['Start Time'] = df['Start Time'].map(
        lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    )
    df['End Time'] = df['End Time'].map(
        lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    )

    # filter by month
    if month != "all":
        filter_list = []  # True and False list
        for start_date in df["Start Time"]:
            filter_list.append(
                start_date.month == MONTHS[month]
            )
        df = df[filter_list]

    # filter by day
    if day != "all":
        filter_list = []
        for start_date in df["Start Time"]:
            filter_list.append(
                week_monday_to_saturday(start_date.weekday()) == DAYS[day]
            )
        df = df[filter_list]

    time_taken = time.time() - start_time
    print(f"\nThis took {time_taken:.2f} seconds.")
    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # count every day, month, and hour
    month_counts = [0] * 12
    weekday_counts = [0] * 7
    hour_counts = [0] * 24
    for start_date in df['Start Time']:
        month_counts[start_date.month - 1] += 1
        weekday_counts[week_monday_to_saturday(start_date.weekday()) - 1] += 1
        hour_counts[start_date.hour] += 1

    # get max of each along with how many occurences

    max_month = 0
    max_month_count = 0
    for i, count in enumerate(month_counts):
        if count > max_month_count:
            max_month_count = count
            max_month = i + 1

    max_weekday = 0
    max_weekday_count = 0
    for i, count in enumerate(weekday_counts):
        if count > max_weekday_count:
            max_weekday_count = count
            max_weekday = i + 1

    max_hour = 0
    max_hour_count = 0
    for i, count in enumerate(hour_counts):
        if count > max_hour_count:
            max_hour_count = count
            max_hour = i

    # display the most common month
    month = get_key_from_value(MONTHS, max_month)
    print(
        f"The most common month is \"{month}\""
        f" with {max_month_count} total trips."
    )

    # display the most common day of week
    day = get_key_from_value(DAYS, max_weekday)
    print(
        f"The most common weekday is \"{day}\""
        f" with {max_weekday_count} total trips."
    )

    # display the most common start hour
    hour = convert_hour_24_to_12(max_hour)
    print(
        f"The most common start hour is \"{hour}\""
        f" with {max_hour_count} total trips."
    )

    time_taken = time.time() - start_time
    print(f"\nThis took {time_taken:.2f} seconds.")
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # count using pandas
    most_start_station = df['Start Station'].mode()[0]
    most_start_station_count = df[
        df['Start Station'] == most_start_station
    ]['Start Station'].count()

    most_end_station = df['End Station'].mode()[0]
    most_end_station_count = df[
        df['End Station'] == most_end_station
    ]['End Station'].count()

    combinations = df.groupby(['Start Station', 'End Station'])\
        .size().reset_index().rename(columns={0: 'count'})
    most_combination_count = combinations['count'].max()
    most_combination = combinations[
        combinations['count'] == most_combination_count
    ].iloc[0]

    # display most commonly used start station
    print(
        f"The most common start station is \"{most_start_station}\""
        f" with {most_start_station_count} total trips."
    )

    # display most commonly used end station
    print(
        f"The most common end station is \"{most_end_station}\""
        f" with {most_end_station_count} total trips."
    )

    # display most frequent combination of start station and end station trip
    start_station = most_combination['Start Station']
    end_station = most_combination['End Station']
    print(
        f"The most common combination is \"{start_station} to"
        f" {end_station}\" with {most_combination_count} total trips."
    )

    time_taken = time.time() - start_time
    print(f"\nThis took {time_taken: .2f} seconds.")
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_travel_time = timedelta(seconds=total_travel_time)
    total_travel_time = timedelta_to_str(total_travel_time)
    print(f"The total travel time is \"{total_travel_time}\".")

    # display mean travel time
    avg_travel_time = int(df['Trip Duration'].mean())
    avg_travel_time = timedelta(seconds=avg_travel_time)
    avg_travel_time = timedelta_to_str(avg_travel_time)
    print(f"The average travel time is \"{avg_travel_time}\".")

    time_taken = time.time() - start_time
    print(f"\nThis took {time_taken:.2f} seconds.")
    print('-'*40)


def user_stats(df: pd.DataFrame):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    grouped = df.groupby('User Type').size().reset_index()\
        .rename(columns={0: 'count'})
    print("Count of user types:")
    for i in range(len(grouped)):
        print(f"\t{grouped['User Type'][i]}: {grouped['count'][i]}")

    print()

    # Display counts of gender
    grouped = df.groupby('Gender')\
        .size().reset_index().rename(columns={0: 'count'})
    print("Count of genders:")
    for i in range(len(grouped)):
        print(f"\t{grouped['Gender'][i]}: {grouped['count'][i]}")

    print()

    # Display earliest, most recent, and most common year of birth
    earliest = int(df['Birth Year'].min())
    recent = int(df['Birth Year'].max())
    common = int(df['Birth Year'].mode()[0])
    print("Birth Years:")
    print(f"\tEarliest: {earliest}")
    print(f"\tMost recent: {recent}")
    print(f"\tMost common: {common}")

    time_taken = time.time() - start_time
    print(f"\nThis took {time_taken:.2f} seconds.")
    print('-'*40)


def view_data(df: pd.DataFrame):
    """
    A function that shows the user the given 
    DataFrame 5 rows in a row upon their request.
    """
    answer = input(
        '\nWould you like to view 5 rows of individual trip data?\n'
        'Enter yes or no\n'
    )

    start_loc = 0
    while answer.lower() == 'yes' and start_loc < len(df):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        answer = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington':
            user_stats(df)

        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
