import re
import pytz
import subprocess
from datetime import datetime, timedelta
from typing import List
import uuid
import dateformat

time_pattern = r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?\b|\b\d{2}:\d{2}\b'
timezone_pattern = r'\b(EST|PST|CST|MST|GMT|UTC|[A-Z]{3})\b'

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


def create_ics(sections, body):
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
    print(content)
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
    extract_dates = []
    yyyymmdd = re.findall(dateformat.yyyymmdd_date_pattern, line)
    # if yyyymmdd format does not exist
    if not yyyymmdd:
        ddmmyyyy = re.findall(dateformat.ddmmyyyy_date_pattern, line)
        # if ddmmyyyy format does not exist
        if not ddmmyyyy:
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
        else:
            for d in ddmmyyyy:
                try:
                    res_date = datetime.strptime(d[0], '%d/%m/%Y')
                except ValueError:
                    res_date = datetime.strptime(d[0], '%d-%m-%Y')

                extract_dates.append(res_date)

            return extract_dates

    else:
        for d in yyyymmdd:
            try:
                res_date = datetime.strptime(d[0], '%Y/%m/%d')
            except ValueError:
                res_date = datetime.strptime(d[0], '%Y-%m-%d')
            extract_dates.append(res_date)
        return extract_dates


def convert_timezone(time, date, timezone):
    try:
    # Attempt to parse as 24-hour time format "HH:MM"
        time_obj = datetime.strptime(time, "%H:%M").time()
    except ValueError:
        # If that fails, try 12-hour format with AM/PM "H:MMAM/PM"
        time_obj = datetime.strptime(time, "%I:%M%p").time()

    new_date = date
    new_date = new_date.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)

    timezone = pytz.timezone(timezone_offsets[timezone])
    new_date = timezone.localize(new_date).astimezone(pytz.utc)
    return new_date

# Convert to UTC-0
def generate_schedule(time_matches, date_matches, timezone_match):
    sdates = []
    edates = []
    # Each date has each pair time
    print(time_matches, date_matches, timezone_match)
    if len(date_matches) == len(time_matches)/2:
        for i,date in enumerate(date_matches):
            if len(time_matches)%2 == 0:
                sdates.append(convert_timezone(time_matches[i*2], date, timezone_match[0]))
                edates.append(convert_timezone(time_matches[i*2+1], date, timezone_match[0]))
            else:
                print("todo")
    else:
        for date in date_matches:
            if len(time_matches)%2 == 0:
                # Even time = start time
                for i in range(len(time_matches))[::2]:
                    sdates.append(convert_timezone(time_matches[i], date, timezone_match[0]))
                # Odd time = end time
                for i in range(len(time_matches))[1::2]:
                    edates.append(convert_timezone(time_matches[i], date, timezone_match[0]))
            else:
                print("todo")


    return (sdates, edates)

def extract_message(message: str):
    lines = message.splitlines()
    sections = {}
    current_section = None
    meta_eindex = 0

    for line in lines:
        if line.startswith("Content-Type:"):
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

    boundary_match = re.search(r'boundary="([^"]+)"', lines[meta_eindex])
    boundary = boundary_match.group(1) if boundary_match else ""
    body_content = ""
    end_body = 0


    time_matches = []
    timezone_match = []
    date_matches = []

    # Get message content
    for i, line in enumerate(lines[meta_eindex:]):
        if f"--{boundary}" in line:
            end_body += 1

        if end_body == 2:
            break

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

    sdates, edates = generate_schedule(time_matches,date_matches, timezone_match)

    print(body_content,sdates, edates)
    sections['Stime'] = []
    sections['Etime'] = []
    for i in range(len(sdates)):
        sections['Stime'].append(sdates[i].strftime("%Y%m%dT%H%M%SZ"))
        sections['Etime'].append(edates[i].strftime("%Y%m%dT%H%M%SZ"))

    sections['Timezone'] = timezone_match[0]

    return (sections, body_content)

def read_eml_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_email = file.read()

    return raw_email

file_path = "./message.eml"
email_text = read_eml_file(file_path)
message = extract_message(email_text)
create_ics(message[0], message[1])
open_in_thunderbird("./meeting_invitation.ics")
