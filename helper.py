import emoji
from urlextract import URLExtract
import pandas as pd
import seaborn as sns
from collections import Counter
extractor = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user !='Overall':
       df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['messages']:

        words.extend(message.split())

    num_media_messages=df[df['messages']=='<Media Omitted>\n'].shape[0]

    link = []
    for messages in df['messages']:
        link.extend(extractor.find_urls(messages))

    return num_messages,len(words),num_media_messages,len(link)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df =round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'user'})
    return x,df


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(25))

    return most_common_df
def emojis_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for messages in df['messages']:
        emojis.extend(c for c in messages if c in emoji.EMOJI_DATA)
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojis_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month_name']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return  df['day_name'].value_counts()
def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap=df.pivot_table(index='day_name', columns='periods', values='messages', aggfunc='count').fillna(0)

    return user_heatmap







