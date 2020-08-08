import json,os,pandas
from datetime import date, timedelta
from os import path
import texttable as tt


def getData(jsonfile,yestjsonfile):
    curl_command = 'curl -L -s https://api.covid19india.org/v4/data-all.json >'
    overall_command = curl_command + jsonfile + '\n'

    if path.exists(jsonfile) == False:
        #print("File doesnt exist!!")
        os.system(overall_command)
        if path.exists(yestjsonfile) == True:
            rm_command = 'rm -rf ' + yestjsonfile
            os.system(rm_command)


def extractData(df,today):
    date_format=str(today.year)+"-"+str(today.month)+"-"+str(today.day)
    day = date_format

    state_list = list(df[day].keys())

    ParentTable = tt.Texttable()
    ParentTable.set_cols_width([15,15,15,15,15,15])
    ParentTable.set_cols_align(['c','c','c','c','c','c'])
    ParentTable.set_cols_valign(['m','m','m','m','m','m'])
    Parentheader = ['State','Confirmed','Recovered','Active','Deceased','Tested']
    ParentTable.header(Parentheader)

    for state in state_list:
        if state != 'UN':
            confirmed = df[day][state]['total']['confirmed']
            recovered = df[day][state]['total']['recovered']
            active = df[day][state]['total']['confirmed'] - df[day][state]['total']['recovered']
            if 'deceased' in df[day][state]['total']:
                death = df[day][state]['total']['deceased']
            else:
                death = 0
            tested = df[day][state]['total']['tested']

            Parentrow = [state,confirmed,recovered,active,death,tested]
            ParentTable.add_row(Parentrow)

    MainParentTable = ParentTable.draw()
    print(MainParentTable)



def main():
    today = date.today()
    yesterday = date.today() - timedelta(days=1)

    jsonfile = date.today().strftime("%d-%m-%Y") + '.json'
    yestjsonfile = yesterday.strftime("%d-%m-%Y") + '.json'

    getData(jsonfile,yestjsonfile)
    df=pandas.read_json(jsonfile)

    extractData(df,today)

if __name__ == "__main__":
    main()
