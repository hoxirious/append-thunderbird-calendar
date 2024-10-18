ddmmyyyy_date_pattern = r'((0[1-9]|[1-9]|[12][0-9]|(30|31))(\/|-)(0[1-9]|[1-9]|1[0-2])(\/|-)((19|20)\d{2}))'
yyyymmdd_date_pattern = r'(((19|20)\d{2})(\/|-)(0[1-9]|[1-9]|1[0-2])(\/|-)(0[1-9]|[1-9]|[12][0-9]|(30|31)))'
mmddyyyy_date_pattern = r'((0[1-9]|[1-9]|1[0-2])(\/|-)(0[1-9]|[1-9]|[12][0-9]|(30|31))(\/|-)((19|20)\d{2}))'
monthdyr_date_pattern = r'((January|Jan|Febuary|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)\s(0[1-9]|[1-9]|[12][0-9]|30|31),\s((19|20)\d{2}))'
dmonthyr_date_pattern = r'((0[1-9]|[1-9]|[12][0-9]|30|31)\s(January|Jan|Febuary|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec),\s((19|20)\d{2}))'
yrmonthd_date_pattern = r'(((19|20)\d{2}),\s(January|Jan|Febuary|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)\s(0[1-9]|[1-9]|[12][0-9]|30|31))'


month_pattern = r'(January|Jan|Febuary|Feb|March|Mar|April|Apr|May|June|Jun|July|Jul|August|Aug|September|Sep|October|Oct|November|Nov|December|Dec)'
date_pattern = r'(3?1st|2?2nd|2?3rd|((1|2)?[0-9]|30)th)'
day_pattern = r'([tT]his\s|[nN]ext\s)?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
