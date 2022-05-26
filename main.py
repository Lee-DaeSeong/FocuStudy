import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt
from datetime import datetime
from PIL import Image

cv_point = pd.read_csv('CSV/point/point_csv.csv')
cv_point = cv_point.set_index('time')
logo = Image.open('logo.png')
st.set_page_config(layout="wide")
st.sidebar.image(logo)
name = st.sidebar.selectbox('Student', ['', '이대성', '한재민', '박준영'],
                            format_func=lambda x: 'Select Student' if x == '' else x)

if name:
    subject = st.sidebar.selectbox('Subject', ['', '캡스톤 디자인 1', '캡스톤디자인 2', '알고리즘', '자료구조'],
                                   format_func=lambda x: 'Select Subject' if x == '' else x)
    if subject:
        date = st.sidebar.date_input('Class Date', datetime(2022, 6, 9))
        if date.timetuple() != datetime(2022, 6, 9).timetuple():
            btn = st.sidebar.button('Start FocuStudy')
            if btn:
                video_file = open('WIN_20220411_23_40_10_Pro.mp4', 'rb')
                video_bytes = video_file.read()
                _, a, _ = st.columns((1, 2, 1))
                c, d = st.columns(2)

                with a:
                    vid = st.video(video_bytes)

                end = 0
                start = 0
                cv_melt = cv_point.reset_index().melt('time', var_name='category', value_name='y').sort_values('time')
                line_chart = alt.Chart(cv_melt[start:end]).mark_line(interpolate='basis').encode(
                    alt.X('time', title='sec'),
                    alt.Y('y', title='Point'),
                    color='category:N'
                    ).properties(
                    title='이해도 점수')
                with c:
                    temp = st.altair_chart(line_chart, use_container_width=True)
                with d:
                    temp1 = st.altair_chart(line_chart, use_container_width=True)

                prev = time.time()
                while True:
                    if end > len(cv_point) * 2:
                        break

                    if time.time() - prev >= 4.995:
                        print(vid)
                        print(time.time() - prev)
                        cv_melt = cv_point.reset_index().melt('time', var_name='category', value_name='y').sort_values(
                            'time')
                        line_chart = alt.Chart(cv_melt[start:end]).mark_line(interpolate='basis'). \
                            encode(alt.X('time', title='sec'), alt.Y('y', title='Point'), color='category:N'). \
                            properties(title='이해도 점수')
                        temp.altair_chart(line_chart, use_container_width=True)
                        temp1.altair_chart(line_chart, use_container_width=True)

                        end += 2
                        if 20 < end:
                            start += 2
                        prev = time.time()

                time.sleep(3)
                temp.altair_chart(line_chart, use_container_width=True)
                temp1.altair_chart(line_chart, use_container_width=True)
