import json,os,pandas
from datetime import date, timedelta
from os import path
import texttable as tt


confirmed_dict = {}
recovered_dict = {}
deceased_dict = {}

confirmed_delta_dict = {}
recovered_delta_dict = {}

#7 days back data:
start_date = date.today() - timedelta(days=7)
delta = date.today() - start_date


def getData(jsonfile,yestjsonfile):
    curl_command = 'curl -L -s https://api.covid19india.org/v4/data-all.json >'
    overall_command = curl_command + jsonfile + '\n'

    if path.exists(jsonfile) == False:
        print("File doesnt exist!!")
        os.system(overall_command)
        if path.exists(yestjsonfile) == True:
            rm_command = 'rm -rf ' + yestjsonfile
            os.system(rm_command)
    else:
        print("File exists!")


def extractData(df,state,district):
    for i in range(1,delta.days ,1):
        day = start_date + timedelta(days=i)
        date_format=str(day.year)+"-"+str(day.month)+"-"+str(day.day)
        day = date_format

        confirmed_dict[date_format] = df[day][state]['districts'][district]['total']['confirmed']

        if 'recovered' in df[day][state]['districts'][district]['total']:
            recovered_dict[date_format] = df[day][state]['districts'][district]['total']['recovered']
        else:
            recovered_dict[date_format] = 0

        if 'deceased' in df[day][state]['districts'][district]['total']:
            deceased_dict[date_format] = df[day][state]['districts'][district]['total']['deceased']
        else:
            deceased_dict[date_format] = 0

        if 'delta' in df[day][state]['districts'][district]:
            if 'confirmed' in df[day][state]['districts'][district]['delta']:
                confirmed_delta_dict[date_format] = df[day][state]['districts'][district]['delta']['confirmed']
            else:
                confirmed_delta_dict[date_format] = 0
        else:
            confirmed_delta_dict[date_format] = 0

        if 'delta' in df[day][state]['districts'][district]:
            if 'recovered' in df[day][state]['districts'][district]['delta']:
                recovered_delta_dict[date_format] = df[day][state]['districts'][district]['delta']['recovered']
            else:
                recovered_delta_dict[date_format] = 0
        else:
            recovered_delta_dict[date_format] = 0

def drawTable(state,district):
    ParentTable = tt.Texttable()
    ParentTable.set_cols_width([15,10,20,20])
    ParentTable.set_cols_align(['c','c','c','c'])
    ParentTable.set_cols_valign(['m','m','m','m'])
    Parentheader = ['District','Date','Confirmed Cases','Recovered Cases']
    ParentTable.header(Parentheader)
    for i in range(1,delta.days ,1):
        day = start_date + timedelta(days=i)
        date_format=str(day.year)+"-"+str(day.month)+"-"+str(day.day)
        day = date_format
        Parentrow = [district, day,confirmed_delta_dict[date_format],recovered_delta_dict[date_format]]
        ParentTable.add_row(Parentrow)
    MainParentTable = ParentTable.draw()
    print(MainParentTable)


def main():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    jsonfile = today.strftime("%d-%m-%Y") + '.json'
    yestjsonfile = yesterday.strftime("%d-%m-%Y") + '.json'

    getData(jsonfile,yestjsonfile)
    df=pandas.read_json(jsonfile)

    print(list(df['28-07-2020'].keys()))
    state = input("Enter State : ")
    print(list(df['28-07-2020'][state]['districts'].keys()))
    district = input("Enter District: ")

    extractData(df,state,district)
    drawTable(state,district)

if __name__ == "__main__":
    main()
