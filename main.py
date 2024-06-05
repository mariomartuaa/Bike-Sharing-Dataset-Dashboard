import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Bike Sharing Dataset Dashboard')
st.write('Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, environmental and health issues. Apart from interesting real world applications of bike sharing systems, the characteristics of data being generated by these systems make them attractive for the research. Opposed to other transport services such as bus or subway, the duration of travel, departure and arrival position is explicitly recorded in these systems. This feature turns bike sharing system into a virtual sensor network that can be used for sensing mobility in the city. Hence, it is expected that most of important events in the city could be detected via monitoring these data.')
st.markdown('- Python libraries: numpy, pandas, streamlit, matplotlib, seaborn')
st.markdown('- Data source: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data')

df_hour = pd.read_csv("hour.csv")
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])



tab1, tab2, tab3 = st.tabs(["Dataset Table", "Counting Hourly", " Counting Time Span"])

with tab1:
        st.table(data=df_hour[:50])

with tab2:
        
        min_date = df_hour['dteday'].min()
        max_date = df_hour['dteday'].max()

        date = st.date_input(
                label = 'Choose a Date', 
                min_value=min_date,
                max_value=max_date,
                value= min_date)
        
        df = df_hour[df_hour['dteday'] == str(date)]
        
        
        morning_data = df[df['hr'] <= 10]
        ttl_morning = morning_data['casual'].sum()
        ttl_morning2 = morning_data['registered'].sum()
        afternoon_data = df[(df['hr'] >= 11) & (df['hr'] <= 14)]
        ttl_afternoon = afternoon_data['casual'].sum()
        ttl_afternoon2 = afternoon_data['registered'].sum()
        evening_data = df[(df['hr'] >= 15) & (df['hr'] <= 17)]
        ttl_evening = evening_data['casual'].sum()
        ttl_evening2 = evening_data['registered'].sum()
        night_data = df[df['hr'] >= 18]
        ttl_night = night_data['casual'].sum()
        ttl_night2 = night_data['registered'].sum()

        total = [ttl_morning, ttl_afternoon, ttl_evening, ttl_night]
        total2 = [ttl_morning2, ttl_afternoon2, ttl_evening2, ttl_night2]
        mean_total = sum(total) / 24
        mean_total2 = sum(total2) / 24
        hours = [x for x in range(24)]
        total_hour = []
        total_hour2 = []
        
        time = ['Morning','Afternoon','Evening','Night']
        type = ['Casual', 'Registered']
        
        st.subheader('Total of Bike Sharing by Hourly')
        fig, ax = plt.subplots(figsize=(15,6))
        for i in range(24):
                total_hour.append(df[df['hr'] == i]['casual'].sum())
                barplot1 = ax.bar(x= i-0.2, height= total_hour[i], width=0.4, color = '#E67F0D')
                ax.bar_label(barplot1, labels= [total_hour[i]])
                total_hour2.append(df[df['hr'] == i]['registered'].sum())
                barplot2 = ax.bar(x= i+0.2, height= total_hour2[i], width=0.4, color = '#93C572')
                ax.bar_label(barplot2, labels= [total_hour2[i]])
        ax.set_xticks(range(len(df['hr'].unique())))
        ax.set_xticklabels(f'{x}:00' for x in range(len(df['hr'].unique())))
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_ylabel('Total')
        ax.legend(type)
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(15,6))
        ax.plot(hours, total_hour)
        ax.plot(hours, total_hour2)
        ax.set_xticks(range(len(df['hr'].unique())))
        ax.set_xticklabels(f'{x}:00' for x in range(len(df['hr'].unique())))
        ax.set_ylabel('Total')
        ax.tick_params(axis='x', labelrotation=45)
        ax.legend(type)
        st.pyplot(fig)
        
        st.subheader('Average of Bike Sharing by Hourly')
        fig, ax = plt.subplots(figsize=(7,6))
        barplot1 = ax.bar(x= 0, height= mean_total, width=0.4, color = '#E67F0D')
        ax.bar_label(barplot1, labels= [f'{mean_total:,.2f}'])
        barplot2 = ax.bar(x= 1, height= mean_total2, width=0.4, color = '#93C572')
        ax.bar_label(barplot2, labels= [f'{mean_total2:,.2f}'])
        ax.set_xticks(range(2))
        ax.set_xticklabels(type)
        ax.set_ylabel('Total')
        st.pyplot(fig)

        st.subheader('Total of Bike Sharing by Time')
        st.markdown("The chart represents the total value of bike rentals based on time:")
        st.markdown("- Morning: 00:00 - 10:59 WIB")
        st.markdown("- Afternoon: 11:00 - 14:59 WIB")
        st.markdown("- Evening: 15:00 - 17:59 WIB")
        st.markdown("- Night: 18:00 - 23:59 WIB")
               
        fig, ax = plt.subplots(figsize=(15,6))
        for i in range(len(time)):
                barplot1 = ax.bar(x= i-0.2, height= total[i], width=0.4, color = '#E67F0D')
                ax.bar_label(barplot1, labels= [total[i]])
                barplot2 = ax.bar(x= i+0.2, height= total2[i], width=0.4, color = '#93C572')
                ax.bar_label(barplot2, labels= [total2[i]])
        ax.set_xticks(range(len(time)))
        ax.set_xticklabels(time)
        ax.set_xlabel('Time')
        ax.set_ylabel('Total')
        ax.legend(type)
        st.pyplot(fig)
        
        st.subheader('Distribution of Bike Sharing by Time')
        colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
        
        total = (ttl_morning, ttl_afternoon, ttl_evening, ttl_night)
        total2 = (ttl_morning2, ttl_afternoon2, ttl_evening2, ttl_night2)
        
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
        ax[0].pie(x=total, labels=time, autopct='%1.1f%%',colors=colors)
        ax[1].pie(x=total2, labels=time, autopct='%1.1f%%',colors=colors)
        ax[0].set_title('Casual')
        ax[1].set_title('Registered')
        st.pyplot(fig)
        
        sunny_data = df[df['weathersit'] == 1]
        ttl_sunny = sunny_data['casual'].sum()
        ttl_sunny2 = sunny_data['registered'].sum()
        cd_data = df[df['weathersit'] == 2]
        ttl_cd = cd_data['casual'].sum()
        ttl_cd2 = cd_data['registered'].sum()
        lr_data = df[df['weathersit'] == 3]
        ttl_lr = lr_data['casual'].sum()
        ttl_lr2 = lr_data['registered'].sum()
        hr_data = df[df['weathersit'] == 4]
        ttl_hr = hr_data['casual'].sum()
        ttl_hr2 = hr_data['registered'].sum()

        total = [ttl_sunny, ttl_cd, ttl_lr]
        total2 = [ttl_sunny2, ttl_cd2, ttl_lr2]
        
        weathers = ['Sunny', 'Cloudy/Misty', 'Rain']
        
        st.subheader('Total of Bike Sharing Hourly by Weather')
        
        fig, ax = plt.subplots(figsize=(15,6))
        for i in range(len(weathers)):
                barplot1 = ax.bar(x= i-0.2, height= total[i], width=0.4, color = '#E67F0D')
                ax.bar_label(barplot1, labels= [total[i]])
                barplot2 = ax.bar(x= i+0.2, height= total2[i], width=0.4, color = '#93C572')
                ax.bar_label(barplot2, labels= [total2[i]])
        ax.set_xticks(range(len(weathers)))
        ax.set_xticklabels(weathers)
        ax.set_xlabel('Weathers')
        ax.set_ylabel('Total')
        ax.legend(type)
        st.pyplot(fig)
        
        st.subheader('Distribution of Bike Sharing Hourly by Weather')
        colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
        
        total = (ttl_sunny, ttl_cd, ttl_lr)
        total2 = (ttl_sunny2, ttl_cd2, ttl_lr2)
        
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
        ax[0].pie(x=total, labels=weathers, autopct='%1.1f%%',colors=colors)
        ax[1].pie(x=total2, labels=weathers, autopct='%1.1f%%',colors=colors)
        ax[0].set_title('Casual')
        ax[1].set_title('Registered')
        st.pyplot(fig)
        
        st.subheader('Bike Sharing by Temperature and Apparent Temperature')
        fig, ax = plt.subplots(figsize=(12,5))
        sns.scatterplot(data = df, x='cnt', y='temp',label='Temperature')
        sns.scatterplot(data = df, x='cnt', y='atemp', label='Apparent Temperature')
        ax.set_xlabel('Total')
        ax.set_ylabel('Suhu')
        ax.legend()
        st.pyplot(fig)
        
        st.subheader('Correlation of Bike Sharing, Temperature and Apparent Temperature')
        fig, ax = plt.subplots(figsize=(5,5))
        korelasi = korelasi = df[['cnt','temp','atemp']].corr()
        sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt=".2f")
        ax.set_title('Correlation Heatmap')
        st.pyplot(fig)
        

