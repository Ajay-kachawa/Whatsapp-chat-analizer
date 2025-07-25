import re
import pandas as pd

def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['date'].dt.month_name()
    df['month_name'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()


    periods = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            periods.append(str(hour) + '-' + str(00))
        elif hour == 0:
            periods.append(str(00) + '-' + str(hour + 1))
        else:
            periods.append(str(hour) + '-' + str(hour + 1))
    df['periods'] = periods

    return df