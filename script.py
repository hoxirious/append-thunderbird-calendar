import re
import pytz
import subprocess
from datetime import datetime, timedelta
from typing import List
import uuid
import dateformat
from tzlocal import get_localzone
import zoneinfo

time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b|\b\d{2}:\d{2}\b'
timezone_pattern = r'\b(EST|PST|CST|MST|GMT|UTC)\b'

day_enum = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

month_dict = {
    'Jan': 'January',
    'Feb': 'Febuary',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December',
        }

timezone_offsets = {
        "EST": "America/New_York",
        "PST": "America/Los_Angeles",
        "CST": "America/Chicago",
        "MST": "America/Denver",
        "GMT": "Etc/GMT",
        "UTC": "UTC"
}


def create_ics(sections, body, html):
    file_path = "./meeting_invitation.ics"

    content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//{sections['Subject']}{sections['Date']}//EN
CALSCALE:GREGORIAN
"""
    for i in range(len(sections['Stime'])):
        uid = str(uuid.uuid4())
        # Construct the event block
        event_block = f"""BEGIN:VEVENT
SUMMARY:{f"Event {i}: {sections['Subject']}"}
UID:{uid}
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:OPAQUE
DTSTART:{sections['Stime'][i]}
DTEND:{sections['Etime'][i]}
DESCRIPTION:{body}
END:VEVENT
"""
        # Add the event block to the main content
        content += event_block

    content += "END:VCALENDAR\n"

    with open(file_path,'w', encoding='utf-8') as file:
        file.write(content)

def open_in_thunderbird(ics_file_path):
    thunderbird_path = "/usr/bin/thunderbird"

    try:
        subprocess.run([thunderbird_path, ics_file_path], check=True)
        print(f"Opened {ics_file_path} in Thunderbird for import.")
    except FileNotFoundError:
        print("Error: Thunderbird executable not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error opening Thunderbird: {e}")

def extract_from_language(line:str) -> List[datetime]|None:
    day = re.findall(dateformat.day_pattern,line)
    reference_date = datetime.now()
    # if next|this Friday
    if day:
        res_date: datetime = reference_date

        pre_day = day[0][0]
        extract_day = day[0][1]
        today_day = reference_date.strftime("%A")
        date_diff = 0
        i = day_enum.index(today_day)
        is_next = "next" in pre_day or "Next" in pre_day
        did_jump = False
        while day_enum[i] != extract_day:
            if (i+1)%7 == 0:
                did_jump = True
            i = (i+1)%7
            date_diff += 1

        if is_next and not did_jump:
            date_diff += 7

        res_date = reference_date + timedelta(date_diff)

        return [res_date]
    # if 4th July...
    else:
        date = re.findall(dateformat.date_pattern,line)
        month = re.findall(dateformat.month_pattern,line)
        if date and month:
            current_year = reference_date.year
            date = date[0][0][:-2]
            month = month_dict.get(month[0], month[0])
            try:
                res_date = datetime.strptime(f"{date} {month} {current_year}", "%d %B %Y")
            except ValueError:
                res_date = datetime.strptime(f"{date} {month} {current_year}", "%d %b %Y")

            return [res_date]
        else:
            return None

# assuming every line contains 1 date
    # time extraction:
    # 12:00
    # 1 PM | 1PM | 1 AM | 1AM
    # 1200
    # [start1,end1,start2, end2] | [start1,start2] + length
    # timezone is null -> use local timezone.

    # date extraction
    # this|next Thursday
    # 27/08/2024 | 27-08-2024
def extract_date(line:str) -> List[datetime]|None:
    yyyymmdd = re.findall(dateformat.yyyymmdd_date_pattern, line)
    if not yyyymmdd:
        ddmmyyyy = re.findall(dateformat.ddmmyyyy_date_pattern, line)
        if not ddmmyyyy:
            mmddyyyy = re.findall(dateformat.mmddyyyy_date_pattern,line)
            if not mmddyyyy:
                monthdyr = re.findall(dateformat.monthdyr_date_pattern, line)
                if not monthdyr:
                    dmonthyr = re.findall(dateformat.dmonthyr_date_pattern, line)
                    if not dmonthyr:
                        yrmonthd = re.findall(dateformat.yrmonthd_date_pattern, line)
                        if not yrmonthd:
                            return extract_from_language(line)
                        else:
                            yrmonthd_formats = ['%Y, %B %d', '%Y, %B %w', '%Y, %b %d', '%Y, %b %w']
                            return format_dates(yrmonthd, yrmonthd_formats)
                    else:
                        dmonthyr_formats = ['%d %B, %Y', '%w %B, %Y', '%d %b, %Y', '%w %b, %Y']
                        return format_dates(dmonthyr, dmonthyr_formats)
                else:
                    monthdyr_formats = ['%B %d, %Y', '%B %w, %Y', '%b %d, %Y', '%b %w, %Y']
                    return format_dates(monthdyr, monthdyr_formats)
            else:
                mmddyyyy_formats = ['%m/%d/%Y', '%m/%w/%Y', '%m-%d-%Y', '%m-%w-%Y']
                return format_dates(mmddyyyy, mmddyyyy_formats)
        else:
            ddmmyyyy_formats = ['%d/%m/%Y', '%w/%m/%Y', '%d-%m-%Y', '%w-%m-%Y']
            return format_dates(ddmmyyyy, ddmmyyyy_formats)
    else:
        yyyymmdd_formats = ['%Y/%m/%d', '%Y/%m/%w', '%Y-%m-%d', '%Y-%m-%w']
        return format_dates(yyyymmdd, yyyymmdd_formats)

def format_dates(dates, formats):
    extract_dates = []
    for d in dates:
        for fmt in formats:
            try:
                res_date = datetime.strptime(d[0], fmt)
                extract_dates.append(res_date)
            except ValueError:
                continue
    return extract_dates

def convert_timezone(time, date: datetime, timezone: zoneinfo.ZoneInfo):
    time_format = ['%H:%M','%H:%M%p','%H:%M %p','I:%M%p', 'I:%M %p']
    for fmt in time_format:
        try:
        # Attempt to parse as 24-hour time format "HH:MM"
            time_obj = datetime.strptime(time,fmt).time()
            new_date = date
            new_date = new_date.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)

            _timezone = pytz.timezone(timezone.key)
            new_date = _timezone.localize(new_date).astimezone(pytz.utc)
            return new_date
        except ValueError:
            continue

    return None

# Convert to UTC-0
def generate_schedule(time_matches, date_matches, timezone_match):
    sdates = []
    edates = []
    # Default length is 60 minutes
    meeting_length = 1
    # Each date has two time sets - start and end time.
    # Even index of time_matches represents for start time
    # Odd index of time_matches represents for end time
    if len(date_matches) == len(time_matches)/2:
        for i,date in enumerate(date_matches):
            sdates.append(convert_timezone(time_matches[i*2], date, timezone_match))
            edates.append(convert_timezone(time_matches[i*2+1], date, timezone_match))
    else:
        for date in date_matches:
            # for each date, add all even indexes time_matches to start time
            # and add odd indexes of time_matches to end time
            if len(time_matches)%2 == 0:
                # Even time = start time
                for i in range(len(time_matches))[::2]:
                    sdates.append(convert_timezone(time_matches[i], date, timezone_match))
                # Odd time = end time
                for i in range(len(time_matches))[1::2]:
                    edates.append(convert_timezone(time_matches[i], date, timezone_match))

            # for each date, add every index of time_matches as start time and increment 60 minutes as end time
            else:
                for i in range(len(time_matches)):
                    sdate = convert_timezone(time_matches[i], date, timezone_match)
                    sdates.append(sdate)
                    if sdate:
                        edate = sdate.replace(hour=sdate.hour+meeting_length, minute=sdate.minute, second=0, microsecond=0)
                    else:
                        edate = sdate
                    edates.append(edate)

    return (sdates, edates)

def extract_message(message: str):
    lines = message.splitlines()
    sections = {}
    current_section = None
    meta_eindex = 0
    boundary_match = None
    boundary = ""

    for line in lines:
        if re.search(r'boundary="([^"]+)"', line):
            boundary_match = re.search(r'boundary="([^"]+)"', lines[meta_eindex])
            meta_eindex += 1
            continue

        if boundary_match and boundary_match.group(1) in line :
            boundary = boundary_match.group(1)
            break

        if re.match(r'^[A-Za-z\-]+:', line):
            header = line.split(":")[0]
            sections[header] = line.split(":", 1)[1].strip()
            current_section = header
        elif current_section:
            sections[current_section] += line + " "
        meta_eindex += 1;

    for key in sections:
        sections[key] = sections[key].strip()

    body_content = ""
    html_content = ""
    end_body = 0


    time_matches = []
    timezone_match = []
    date_matches = []

    # Get message content
    for i, line in enumerate(lines[meta_eindex:]):
        if f"--{boundary}" in line:
            end_body += 1

        if end_body == 3:
            break

        if end_body == 1:
            body_content += line
            # Date Extract
            date = extract_date(line)
            if date:
                date_matches.extend(date)

            # Time Extract
            time = re.findall(time_pattern, line)
            if time:
                time_matches.extend(time)

            timezone = re.findall(timezone_pattern, line)
            if timezone:
                timezone_match.extend(timezone)
        if end_body == 2:
            html_content += line

    sdates, edates = generate_schedule(time_matches,date_matches, timezone_match[0] if len(timezone_match) > 0 else get_localzone())
    sections['Stime'] = []
    sections['Etime'] = []
    for i in range(len(sdates)):
        sections['Stime'].append(sdates[i].strftime("%Y%m%dT%H%M%SZ"))
        sections['Etime'].append(edates[i].strftime("%Y%m%dT%H%M%SZ"))

    sections['Timezone'] = timezone_match[0] if len(timezone_match) > 0 else get_localzone()

    return (sections, body_content, html_content)

def read_eml_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_email = file.read()

    return raw_email

file_path = "./message.eml"
email_text = read_eml_file(file_path)
message = extract_message(email_text)
create_ics(message[0], message[1], message[2])
open_in_thunderbird("./meeting_invitation.ics")
