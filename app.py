import time
import streamlit as st
from main import Consumer
st.markdown(
            """
    <style>
    body {
        background-color: black; /* Set background color of entire body */
    }
    .stApp {
        background: linear-gradient(to right, #9ca1b9, #9ad1e7, #f7cece); /* Set background color of main content area */
    }

    </style>
    """,
    unsafe_allow_html=True
            )

class Configuration:
    def __init__(self, consumer):
        self.consumer = consumer
        st.sidebar.image("Consumer_image_title.jpg")
        
    def sidebar_year_list(self):
        value = self.consumer.year_list_for_sidebar()
        selected_year = st.sidebar.selectbox("Year_Selection", value)
        return selected_year

    def show_basic_analysis(self, submitted_year):
        result= self.consumer.show_basic_analysis_fun(submitted_year, self.submitted_by_left_panel)
        
        if self.submitted_by_left_panel == "Overall" and submitted_year == "Overall":
            Overall_data,top_issue,company_response,total_dispute=result
            st.header("Overall Analysis")
            st.dataframe(Overall_data)
            left_column, right_column = st.columns(2)
            with left_column:
                st.write(f"**Top Issues list faced by Consumer**")
                st.write(top_issue)
            with right_column:  
                st.write(f"**Top Company Response to Consumer**")
                st.write(company_response)

            st.write(f"**Consumer Disputed**")
            st.write(total_dispute)
        else:
            st.header("Top 10 Rows of DATA:")
            st.dataframe(result)


    def figures_analsis(self,submitted_year):
        st.header(str(submitted_year)+' Product List')
        figure_pie,figure_count,figure_bar = self.consumer.figure(current_selected_year)
        st.plotly_chart(figure_pie)
        st.header(str(submitted_year )+" Anaylsis of Product & Submitted ")
        st.pyplot(figure_count)
        st.plotly_chart(figure_bar)


    def print_time(self,start_time,end_time):
        start_time
        st.write(f"Time taken to render: {end_time - start_time} seconds")

if __name__ == '__main__':
    start_time = time.time()
    consumer = Consumer()
    Configuration_object = Configuration(consumer)

    Configuration_object.submitted_by_left_panel = st.sidebar.radio(
        'Submitted By',
        ('Overall', 'Web', 'Referral', 'Phone', 'Postal mail', 'Fax', 'Email')
    )

    current_selected_year = Configuration_object.sidebar_year_list()
    Configuration_object.show_basic_analysis(current_selected_year)
    Configuration_object.figures_analsis(current_selected_year)
    end_time = time.time()
    Configuration_object.print_time(start_time,end_time)
    
