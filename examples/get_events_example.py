#!/usr/bin/env python3
import json
from os import environ as env

import anyio

import aiocaldav as caldav

username = env["CALDAV_USERNAME"]
password = env["CALDAV_PASSWORD"]
url = env["CALDAV_URL"]
caldav_url = f"https://{url}/{username}/"
headers = {}


async def fetch_and_print():
    with caldav.DAVClient(
        url=caldav_url,
        username=username,
        password=password,
        # Optional parameter to set HTTP headers on each request if needed
        headers=headers,
    ) as client:
        print_calendars_demo((await client.principal()).calendars())


def print_calendars_demo(calendars):
    if not calendars:
        return
    events = []
    for calendar in calendars:
        for event in await calendar.events():
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append(fill_event(component, calendar))
    print(json.dumps(events, indent=2, ensure_ascii=False))


def fill_event(component, calendar) -> dict[str, str]:
    cur = {}
    cur["calendar"] = f"{calendar}"
    cur["summary"] = component.get("summary")
    cur["description"] = component.get("description")
    cur["start"] = component.get("dtstart").dt.strftime("%m/%d/%Y %H:%M")
    endDate = component.get("dtend")
    if endDate and endDate.dt:
        cur["end"] = endDate.dt.strftime("%m/%d/%Y %H:%M")
    cur["datestamp"] = component.get("dtstamp").dt.strftime("%m/%d/%Y %H:%M")
    return cur


if __name__ == "__main__":
    anyio.run(fetch_and_print)
