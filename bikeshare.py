import time
import datetime
import pandas as pd
import numpy as np
from tabulate import tabulate

#declare constant dictionaries
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv','atlanta':'atlanta.csv' }
MONTH = {'1':'January',
         '2':'February',
         '3':'March',
         '4':'April',
         '5':'May',
         '6':'June',
         '7':'July',
         '8':'August',
         '9':'September',
         '10':'October',
         '11':'November',
         '12':'December',
         'all':'All Months'}
WEEKDAY = {'0':'Monday',
            '1':'Tuesday',
            '2':'Wednesday',
            '3':'Thursday',
            '4':'Friday',
            '5':'Saturday',
            '6':'Sunday',
            'all':'All Days'}

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class UserInvalidEntry(Error):
    """Raised when the user enters an invalid entry"""
    pass

class UserAborted(Error):
    """Raised when the user aborts a filter request"""
    pass



def get_filter_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    """
    #define the valid user input options
    validcities=['Chicago','Washington','New York City','Atlanta']

    #get a comma seperated string for labels
    city_label = ", ".join(validcities)

    # get user input for city (chicago, new york city, washington,'atlanta'). 
    while True:
        try:
            city = input("Which city would you like to analyze, type {} or X to abort: ".format(city_label)).title().split(",")
 
            #check city is valid, if not; message user (include option X to abort) and exit
            if city[0] in validcities:
                break
            elif city[0].lower()=="x":
                raise UserAborted
            else:    
                raise UserInvalidEntry("{} is not a valid city, please enter {} or X to abort'".format(city[0],city_label))
        except UserInvalidEntry as e:
            print("Invalid entry: {}".format(e))
        except UserAborted:
            #raise the error to calling procedure
            raise
        except Exception:
            print("Exception occurred: {}".format(e))

    return city[0]
            
def get_filter_month():
    """
    Asks user to specify a month to analyze.

    Returns:
        (str) month - numeric string(1-12) of the month to filter by, or "all" to apply no month filter
    """
   # get user input for month (all, january, february, ... , june)
    while True:
        try:      
            month = input("Enter the months to analyze (1-12), 'all' or X to abort: ").title().split(",")

            #check nominated month is valid, if not; message the user (include option X to abort) and exit
            if month[0].lower()=="x":
                raise UserAborted
            elif (month[0].isdigit() and 1 <= int(month[0]) <= 12) or month[0].lower()=="all":
                break
            else:
                raise UserInvalidEntry("{} is not a valid month, please enter a numeric between 1 and 12, all, or X to abort'".format(month[0]))
        except UserInvalidEntry as e:
            print("Invalid entry: {}".format(e))
        except UserAborted:
            #raise the error to calling procedure
            raise
        except Exception:
            print("Exception occurred: {}".format(e))
    
    #return the string that represents the month
    return month[0].lower()

def get_filter_day():
    """
    Asks user to specify a weekday to analyze.

    Returns:
        (str) day - numeric string(0-6) of the day of week to filter by (where 0 = Monday), or "all" to apply no day filter
    """
    #define the valid user input options
    validdays={'M':'0','Tu':'1','W':'2','Th':'3','F':'4','Sa':'5','Su':'6','All':'all'}

    #get a comma seperated string for labels
    day_label = ", ".join(validdays)

   #get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Enter the days to analyze ({}), or type X to abort: ".format(day_label)).title().split(",")

            #check day is valid, if not; message user (include option X to abort) and exit
            if day[0] in validdays:
                #valid selection, exit while
                break
            elif day[0].lower()=="x":
                #abort request, raise abort exception
                raise UserAborted
            else:
                #user input invalid    
                raise UserInvalidEntry("{} is not a valid day, please enter '{}' or X to abort'".format(day[0],day_label))

        except UserInvalidEntry as e:
            print("Invalid entry: {}".format(e))
        except UserAborted:
            #raise the error to calling procedure
            raise
        except Exception:
            print("Exception occurred: {}".format(e))

    #return the numeric equivalent string for the valid day
    return validdays.get(day[0])

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - numeric string(1-12) of the month to filter by, or "all" to apply no month filter
        (str) day - numeric string(0-6) of the day of week to filter by (where 0 = Monday), or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    try:
        #retrieve the city to be evaluated
        city = get_filter_city()

        #retrieve the month  to be evaluated
        month = get_filter_month()

        #retrieve the day of week to be evaluated
        day = get_filter_day()       
    except:
        #user aborted - return nothing to trigger restart
        return None,None,None
        
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
    #read data from appropriate file based on city.
    df = pd.read_csv("./"+ CITY_DATA.get(city),parse_dates=['Start Time','End Time'])

    #drop any column that doesn't have a name
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)

    #df.rename({'Birth_Year':'Birth_Year','Start_Time':'Start_Time',''},axis=1, inplace=True)
    df.columns = df.columns.str.replace(' ','_')
    
    #add column to represent start month
    df['start_month']= pd.DatetimeIndex(df['Start_Time']).month

    #add column to represent start day
    df['start_day']= pd.DatetimeIndex(df['Start_Time']).dayofweek

    #drop the rows that represent months we don't want
    if month.lower() != 'all':
        df.drop(df[df.start_month != int(month)].index, inplace=True)
 
    #drop the rows that represent days we don't want
    if day.lower() != 'all':
        df.drop(df[df.start_day != int(day)].index, inplace=True)  

    return df

def view_raw_data(df):
    """
    Displays ten lines of raw data from the dataframe until the user indicates they do not want to see more.
   
    Args:
        (df) df - dataframe containing data to display
    Returns:
        nothing
    """
    rowfrom = 0
    numlines = 10
    rowto = rowfrom + numlines

    #print slice: nominated rows, all columns of dataframe
    print(df.iloc[rowfrom:rowto,:])

    #get the number of rows in the dataframe
    numrows = len(df.index)

    while rowfrom < numrows: #True:
        try:
            # DISPLAY numlines LINES OF DATA UNTIL USER INDICATES THEY WANT TO STOP
            #increase the slice definition
            rowfrom += numlines
            rowto += numlines

            restart = input('\nWould you like to like to see rows {} to {} ({} total rows)? Enter yes to continue or no to view summary statistics.\n'.format(rowfrom,rowto,numrows))

            if restart.lower()=='yes':
                #print(df.iloc[rowfrom:rowto,:])
	print(tabulate(df.iloc[np.arange(rowfrom,rowto)], headers ="keys"))
            elif restart.lower() == 'no':
                raise UserAborted
            else:
                raise UserInvalidEntry('Enter yes or no')

        except UserInvalidEntry as e:
            print("Invalid entry: {}".format(e))
        except UserAborted:
            #raise the error to calling procedure
            break
        except Exception:
            print("Exception occurred: {}".format(e))

def most_frequent(List): 
    return max(set(List), key = List.count) 

def time_stats(df,month,day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (df)  df    - dataframe containing data to display
        (str) month - month to display (numeric 1-12 or 'all')
        (str) day   - day to display (numeric 1-31 or 'all')
    
    Returns:
        nothing
    """

    print('\nCalculating The Most Frequent Times of Travel for {} - {}...\n'.format(MONTH.get(month),WEEKDAY.get(day)))

    # IF THE USER REQUESTES ALL MONTHS, DISPLAY THE MOST COMMON MONTH
    if month == 'all':
        # convert pandas data series to list and get the most frequent item from it
        print('The most frequent month is {}'.format(MONTH.get(most_frequent(df['start_month'].tolist()))))

    # IF THE USER REQUESTED ALL DAYS DISPLAY THE MOST COMMON DAY OF THE WEEK
    if day == 'all':
        # convert pandas data series to list
        print('The most frequent day is {}'.format(WEEKDAY.get(most_frequent(df['start_day'].tolist()))))

    # DISPLAY THE MOST COMMON START HOUR
    # add hour to the dataframe
    df['start_hour']= pd.DatetimeIndex(df['Start_Time']).hour
    print('The most common start hour is {}:00'.format(most_frequent(df['start_hour'].tolist())))

    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        (df)  df    - dataframe containing data to display
    
    Returns:
        nothing    
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')

    # DISPLAY MOST COMMONLY USED START STATION
    #make the dataframe index Start_Station
    df.set_index('Start_Station')
 
    #use valuecounts to get count of distinct values, ordered descending (default)
    x = df['Start_Station'].value_counts().index[0]
    print('The most common start station is {}'.format(x))

    # DISPLAY MOST COMMONLY USED END STATION
    df.set_index('End_Station')
    print('The most common end station is {}'.format(df['End_Station'].value_counts().index[0]))

    # display most frequent combination of start station and end station trip 
    df['station_combination']=df['Start_Station']+' to ' + df['End_Station']
    df.set_index('station_combination')
    print('The most common common start/end station combination is {}'.format(df['station_combination'].value_counts().index[0]))

    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Uses datetime.timedelta which requires a float64
    
    Args:
        (df)  df    - dataframe containing data to display
    
    Returns:
        nothing
    """

    print('\nCalculating Trip Duration...\n')
    
    #convert Trip Duration to float
    df['Trip_Duration'] = df['Trip_Duration'].astype('float')

    #clear Trip Duration of any NaN entries
    df = df[df['Trip_Duration'].notna()]
     
    # display mean & total travel time
    total = str(datetime.timedelta(seconds=round(df['Trip_Duration'].sum())))
    mean = str(datetime.timedelta(seconds=round(df['Trip_Duration'].mean())))

    print("Trip Duration ([dy], h:m:s) - SUM: {} MEAN: {}".format(total,mean))

    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (df)  df    - dataframe containing data to display
    
    Returns:
        nothing
    """

    print('\nCalculating User Stats...')

    # Display counts of user types
    if 'User_Type' in df:
        print('\nCount by User Type:')
        print(df.groupby(['User_Type'])['start_month'].count())
    else:
        print('\nUser type stats are unavailable')

    # Display counts of gender
    if 'Gender' in df:
        print('\nCount by Gender:')
        print(df.groupby(['Gender'])['start_month'].count())
    else:
        print('\nGender stats are unavailable')

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        #drop na columns
        df = df[df['Birth_Year'].notna()]
        print('\nBirth Year stats:')
        print('The minimum birth year is {}'.format(df['Birth_Year'].min()))
        print('The maximum birth year is {}'.format(df['Birth_Year'].max()))
        print('The most common birth year is {}'.format(most_frequent(df['Birth_Year'].tolist())))
    else:
        print('\nBirth year stats are unavailable')

    print('-'*40)


def main():
    while True:
        #find out what the user wants to see
        city, month, day = get_filters()
        
        #if city, month and day are all populated
        if all([city,month,day]):
            
            print("\nExtracting data for: {} - month: {}, day: {}".format(city.title(),MONTH.get(month),WEEKDAY.get(day)))

            #load and filter the data
            df = load_data(city.lower(), month.lower(), day.lower())

            if df.empty:
                print("No data returned for: {} - month: {}, days: {}".format(city.title(),MONTH.get(month),WEEKDAY.get(day)))
            else:
                if input('\nWould you like to see the raw data? Enter yes or y to continue, any other key to skip\n').lower() in('yes','y'):
                    view_raw_data(df)

                #start the clock for retriving stats collection time.
                start_time = time.time()

                time_stats(df,month,day)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)

                #print out how long it took to get the stats
                print("\nThis took %s seconds." % round((time.time() - start_time),3))

        restart = input('\nWould you like to restart? Enter yes or y to continue, any other key to skip.\n')
        if restart.lower() not in('yes','y'):
            break


if __name__ == "__main__":
	main()
