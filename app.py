import streamlit as st
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import emoji
import seaborn as sns
st.sidebar.title('Whatsapp chat analysis')


uploaded_file = st.sidebar.file_uploader('choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)

    st.dataframe(df)
    #fetch unique usero
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)

if st.sidebar.button('Show analysis'):
    num_messages,words,num_media_messages,num_link = helper.fetch_stats(selected_user,df)
    st.title('Top statistic of whatsapp chat')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header('Total Messages')
        st.title(num_messages)
    with col2:
        st.header('Total Words')
        st.title(words)
    with col3:
        st.header('Total Media')
        st.title(num_media_messages)
    with col4:
        st.header('Links Shared')
        st.title(num_link)

if selected_user == 'Overall':
    st.title('Most busy users')
    x, new_df = helper.most_busy_users(df)
    fig, ax = plt.subplots()

    col1,col2 = st.columns(2)

    with col1:
         ax.bar(x.index,x.values,color='green')
         st.pyplot(fig)
    with col2:
        st.dataframe(new_df)

most_common_df = helper.most_common_words(selected_user,df)
st.dataframe(most_common_df)

fig, ax = plt.subplots()
ax.bar(most_common_df[0],most_common_df[1],color='orange')
plt.xticks(rotation=90)
st.title('Most Common User')
st.pyplot(fig)

emoji_df = helper.emojis_helper(selected_user,df)
st.title('Emoji Analysis')

col1,col2 = st.columns(2)

with col1:
    st.dataframe(emoji_df)
with col2:
    fig, ax = plt.subplots()
    ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct='%1.1f%%')
    st.pyplot(fig)

st.title('Monthly Timeline Analysis')
timeline = helper.monthly_timeline(selected_user,df)

fig, ax = plt.subplots()
ax.plot(timeline['time'],timeline['messages'])
plt.xticks(rotation = 90)

st.pyplot(fig)

st.title('Daily Timeline Analysis')
daily_timeline = helper.daily_timeline(selected_user,df)
fig, ax = plt.subplots()
ax.plot(daily_timeline['only_date'],daily_timeline['messages'],color = 'magenta')
plt.xticks(rotation = 90)
st.pyplot(fig)

st.title('Activity Map')
col1,col2 = st.columns(2)

with col1:
    st.header('Most Busy Day')
    busy_day = helper.week_activity_map(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(busy_day.index,busy_day.values,color='r')
    plt.xticks(rotation = 90)
    st.pyplot(fig)
with col2:
    st.header('Most Busy Month')
    busy_month = helper.monthly_activity_map(selected_user, df)
    fig, ax = plt.subplots()
    ax.bar(busy_month.index, busy_month.values, color='aqua')
    plt.xticks(rotation=90)
    st.pyplot(fig)

st.title('Online Activity Map')

user_heatmap= helper.activity_heatmap(selected_user,df)
fig, ax = plt.subplots()
ax = sns.heatmap(user_heatmap)
st.pyplot(fig)


