import csv
import datetime
import json
import os

import pandas as pd
import requests

os.makedirs('data', exist_ok=True)


def getWeeklyData():
    apirURL = 'https://services.arcgis.com/g1fRTDLeMgspWrYp/arcgis/rest/services/Weekly_Bexar_County_CoVID19_Surveillance_Data_Public/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

    r = requests.get(apirURL)
    weeklyData = json.loads(r.text)['features']
    return weeklyData


def getWeeklyLabData():
    apirURL = 'https://services.arcgis.com/g1fRTDLeMgspWrYp/arcgis/rest/services/vCOVID19_WeeklyLabTesting_Public/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

    r = requests.get(apirURL)
    weeklyLabData = json.loads(r.text)['features']
    return weeklyLabData


def getDailyData():
    apirURL = 'https://services.arcgis.com/g1fRTDLeMgspWrYp/arcgis/rest/services/SAMHD_DailySurveillance_Data_Public/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

    r = requests.get(apirURL)
    dailyData = json.loads(r.text)['features']
    return dailyData


dailyData = getDailyData()
weeklyData = getWeeklyData()
weeklyLabData = getWeeklyLabData()

# DAILY GRAPHICS

def getTwoWeekChange(data):
    currentDataIndex = len(data) - 1
    twoWeeksAgoIndex = currentDataIndex - 14
    currentCaseAverage = data[currentDataIndex]['attributes']['count_7_day_moving_avg']
    twoWeeksAgoCaseAverage = data[twoWeeksAgoIndex]['attributes']['count_7_day_moving_avg']
    twoWeeksChange = round((currentCaseAverage - twoWeeksAgoCaseAverage) / twoWeeksAgoCaseAverage * 100, 1)

    if (twoWeeksChange > 0):
        upDown = 'up'
        color = 'red'
    else:
        upDown = 'down'
        color = 'green'

    s = '<div><p>The 7-day rolling average of new COVID-19 cases in San Antonio has gone <span style = "color: {}">{} by {}%</span> over the last two weeks.</p></div>'.format(color, upDown,twoWeeksChange)

    with open('data/twoWeeksChange.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([s])

def getLast90Days(data):
    '''
    TK TK TK
    '''
    dateColumn = []
    newCaseList = []
    startRow = len(data) - 90
    for i in range(startRow, len(data)):
        datetime_time = datetime.datetime.fromtimestamp(data[i]['attributes']['reporting_date'] / 1000).strftime("%Y-%m-%d")
        print(datetime_time)
        dateColumn.append(datetime_time)
        newCaseList.append(data[i]['attributes']['count_7_day_moving_avg'])
    
    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Cases'] = newCaseList

    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    df.to_csv('data/last90Days.csv', index=False)

def getSevenDayNewCases(data):
    '''
    Chart title: New confirmed and probable COVID-19 cases in Bexar County, daily count and 7-day rolling average

    DW link: https://app.datawrapper.de/chart/cBNh5/publish

    WCM Link: https://wcm.hearstnp.com/index.php?_wcmAction=business/item&id=96075
    '''

    dateColumn = []
    newCaseList = []
    baselineList = []
    rollingAverage = []

    for i in range(len(data)):
        if data[i]['attributes']['count_7_day_moving_avg'] == None:
            pass
        elif data[i]['attributes']['reporting_date'] == 1594875600000:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            newCaseList.append(691)
            baselineList.append(0)
            rollingAverage.append(479)
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            newCaseList.append(data[i]['attributes']
                               ['total_case_daily_change'])
            rollingAverage.append(data[i]['attributes']
                                  ['count_7_day_moving_avg'])
            baselineList.append(0)

    # Pandas work
    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Cases'] = newCaseList
    df['Seven Day Rolling Average'] = rollingAverage
    df['Baseline'] = baselineList

    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    # print(df)
    df.to_csv('data/seven_day_case_line_bar.csv', index=False)


def getUpdateTable(data):
    '''
    Chart title: CORONAVIRUS IN BEXAR COUNTY [It's blank on DW]

    DW link: https://app.datawrapper.de/table/MXNZd/publish

    WCM: https://wcm.hearstnp.com/index.php?_wcmAction=business/item&id=96125
    '''
    dateColumn = []
    newCaseNumbers = []
    newDeathNumbers = []
    caseCumList = []
    deathCumList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['total_case_daily_change'] == None:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            # print(str(datetime_time) + " | " +
            #       str(data[i]['attributes']['reporting_date']))
            dateColumn.append(datetime_time)
            caseCumList.append(data[i]['attributes']['total_case_cumulative'])
            deathCumList.append(data[i]['attributes']['deaths_cumulative'])
            newCaseNumbers.append(
                data[i]['attributes']['total_case_daily_change'])
            newDeathNumbers.append(
                data[i]['attributes']['deaths_daily_change'])

    latestNums = [newCaseNumbers[-1], newDeathNumbers[-1]]
    totalNums = [caseCumList[-1], deathCumList[-1]]

    # Sorting
    df2 = pd.DataFrame()
    df2['Date'] = dateColumn
    df2['New Cases'] = newCaseNumbers
    df2['New Deaths'] = newDeathNumbers
    df2['Cumulative cases'] = caseCumList
    df2['Cumulative deaths'] = deathCumList
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2 = df2.sort_values(by='Date')
    newCases = df2['New Cases'].iloc[-1]
    cumCases = df2['Cumulative cases'].iloc[-1]
    newDeaths = df2['New Deaths'].iloc[-1]
    cumDeaths = df2['Cumulative deaths'].iloc[-1]
    cases = ['+' + f'{newCases:,}', f'{cumCases:,}']
    deaths = ['+' + f'{int(newDeaths):,}', f'{cumDeaths:,}']

    df3 = pd.DataFrame()
    df3['‎'] = ['New', 'All time']
    df3['Cases'] = cases
    df3['Deaths'] = deaths
    df3.to_csv('data/covid_update_table.csv', index=False)


def getSevenDayNewDeaths(data):
    '''
    Chart title: COVID-19 deaths in Bexar County, daily count and 7-day rolling average

    DW link: https://app.datawrapper.de/chart/y1v4d/publish

    WCM id: https://wcm.hearstnp.com/?_wcmAction=business/item&id=96074
    '''
    dateColumn = []
    deathsCumList = []
    baselineList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['deaths_daily_change'] == None:
            pass
        elif data[i]['attributes']['reporting_date'] == 1608789600000:
            pass
        elif data[i]['attributes']['reporting_date'] == 1608876000000:
            pass
        elif data[i]['attributes']['reporting_date'] == 1609005600000:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            deathsCumList.append(data[i]['attributes']['deaths_daily_change'])
            baselineList.append(0)

    # Pandas work
    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Deaths'] = deathsCumList
    # Thursday, June 30, 2022: Metro health entered the data incorrectly. The death change was 1.
    df.at[df.index[df['Date'] == '2022-06-24'].to_list()[0], 'Deaths'] = 1
    df['7-day rolling average'] = df['Deaths'].rolling(7).mean().round(1)
    df['Baseline'] = baselineList
    df = df.dropna(subset=['7-day rolling average'])
    # Sort by date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    df.to_csv('data/seven_day_deaths_line_bar.csv', index=False)


def getCumConfirmedCases(data):
    '''
    Chart title: Confirmed and probable COVID-19 cases in San Antonio

    DW link: https://app.datawrapper.de/chart/6yc5D/publish

    WCM id: https://wcm.hearstnp.com/?_wcmAction=business/item&id=96319
    '''

    dateColumn = []
    casesCumList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['total_case_daily_change'] == None:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            casesCumList.append(data[i]['attributes']['total_case_cumulative'])

    # Pandas work
    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Confirmed and probable'] = casesCumList

    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # print(df)
    df.to_csv('data/cumulative_confirmed_cases.csv', index=False)


def getCumDeaths(data):
    '''
    Chart title: Cumulative number of deaths caused by COVID-19 in Bexar County

    DW link: https://app.datawrapper.de/chart/vfSa2/publish

    WCM id: https://wcm.hearstnp.com/?_wcmAction=business/item&id=95837
    '''
    dateColumn = []
    deathsCumList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        # elif data[i]['attributes']['total_case_daily_change'] == None:
        #     pass
        elif data[i]['attributes']['deaths_cumulative'] == 0:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            deathsCumList.append(data[i]['attributes']['deaths_cumulative'])

    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Deaths'] = deathsCumList
    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    df.to_csv('data/cumulative_deaths.csv', index=False)

# WEEKLY GRAPHICS


def GetActiveCaseMap():
    df = pd.read_csv(
        'https://cosacovid-cosagis.hub.arcgis.com/datasets/a39a0abe9bb246d0b2fe3334616e5bc3_0.csv?outSR=%7B%22latestWkid%22%3A2278%2C%22wkid%22%3A102740%7D')
    del df['OBJECTID']
    activeCaseRatePer1k = []
    for i in range(len(df)):
        # print(df['ZIP_CODE'][i])
        totalActiveCases = df['ActiveCases']
        zipPop = df['TotPop2020']
        rate = (totalActiveCases / zipPop) * 1000
        activeCaseRatePer1k.append(rate[i])
    df['active cases per 1k'] = activeCaseRatePer1k
    df.to_csv('data/active_case_map.csv', index=False)


def getWeeklyPositivity(data):
    '''
    Chart title: Weekly positive test rate for Bexar County

    DW link: https://app.datawrapper.de/chart/tAc4D/publish

    WCM: https://wcm.hearstnp.com/index.php?_wcmAction=business/item&id=96347
    '''
    dateColumn = []
    weeklyRate = []

    for i in range(len(data)):
        timeDate = data[i]['attributes']['enter_web_posting_date'] / 1000
        datetime_time = datetime.datetime.fromtimestamp(
            timeDate).strftime("%Y-%m-%d")
        dateColumn.append(datetime_time)
        weeklyRate.append(data[i]['attributes']
                          ['percent_weekly_bexar_county_pos'])

    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Weekly positivity rate'] = weeklyRate

    # print(df)
    df.to_csv('data/weekly_positivity_line.csv', index=False)


def getWeeklyCaseChange(data):
    '''
    Chart title: New confirmed and probable COVID-19 cases in Bexar County each week

    DW link: https://app.datawrapper.de/chart/1UYvz/visualize#refine

    WCM Link: https://wcm.hearstnp.com/index.php?_wcmAction=business/item&id=98631

    '''

    dateColumn = []
    newCaseList = []
    baselineList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['case_count_weekly_change'] == None:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            newCaseList.append(data[i]['attributes']
                               ['case_count_weekly_change'])
            baselineList.append(0)

    # # Pandas work
    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Total new cases'] = newCaseList

    # print(df)
    df.to_csv('data/weekly_new_cases.csv', index=False)


def getCumDeaths(data):
    '''
    Chart title: Cumulative number of deaths caused by COVID-19 in Bexar County

    DW link: https://app.datawrapper.de/chart/vfSa2/publish

    WCM id: https://wcm.hearstnp.com/?_wcmAction=business/item&id=95837
    '''
    dateColumn = []
    deathsCumList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['deaths_cumulative'] == 0:
            pass
        elif data[i]['attributes']['deaths_cumulative'] == None:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            deathsCumList.append(data[i]['attributes']
                                 ['deaths_cumulative'])

    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Cumulative Deaths'] = deathsCumList

    # Thursday, June 30, 2022: Metro health entered the data incorrectly. The cumulative death count was 
    df.at[df.index[df['Date'] == '2022-06-24'].to_list()[0], 'Cumulative Deaths'] = 5338

    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # print(df)
    df.to_csv('data/cumulative_deaths.csv', index=False)


def getPatientStatus(data):
    '''
    Chart title: COVID-19 patients in Bexar County hospitals by day

    DW link: https://app.datawrapper.de/chart/zlJXV/publish

    WCM: https://wcm.hearstnp.com/index.php?_wcmAction=business/item&id=96060
    '''
    dateColumn = []
    PosPatientsList = []
    CovidIcuList = []
    CovidonVentList = []

    for i in range(len(data)):
        if data[i]['attributes']['reporting_date'] == None:
            pass
        elif data[i]['attributes']['total_case_daily_change'] == None:
            pass
        else:
            timeDate = data[i]['attributes']['reporting_date'] / 1000
            datetime_time = datetime.datetime.fromtimestamp(
                timeDate).strftime("%Y-%m-%d")
            dateColumn.append(datetime_time)
            CovidIcuList.append(data[i]['attributes']
                                ['strac_covid_positive_in_icu'])
            PosPatientsList.append(
                data[i]['attributes']['strac_covid_positive_in_hospita'])
            CovidonVentList.append(
                data[i]['attributes']['strac_covid_positive_on_ventila'])

    df = pd.DataFrame()
    df['Date'] = dateColumn
    df['Total number of patients'] = PosPatientsList
    df['Patients in ICU'] = CovidIcuList
    df['Patients on ventilators'] = CovidonVentList
    df = df.dropna(subset=['Patients on ventilators'])

    # Sort the DF by the date.
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')

    # print(df)
    df.to_csv('data/patient_status.csv', index=False)

def getTexasCountyData():
    df = pd.read_excel('https://dshs.texas.gov/coronavirus/COVID19NewConfirmedCasesbyCounty.xlsx', sheet_name='Cases by County 2022', skiprows=2)
    df = df.iloc[:,list([0] + [-1])]
    df.columns = ['County', 'Cases']
    df.to_csv('data/texas_county_data.csv', index=False)

def createMetadata():
    print('Creating metadata...')
    # Save current date to variable in this format: Aug. 4, 2022
    date = datetime.datetime.now().strftime("%b. %-d, %Y")
    s = f'Data as of {date}'
    data = {}
    
    # Create nested dictionary with metadata
    data['annotate'] = {'notes': s}

    json_data = json.dumps(data)
    with open('data/metadata.json', 'w') as f:
        f.write(json_data)

# July 13, 2021 Functions
getWeeklyPositivity(weeklyLabData)
getWeeklyCaseChange(weeklyData)
# GetActiveCaseMap()

# DAILY GRAPHICS
getTwoWeekChange(dailyData)
getLast90Days(dailyData)
getSevenDayNewCases(dailyData)
getCumConfirmedCases(dailyData)
getUpdateTable(dailyData)
getSevenDayNewDeaths(dailyData)
getPatientStatus(dailyData)
getCumDeaths(dailyData)

# State data
getTexasCountyData()

createMetadata()
