from ics import Calendar, Event
from datetime import timedelta
import config


def create_calendar_events(data):
    c = Calendar()

    for item in data:
        event = Event()
        event.name = f"到期提醒: {item['name']}"
        event.begin = item['maturity'].replace(hour=9, minute=0)
        event.description = (
            f"金额: ${item['amount']:,.2f}\n"
            f"利率: {item['rate'] * 100:.2f}%"
        )
        event.alarms = [{
            'trigger': -timedelta(days=config.REMINDER_DAYS),
            'action': 'display',
            'description': f"提前{config.REMINDER_DAYS}天提醒"
        }]
        c.events.add(event)


    with open('reminders.ics', 'w', encoding='utf-8') as f:
        f.write(c.serialize())