'''
Given a list of strava athletes print get the year to date cycling information
in metric units.
'''

import urllib2
from bs4 import BeautifulSoup
import csv
import argparse

class Athlete_public_html ():
    ''' Class that holds all the public "HTML" information for a given athlete
    '''
    def __init__(self, ID):
        self.id = ID
        self.url = 'http://www.strava.com/athletes/' + self.id
        self.html = urllib2.urlopen(self.url)
        self.soup = BeautifulSoup(self.html)
        try:
            self.year_stats = self.__get_year_stats_from_html()
        except:
            self.year_stats = {'distance' : 'error - Get data Manually'}
            print "Non standard public page. needs manual update"

    def __get_year_stats_from_html(self):
        records_table = self.soup.find('section', attrs={'class':'row athlete-records'})
        year_section = records_table.find('div')
        header = year_section.find('h2')

        # Validate that we have the 'Year-to-Date' section of the table.
        if header.get_text() != 'Year-to-Date':
            print "Didn't find year to date table. HTML must have change and script needs to be updated"
            return {}

        htmltable = year_section.find('table')

        thead = htmltable.find('thead')
        head_text = thead.get_text().strip()
        # Validate that we have the Cycling table
        if head_text != 'Cycling':
            print "No cycling information, must be a runner."
            return {'distance' : 'error - Get data Manually'}

        tbody =  htmltable.find('tbody')
        rows = tbody.find_all('tr')

        ret_dict = {}
        for row in rows:

            #get the Field name and store as Key
            field_name = row.find('th')
            key = field_name.get_text()

            #Get the value
            col = row.find('td')
            td_data = col.get_text()

            #Convert the table names to standard Key names (in case strava changes the names)
            if key == 'Distance':
                key = 'distance'
                units = td_data[-2:]
                if units == 'mi':
                    km = float(td_data[:-2].replace(',',''))*1.609
                elif units == 'km':
                    km = float(td_data[:-2].replace(',',''))
                else:
                    km = 'bad_unit'

                ret_dict[key] = km
            elif key == 'Time':
                key = 'time'
                ret_dict[key] = td_data
            elif key == 'Elevation Gain':
                key = 'elevation gain'
                units = td_data[-2:]
                if units == 'ft':
                    m = float(td_data[:-2].replace(',',''))*0.3048
                else:
                    units = td_data[-1:]
                    if units == 'm':
                        m = float(td_data[:-1].replace(',',''))
                    else:
                        m = 'bad_unit'
                ret_dict[key] = m
            elif key == 'Rides':
                key = 'rides'
                ret_dict[key] = td_data
            else:
                ret_dict[key] = td_data

        return ret_dict

    def get_name (self):
        title = self.soup.title.string
        title_name = title.split('|')
        return title_name[0]

    def get_id (self):
        return self.ID

    def get_year_distance(self):
        if 'distance' in self.year_stats:
            distance = self.year_stats['distance']
        else:
            distance = ''
        return distance

    def get_year_time(self):
        if 'time' in self.year_stats:
            time = self.year_stats['time']
        else:
            time = ''

        return time

    def get_year_elevation_gain(self):
        if 'elevation gain' in self.year_stats:
            elevation = self.year_stats['elevation gain']
        else:
            elevation = ''
        return elevation

    def get_year_rides(self):
        return self.year_stats['rides']

def get_athlete_list_from_file (user_list_csv):
    athletes = []
    with open(user_list_csv, 'rb') as fin:

        csvin = csv.reader(fin)

        for member in csvin:
            athletes.append([member[0], member[1]])
    return athletes

def save_members_ytd_stats (user_list, out_file):
    with open (out_file, 'wb') as fout:

        csvout = csv.writer(fout)
        csvout.writerow(['ID', 'Name', 'Distance(Km)', 'Elevation Gain(m)'])
        for member in user_list:
            athlete = Athlete_public_html(str(member[0]))
            dist = athlete.get_year_distance()
            elev = athlete.get_year_elevation_gain()
            print member[1] + "," + str(dist) + "," + str(elev)

            csvout.writerow([member[0], member[1], dist, elev])

def save_members_from_file_ytd_stats (user_list_csv, out_file):
    with open (out_file, 'wb') as fout, open(user_list, 'rb') as fin:

        csvin = csv.reader(fin)

        csvout = csv.writer(fout)
        csvout.writerow(['id', 'Name', 'Distance', 'Elevation Gain'])
        for member in csvin:

            athlete = Athlete_public_html(str(member[0]))
            dist = athlete.get_year_distance()
            elev = athlete.get_year_elevation_gain()
            print member[1] + "," + str(dist) + "," + str(elev)

            csvout.writerow([member[0], member[1], dist, elev])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the year to date totals for a list of users in strava.')
    parser.add_argument('-m', '--members', dest='user_list', required=True,
                        help='CSV File containing a list of users. The data should be ordered as Account_Number, "Athlete Name". This program will try to get the yearly stats for this list of users.')
    parser.add_argument('-o', '--out', dest='out_file',
                        default='year_to_date_club_stats.csv',
                        help='Output CSV file name, default value is year_to_date_club_stats.csv. The output has all units converted to metric.')
    args = parser.parse_args()

    user_list_file = args.user_list
    out_file = args.out_file

    athletes = get_athlete_list_from_file (user_list_file)

    save_members_ytd_stats (athletes, out_file)
