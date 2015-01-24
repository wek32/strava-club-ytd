'''
This scripts combines the extract_grou_members and get_stats scripts into one
easy to execute instance.
'''

import argparse
from extract_group_members import get_group_members_from_html
from get_stats import save_members_ytd_stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the year to date totals for all the athletes of a Strava club.')
    parser.add_argument('--html', dest='html_file', required=True,
                        help='A saved copy of the group strava page when logged in as the club owner.')
    parser.add_argument('-o', '--out', dest='out_file',
                        default='year_to_date_club_stats.csv',
                        help='Output CSV file name, default value year_to_date_club_stats.csv. The output has all units converted to metric.')
    args = parser.parse_args()

    html_file = args.html_file
    out_file = args.out_file

    club_members = get_group_members_from_html(html_file)
    save_members_ytd_stats(club_members, out_file)
