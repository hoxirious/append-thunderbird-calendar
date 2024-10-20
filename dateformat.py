# dd-mm-yyyy or dd/mm/yyyy
ddmmyyyy_date_pattern = r'((0[1-9]|[12][0-9]|3[01])(\/|-)(0[1-9]|1[0-2])(\/|-)((19|20)\d{2}))'

# yyyy-mm-dd or yyyy/mm/dd
yyyymmdd_date_pattern = r'(((19|20)\d{2})(\/|-)(0[1-9]|1[0-2])(\/|-)(0[1-9]|[12][0-9]|3[01]))'

# mm-dd-yyyy or mm/dd/yyyy
mmddyyyy_date_pattern = r'((0[1-9]|1[0-2])(\/|-)(0[1-9]|[12][0-9]|3[01])(\/|-)((19|20)\d{2}))'

# Month Day, Year (e.g., January 01, 2023)
monthdyr_date_pattern = r'((January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)\s(0[1-9]|[12][0-9]|30|31),\s((19|20)\d{2}))'

# Day Month, Year (e.g., 01 January, 2023)
dmonthyr_date_pattern = r'((0[1-9]|[12][0-9]|30|31)\s(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec),\s((19|20)\d{2}))'

# Year, Month Day (e.g., 2023, January 01)
yrmonthd_date_pattern = r'(((19|20)\d{2}),\s(January|Jan|February|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)\s(0[1-9]|[12][0-9]|30|31))'

month_pattern = r'(January|Jan|Febuary|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)'
date_pattern = r'(3?1st|2?2nd|2?3rd|((1|2)?[0-9]|30)th)'
day_pattern = r'([tT]his\s|[nN]ext\s)?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
