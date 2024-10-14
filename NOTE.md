## .ics format

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//appsheet.com//appsheet 1.0//EN #calendar properties
CALSCALE:GREGORIAN
BEGIN:VEVENT
SUMMARY:Invitation from <<USEREMAIL()>> to talk about <<[MeetingTopic]>>
UID:c7614cff-3549-4a00-9152-d25cc1fe077d
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:TRANSPARENT
DTSTART:<<[StartDateTime]>>
DTEND:<<[EndDateTime]>>
LOCATION:<<[MeetingAddress]>>
DESCRIPTION:<<[MeetingDescription]>>
END:VEVENT
END:VCALENDAR
```
OR

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//hacksw/handcal//NONSGML v1.0//EN
BEGIN:VEVENT
UID:uid1@example.com
ORGANIZER;CN=John Doe:MAILTO:john.doe@example.com
DTSTART:19970714T170000Z
DTEND:19970715T040000Z
SUMMARY:Bastille Day Party
GEO:48.85299;2.36885
END:VEVENT
END:VCALENDAR
```

- The most common representation of date and time is a tz timestamp such as
20010911T124640Z with the format <year (4 digits)><month (2)><day (2)>T<hour
(2)><minute (2)><second (2)>Z for a total fixed length of 16 characters. Z
indicates the use of UTC (referring to its Zulu time zone).[12] When used in
DTSTART and DTEND properties, start times are inclusive while end times are
not. This allows an event's end time to be the same as a consecutive event's
start without those events overlapping and potentially creating (false)
scheduling conflicts.

- Components include:

    - VEVENT describes an event, which has a scheduled amount of time on a
      calendar. Normally, when a user accepts the calendar event, this will
      cause that time to be considered busy, though an event can be set to be
      TRANSPARENT to change this interpretation. A VEVENT may include a VALARM
      which allows an alarm. Such events have a DTSTART which sets a starting
      time, and a DTEND which sets an ending time. If the calendar event is
      recurring, DTSTART sets up the start of the first event.
    - VTODO explains a to-do item, i.e., an action-item or assignment. Not all
      calendar applications recognize VTODO items. In particular, Outlook does
      not export Tasks as VTODO items, and ignores VTODO items in imported
      calendars.[14]
    - VJOURNAL is a journal entry. They attach descriptive text to a particular
      calendar date, may be used to record a daily record of activities or
      accomplishments, or describe progress with a related to-do entry. A
      VJOURNAL calendar component does not take up time on a calendar, so it
      has no effect on free or busy time (just like TRANSPARENT entries). In
      practice, few programs support VJOURNAL entries.
    - VFREEBUSY is a request for free/busy time, is a response to a request, or
      is a published set of busy time.[clarification needed] Other component
      types include VAVAILABILITY, VTIMEZONE (time zones) and VALARM (alarms).
      Some components can include other components (VALARM is often included in
      other components). Some components are often defined to support other
      components defined after them (VTIMEZONE is often used this
      way).[clarification needed]


ref:
- https://en.wikipedia.org/wiki/ICalendar
