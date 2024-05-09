import streamlit as st
from main import ConsumerDisputeInsight

st.set_page_config(layout="wide", page_title="Consumer Dispute Insights", page_icon=":fontawesome:📄")
st.markdown(
    """
        <style>
            body {
                background-color: black; /* background color */
                }
            .stApp {
                background: linear-gradient(to right, #9ca1b9, #9ad1e7, #f7cece);
                }
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #333;
                color: white;
                text-align: center;
                font-size: 15px;
                padding: 10px 0;
            }
        </style>
    """+
    """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css" 
            rel="stylesheet" integrity="sha512-KfkfwYDsLkIlwQp6LFnl8zNdLGxu9YAA1QvwINks4PhcElQSvqcyVLLD9aMhXd13uQjoXtEKNosOWaZqXgel0g=="
            crossorigin="anonymous" referrerpolicy="no-referrer">""",
    unsafe_allow_html=True
            )


class Configuration:
    def __init__(self, consumer):
        self.consumer = consumer
        st.sidebar.image("Consumer_image_title.jpg") # SHOWS IMAGE TO THE SIDEBAR OF APPLICATION.
        st.title("Consumer Dispute Analysis") # SIDEBAR TITLE
       
    def sidebar_year_list(self):
        """
        To display a sidebar selectbox for selecting a year..

        Parameters:
            self: The instance of the Configuration class.

        Returns:
            selected_year (str): The selected year from the sidebar selectbox.
        """
        value = self.consumer.get_year_list_for_sidebar()
        selected_year = st.sidebar.selectbox("Select Year to View", value)
        return selected_year
    
    def show_basic_analysis(self, submitted_year)-> None: 
        """
        Shows basic insight of data..

        Parameters:
            self: The instance of the Configuration class.
            _submitted_year: The selected year from the sidebar selectbox.
        
        Requires:
            Object:  Access to Consumer objects to call shows_basic_analasis_function to preproces the data and return for rendering.

        Returns:
            None
        """
        result= self.consumer.show_basic_analysis_fun(submitted_year, self.submitted_by_left_panel)
        
        if self.submitted_by_left_panel == "Overall" and submitted_year == "Overall":
            Overall_data,top_issue,company_response=result
            st.header("Overall Analysis")
            st.dataframe(Overall_data)
            left_column, right_column = st.columns(2)
            with left_column:    # LEFT SIDE GRAPH
                st.write(f"**Top Issues Faced by Consumer**",top_issue)
               
            with right_column:  # RIGHT SIDE GRAPH
                st.write(f"**Top Company Response to Consumer**",company_response)

        else:
            st.header("Top Insight of Data:") # WHOLE DATA
            st.dataframe(result)

    def figures_analsis(self,current_selected_year):
        """
        Responsible for returning the analytics figure

        parameter:
            self: The instance of the Configuration class.
            current_selected_year: str
        
        Requires: streamlit library instance

        Returns: None
        """
        product_pie_chart,response_to_consumer_pie_chart,figure_count,figure_bar_plotly,dispute_resolved_bar_plotly = self.consumer.show_figures(current_selected_year)

        left_column, right_column = st.columns(2)
        with left_column:           
            st.header(str(current_selected_year ) +" Products")
            st.plotly_chart(product_pie_chart,use_container_width=True)
            
        with right_column:  
            
            st.header(str(current_selected_year ) +" Response to Consumer")
            st.plotly_chart(response_to_consumer_pie_chart,use_container_width=True)
        # SEABORN BAR GRPAH
        st.header(str(current_selected_year )+" Anaylsis of Product & Submitted ")
        st.pyplot(figure_count)

        left_column, right_column = st.columns(2)
        with left_column:           
            st.header(str(current_selected_year ) +" Disputes Submitted over Products")
            st.plotly_chart(figure_bar_plotly,use_container_width=True)
            
        with right_column:  
            
            st.header(str(current_selected_year ) +" Disputes over Products")
            st.plotly_chart(dispute_resolved_bar_plotly,use_container_width=True)


class SoicalFooterUI:
    def footer(self):
        """
        Function to display footer with social media links.

        Returns:
            None
        """
        social_media_links = {
            "GitHub": "https://github.com/Shivam-Shane",
            "Medium": "https://medium.com/@sk0551460",
            "LinkedIn": "https://www.linkedin.com/in/shivam-2641081a0/",
            "Portfolio": "https://shivam-shane.github.io/My_portfolio_website/"
        }

        icon_urls = {
        "GitHub": "fab fa-github",
        "Medium": "fab fa-medium",
        "LinkedIn": "fab fa-linkedin-in",
        "Portfolio": "far fa-envelope-open"
        }

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Stay connected with us on social media.**")
            for platform, url in social_media_links.items():
                icon_url = icon_urls[platform]
                st.markdown(f'<a href="{url}"><i class="{icon_url}" style="font-size: 30px;"></i> {platform}</a>'
                            , unsafe_allow_html=True)
                st.markdown(
            '<div class="footer"> '
            '<div>Thank you for visiting Consumer Dispute Insights! &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            '&nbsp;&nbsp;&nbsp;&nbsp; Copyright © 2024 &nbsp;&nbsp;SHIVAM </div>'
            '</div>',
            unsafe_allow_html=True
        )    



if __name__ == '__main__':
    # Instantiate objects
    consumer = ConsumerDisputeInsight()
    configuration = Configuration(consumer)
    soicalfooterui=SoicalFooterUI()
    # Sidebar options
    configuration.submitted_by_left_panel = st.sidebar.radio(
        'Select Submission Type',
        ('Overall', 'Web', 'Referral', 'Phone', 'Postal mail', 'Fax', 'Email')
    )
    # Sidebar year selection
    current_selected_year = configuration.sidebar_year_list()
    configuration.show_basic_analysis(current_selected_year)
    configuration.figures_analsis(current_selected_year)
    soicalfooterui.footer()