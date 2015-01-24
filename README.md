## Strava Club Year to date Stats.

This set of Python scripts will retrieve the year to date totals (distance and elevation gain) from the public profile page for all the athletes on a club or list.

#####Pros:
  * Simple, the scripts just interprets HTML.
  * Uses publicly available information.
  * Does not require special credentials to get the information.

#####Cons:
  * High risk of breaking, strava may change the HTML and break the script.
  * Not perfect. Some athletes prefer not to have cycling Year to date totals made public.

## Scripts
 1. get_ytd_club_stats.py: the "I'm feeling lucky" script. Calls the next two scripts in sequence.
 2. extract_group_members.py: Given a HTML File from Strava Club page saved by the club owner, extract all the athlete names and IDs.
 3. get_stats.py: Given a list of IDs/athletes, get the Year to Date stats.

##Install
The script has been tested using Python2.7 and beautifulsoup4. You can use pip to install beautifulsoup4:

    pip install -r requirements.txt

##Generating Year To Date stats
The script uses publicly available information in strava to get the Year to Date stats. If an specific user has his profile default set to "running" or is a Strava pro, then this script won't work for that specific user.

The script does two steps:
 1. Generate a list of Athletes/users using the Strava Club Page.
 2. For each user get the Public profile and extract the Year to date information.

The list of athletes can be generated from a club or created manually.
 1. Generation from a club: The owner of the club must log in to strava, visit the club web site and save the web site as HTML.
 2. Manual list: Create a CSV file with "ID,Athlete Name" for each athlete.

### Generating ytd stats: "I'm feeling lucky"
First step is saving the club website, this must be done by the club owner. Then run the following line from the command line:

    python get_ytd_club_stats.py --html club_website_saved_by_club_owner.html --out ytd_stats.csv

### Generating ytd stats: "I'll do it myself"
If you want to change the list of athletes the script gets the Year to Date information, then you'll need to do some extra steps.

First, lets generate the list/csv of athletes to get the year to date information. This can be done manually or by running the script:

    python python extract_group_members.py --html club_website_saved_by_club_owner.html --out list_of_athletes.csv

Now you can modify the file list_of_athletes and either add or remove them.

Next run the second script:

    python get_stats.py --members list_of_athletes.csv --out ytd_stats.csv

There are some athletes public profile that don't have the cycling year to date information. The information for these athletes can be extracted manually when logged into strava.

### Examples
Run the script:
    python get_ytd_club_stats.py --html examples/club_example.html --out ytd_stats.csv
or:
    python python extract_group_members.py --html examples/club_example.html --out list_of_athletes.csv
    python get_stats.py --members list_of_athletes.csv --out ytd_stats.csv
