import os
import requests
import json
import datetime

HEADERS = {
    'authorization': f'Token {os.getenv("TOKEN")}',
}

LESSON_TIMES = (
    "08:30 - 10:00", "10:10 - 11:40", "11:50 - 13:20", "14:00 - 15:30",
    "15:40 - 17:10", "17:20 - 18:50", "18:55 - 20:25", "20:30 - 22:00",
)

DAYS_OF_WEEK = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',
]


def date_to_style(input_date):
    date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    day_of_week = DAYS_OF_WEEK[date.weekday()]
    return f"{day_of_week}, {date.day}.{date.month}.{date.year}"


def fetch_lessons(group, week):
    params = {
        'group': group,
        'week': week
    }
    response = requests.get(f'http://194.85.206.18/list_schedule/', headers=HEADERS, params=params)
    lessons_raw = json.loads(response.text).get('stats')

    if not lessons_raw:
        return []

    lessons = []
    for lesson in lessons_raw:
        lesson_clean = parse_lesson(lesson)
        lessons.append(lesson_clean)
    return lessons


def parse_lesson(lesson_raw):
    teacher = lesson_raw.get('teacher').get('name')
    title = lesson_raw.get('title')
    subgroup = lesson_raw.get('subgroup')
    campus = lesson_raw.get('classroom').get('campus')
    room = lesson_raw.get('classroom').get('room_num')
    lesson_type = lesson_raw.get('lesson_type')
    lesson_number = lesson_raw.get('lesson_num')
    day = date_to_style(lesson_raw.get('date'))
    week = lesson_raw.get('week')
    time = LESSON_TIMES[lesson_raw.get('lesson_num') - 1]
    lesson = {
        'week': week,
        'day': day,
        'time': time,
        'title': title,
        'subgroup': subgroup,
        'campus': campus,
        'room': room,
        'lesson_number': lesson_number,
        'lesson_type': lesson_type,
    }
    return lesson

if __name__ == "__main__":
    group = '291Д-07ИБ/16'
    week = 0
    fetch_lessons(group, week)
    print(lessons)