with tab3:
        df_day = pd.read_csv("C:\\Users\\Mario\\Downloads\\dicoding project 2\\data\\new_data.csv")
        df_day['date'] = pd.to_datetime(df_day['date'])
        
        min_date = df_day['date'].min()
        max_date = df_day['date'].max() 
        
        start_date, end_date = st.date_input(
                label='Choose a Date Span', min_value=min_date,
                max_value=max_date,
                value=[min_date, max_date])

        df = df_day[(df_day['date'] >= str(start_date)) & (df_day['date'] <= str(end_date))]
        df1 = df_hour[(df_hour['dteday'] >= str(date)) & (df_hour['dteday'] <= str(end_date))]
        
        st.subheader('Total of Bike Sharing by Day')
        
        monday_data = df[df['day'] == "Monday"]
        ttl_monday = monday_data['total'].sum()
        casual_monday = monday_data['casual'].sum()
        reg_monday = monday_data['registered'].sum()
        tuesday_data = df[df['day'] == "Tuesday"]
        ttl_tuesday = tuesday_data['total'].sum()
        casual_tuesday = tuesday_data['casual'].sum()
        reg_tuesday = tuesday_data['registered'].sum()
        wednesday_data = df[df['day'] == 'Wednesday']
        ttl_wednesday = wednesday_data['total'].sum()
        casual_wednesday = wednesday_data['casual'].sum()
        reg_wednesday = wednesday_data['registered'].sum()
        thursday_data = df[df['day'] == 'Thursday']
        ttl_thursday = thursday_data['total'].sum()
        casual_thursday = thursday_data['casual'].sum()
        reg_thursday = thursday_data['registered'].sum()
        friday_data = df[df['day'] == 'Friday']
        ttl_friday = friday_data['total'].sum()
        casual_friday = friday_data['casual'].sum()
        reg_friday = friday_data['registered'].sum()
        saturday_data = df[df['day'] == 'Saturday']
        ttl_saturday = saturday_data['total'].sum()
        casual_saturday = saturday_data['casual'].sum()
        reg_saturday = saturday_data['registered'].sum()
        sunday_data = df[df['day'] == 'Sunday']
        ttl_sunday = sunday_data['total'].sum()
        casual_sunday = sunday_data['casual'].sum()
        reg_sunday = sunday_data['registered'].sum()
        
        total_day = [ttl_monday, ttl_tuesday, ttl_wednesday, ttl_thursday, ttl_friday, ttl_saturday, ttl_sunday]
        casual_day = [casual_monday, casual_tuesday, casual_wednesday, casual_thursday, casual_friday, casual_saturday, casual_sunday]
        reg_day = [reg_monday, reg_tuesday, reg_wednesday, reg_thursday, reg_friday, reg_saturday, reg_sunday]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig, ax = plt.subplots(figsize=(15,6))
        barplot =  ax.bar(x= days, height= total_day)
        ax.bar_label(barplot, labels= total_day)
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(15,6))
        for i in range(len(casual_day)):
                barplot1 =  ax.bar(x= i-0.2, height= casual_day[i], width = 0.4, color = '#E67F0D')
                ax.bar_label(barplot1, labels= [casual_day[i]])
                barplot2 = ax.bar(x= i+0.2, height= reg_day[i], width = 0.4, color = '#93C572')
                ax.bar_label(barplot2, labels= [reg_day[i]])
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days)
        ax.set_xlabel('Days')
        ax.set_ylabel('Total')
        ax.legend(type)
        st.pyplot(fig) 
        
        st.subheader('Distribution of Bike Sharing by Day')
        colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
        ax[0].pie(x=casual_day, labels=days, autopct='%1.1f%%',colors=colors)
        ax[1].pie(x=reg_day, labels=days, autopct='%1.1f%%',colors=colors)
        ax[0].set_title('Casual')
        ax[1].set_title('Registered')
        st.pyplot(fig)
        
        morning_data = df1[df1['hr'] <= 10]
        ttl_morning = morning_data['cnt'].sum()
        casual_morning = morning_data['casual'].sum()
        reg_morning = morning_data['registered'].sum()
        afternoon_data = df1[(df1['hr'] >= 11) & (df1['hr'] <= 14)]
        ttl_afternoon = afternoon_data['cnt'].sum()
        casual_afternoon = afternoon_data['casual'].sum()
        reg_afternoon = afternoon_data['registered'].sum()
        evening_data = df1[(df1['hr'] >= 15) & (df1['hr'] <= 17)]
        ttl_evening = evening_data['cnt'].sum()
        casual_evening = evening_data['casual'].sum()
        reg_evening = evening_data['registered'].sum()
        night_data = df1[df1['hr'] >= 18]
        ttl_night = night_data['cnt'].sum()
        casual_night = night_data['casual'].sum()
        reg_night = night_data['registered'].sum()
        
        totalh = [ttl_morning, ttl_afternoon, ttl_evening, ttl_night]
        casual_time = [casual_morning, casual_afternoon, casual_evening, casual_night]
        reg_time = [reg_morning, reg_afternoon, reg_evening, reg_night]
        time = ['Morning','Afternoon','Evening','Night']
        
        st.subheader('Total of Bike Sharing by Time')
        st.markdown("The chart represents the total value of bike rentals based on time:")
        st.markdown("- Morning: 00:00 - 10:59 WIB")
        st.markdown("- Afternoon: 11:00 - 14:59 WIB")
        st.markdown("- Evening: 15:00 - 17:59 WIB")
        st.markdown("- Night: 18:00 - 23:59 WIB")
        
        fig, ax = plt.subplots(figsize=(15,6))
        barplot2 = ax.bar(x= time, height= totalh)
        ax.bar_label(barplot2, labels = totalh)
        st.pyplot(fig)
        
        fig, ax = plt.subplots(figsize=(15,6))
        for i in range(len(casual_time)):
                barplot1 =  ax.bar(x= i-0.2, height= casual_time[i], width = 0.4, color = '#E67F0D')
                ax.bar_label(barplot1, labels= [casual_time[i]])
                barplot2 = ax.bar(x= i+0.2, height= reg_time[i], width = 0.4, color = '#93C572')
                ax.bar_label(barplot2, labels= [reg_time[i]])
        ax.set_xticks(range(len(time)))
        ax.set_xticklabels(time)
        ax.set_xlabel('Time')
        ax.set_ylabel('Total')
        ax.legend(type)
        st.pyplot(fig) 
        
        st.subheader('Distribution of Bike Sharing by Time')
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
        ax[0].pie(x=casual_time, labels=time, autopct='%1.1f%%',colors=colors)
        ax[1].pie(x=reg_time, labels=time, autopct='%1.1f%%',colors=colors)
        ax[0].set_title('Casual')
        ax[1].set_title('Registered')
        st.pyplot(fig)

        sunny_data = df[(df['weather_map'] == 1) & (df['status'] == 'Weekday')]
        avg_sunnywd = sunny_data['total'].mean()
        cd_data = df[(df['weather_map'] == 2) & (df['status'] == 'Weekday')]
        avg_cdwd = cd_data['total'].mean()
        lr_data = df[(df['weather_map'] == 3) & (df['status'] == 'Weekday')]
        avg_lrwd = lr_data['total'].mean()

        avg = [avg_sunnywd, avg_cdwd, avg_lrwd]

        st.subheader('Average Weekday Bike Sharing Based On Weather')
        fig, ax = plt.subplots(figsize=(10,6))
        barplot = ax.bar(x= ['Sunny', 'Cloudy/Misty', 'Rain'], height= avg)
        ax.bar_label(barplot, labels=[f'{x:,.2f}' for x in avg], fontsize = 10)
        st.pyplot(fig)

        sunny_data = df[(df['weather_map'] == 1) & (df['status'] == 'Weekend')]
        avg_sunnyw = sunny_data['total'].mean()
        cd_data = df[(df['weather_map'] == 2) & (df['status'] == 'Weekend')]
        avg_cdw = cd_data['total'].mean()
        lr_data = df[(df['weather_map'] == 3) & (df['status'] == 'Weekend')]
        avg_lrw = lr_data['total'].mean()

        avg = [avg_sunnyw, avg_cdw, avg_lrw]

        st.subheader('Average Weekend Bike Sharing Based On Weather')
        fig, ax = plt.subplots(figsize=(10,6))
        barplot = ax.bar(x= ['Sunny', 'Cloudy/Misty', 'Rain'], height= avg)
        ax.bar_label(barplot, labels=[f'{x:,.2f}' for x in avg], fontsize = 10)
        st.pyplot(fig)
        
        sunny_data = df[(df['weather_map'] == 1) & (df['status'] == 'Holiday')]
        avg_sunnyh = sunny_data['total'].mean()
        cd_data = df[(df['weather_map'] == 2) & (df['status'] == 'Holiday')]
        avg_cdh = cd_data['total'].mean()
        lr_data = df[(df['weather_map'] == 3) & (df['status'] == 'Holiday')]
        avg_lrh = lr_data['total'].mean()

        avg = [avg_sunnyh, avg_cdh, avg_lrh]

        st.subheader('Average Holiday Bike Sharing Based On Weather')
        fig, ax = plt.subplots(figsize=(10,6))
        barplot = ax.bar(x= ['Sunny', 'Cloudy/Misty', 'Rain'], height= avg)
        ax.bar_label(barplot, labels=[f'{x:,.2f}' for x in avg], fontsize = 10)
        ax.set_title('Rata-rata peminjaman sepeda pada hari libur berdasarkan cuaca')
        st.pyplot(fig)
        
        sunny_data2 = df[df['weather_map'] == 1]
        avg_sunnyt = sunny_data2['total'].mean()
        cd_data2 = df[df['weather_map'] == 2]
        avg_cdt = cd_data2['total'].mean()
        lr_data2 = df[df['weather_map'] == 3]
        avg_lrt = lr_data2['total'].mean()
                        
        avgt = [avg_sunnyt, avg_cdt, avg_lrt]
        
        for i in range(len(avgt)):
                if np.isnan(avgt[i]):
                        avgt[i] = 0
        
        st.subheader('Distribution of Bike Sharing Based On Weather')
        fig, ax = plt.subplots(figsize=(15,6))
        ax.pie(
                x = avgt,
                labels = weathers,
                autopct='%1.1f%%',
                colors = colors
        )
        st.pyplot(fig)

        st.subheader('Bike Sharing by Temperature and Apparent Temperature')
        fig, ax = plt.subplots(figsize=(12,5))
        sns.scatterplot(data = df, x='total', y='temp',label='Suhu')
        sns.scatterplot(data = df, x='total', y='atemp', label='Suhu Jelas')
        ax.set_xlabel('Total')
        ax.set_ylabel('Suhu')
        ax.legend()
        st.pyplot(fig)

        st.subheader('Correlation of Bike Sharing, Temperature and Apparent Temperature')
        fig, ax = plt.subplots(figsize=(5,5))
        korelasi = korelasi = df[['total','temp','atemp']].corr()
        sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt=".2f")
        ax.set_title('Correlation Heatmap')
        st.pyplot(fig)
