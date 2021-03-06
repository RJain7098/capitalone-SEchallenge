from app import app
import iso8601
import datetime

# I noticed that the headline had "- [nameOfSite]" added onto it, and I didn't like that
# cluttering the title, so I wrote this function to remove it. It works for most major
# sites, but some foreign/les mainstream sources are formatted weirdly in the data that
# the API returns, so it's difficult to catch every case.
@app.context_processor
def delete_extra():
    def _delete_extra(title, source):
        index = title.lower().find(source.partition(".")[0].lower())
        return title[0:index-2]
    return dict(delete_extra=_delete_extra)

# This is some rudimenteray paywall "detetection". Rather than web scraping to find this,
# I simply gathered a list of sites that have some sort of paywall. It's not comprehensive,
# but it does help the user at least identify the most obvious ones.
# Note that the NewsAPI tends not to return many results from popular sites, and I'm 
# not quite sure why - likely a configuration based on the category and top-hadlines endpoint.
# So you likely won't see the "paywall warning" very often. 
@app.context_processor
def find_paywall():
    def _find_paywall(url):
        sites = ["thetimes.co.uk", "thesundaytimes.co.uk", "wsj.com", "newsweek.com", "kyivpost.com", "ft.com", 
                "latimes.com", "nytimes.com", "washingtonpost.com", "theglobeandmail.com", "nationalpost.com", 
                "smh.com.au", "theage.com.au", "bostonglobe.com", "theaustralian.com.au", "bloomberg.com"]
        temp_index = url.rfind("/", 0, 8)
        if url[temp_index:].find("www") != -1:
            begin_index = temp_index + 5
        else:
            begin_index = temp_index + 1
        end_index = url.find("/", begin_index)
        if url[begin_index:end_index] in sites:
            return "True"
        else:
            return "False"
    return dict(find_paywall=_find_paywall)

# The date from the API is returned in standard ISO 8601 format, so I used
# a python library to process it into an easier to read format for the user. 
@app.context_processor
def process_date():
    def _process_date(date):
        months = ["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        parsed = iso8601.parse_date(date)
        return months[parsed.month-1] + " " + str(parsed.day) + ", " + str(parsed.year)
    return dict(process_date=_process_date)
