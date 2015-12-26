'''
Strava club information is not publicly available. To get the club information
 the club owner needs to be logged in. This script takes the HTML file of the
 strava club page and extracts all the users/athletes.
'''

from bs4 import BeautifulSoup
import argparse

def get_group_members_from_html(html_in):
    with open(html_in, 'rb') as fin:
        soup = BeautifulSoup(fin)
        scripts = soup.find_all('script')
        for jscript in scripts:
            text = jscript.get_text()
            if 'members:' in text:
                junk, tail = text.split('members:')
                last_char = tail.find(']]')
                first_char = tail.find('[[')
                member_list = tail[first_char:last_char+2]

                mem_array = eval(member_list)

                return mem_array
    return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the year to date totals for a list of users in strava.')
    parser.add_argument('--html', dest='html_file', required=True,
                        help='A saved copy of the group strava page when logged in.')
    parser.add_argument('-o', '--out', dest='out_file',
                        default='club_members.csv',
                        help='Output CSV file name, default value is club_members.csv')
    args = parser.parse_args()

    html_file = args.html_file
    out_file = args.out_file

    with open (out_file, 'wb') as fout:
        members = get_group_members_from_html(html_file)
        for member in members:
            line = unicode(str(member[0])) + u',' + member[1].decode('unicode_escape') + u'\n'
            fout.write(line.encode('utf8'))

    with open (out_file, 'r') as f:
        for line in f:
            print line.strip()
