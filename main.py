import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from constant import CONFIG_FILE_PATH
from utils import read_yaml
from ensure import ensure_annotations


class ConsumerDisputeInsight:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.data = pd.read_csv(self.config.data_path)
        self.data['Date received'] = pd.to_datetime(self.data['Date received'])
        self.data['year'] = self.data['Date received'].dt.year
        self.product_count = self.data['Product'].value_counts()
        self.submitted_via_count = self.data['Submitted via'].value_counts()

    def show_basic_analysis_fun(self, submitted_year, submitted_by):
        if submitted_by == "Overall" and submitted_year == "Overall":
            overall_data = {"Unique Product List": len(self.product_count),
                            "Total Year": len(self.data['year'].unique()),
                            "Overall Dispute Submittion Mode": len(self.submitted_via_count),
                            "Total Consumer Disputes": (self.data['Consumer disputed?'] == 'Yes').sum()}
            overall_data = pd.DataFrame(overall_data, index=[0])
            top_issues = self.data['Issue'].value_counts().head(5)
            company_response = self.data['Company response to consumer'].value_counts().head(5)
            return overall_data, top_issues, company_response
        elif submitted_by == "Overall":
            return self.data[self.data['year'] == submitted_year].iloc[:10, 1:-1]
        elif submitted_year == "Overall":
            return self.data[self.data['Submitted via'] == submitted_by].iloc[:10, 1:-1]
        else:
            return self.data[(self.data['Submitted via'] == submitted_by) & (self.data['year'] == submitted_year)].iloc[:10, 1:-1]


 
    def get_year_list_for_sidebar(self)->list[str]:
        """
        Responsible for generating the year list for the application sidebar

        parameter: 
            None:
        return list of year
        """
        data_years = self.data['year'].unique().tolist()
        data_years.sort()
        data_years.insert(0, "Overall")
        return data_years
    
    def generate_figures(self,data):
        """
        Responsible for genrating the analytics figure over specified conditions received from UI

        parameter:
            data: dataframe , from UI as per conditions

        Requires: 
            data
        
        Returns: 
            a list of figures
        """
        figure_count, axes=plt.subplots(1,2,figsize=(15,10))
        palette_color_product = sns.color_palette("rocket")
        palette_color_submitted=sns.color_palette("viridis")
        # PLOTLY PIE CHART OF PRODUCT COUNT YEAR WISE
        product_pie_chart = px.pie(data, values=data['year'], names="Product", color_discrete_sequence=px.colors.sequential.Blugrn)
        # PLOTLY PIE CHART OF PRODUCT COUNT YEAR WISE
        response_to_consumer_pie_chart = px.pie(data, values=data['year'], names="Company response to consumer", color_discrete_sequence=px.colors.sequential.Sunset)
        response_to_consumer_pie_chart.update_layout(
            showlegend=False,
            margin=dict(t=0, b=0, r=0, l=0)
        )
        # SEABORN BAR CHART OF SUBMITTED VIE AND PRODUCT LIST
        sns.countplot(y=data["Product"], order=data["Product"].value_counts(ascending=True).index,ax=axes[0],palette=palette_color_product)
        sns.countplot(x = data['Submitted via'], data = data,ax=axes[1],palette=palette_color_submitted)
        plt.xlabel('Submitted', fontsize = 15)
        # PLOTLY BAR CHART DISOUTE BY SUBMISSION
        dispute_by_submission_bar_plotly=px.bar(data, x="Product", color="Submitted via")
        dispute_by_submission_bar_plotly.update_xaxes(title_text="Product Name")
        dispute_by_submission_bar_plotly.update_yaxes(title_text="Total Disputes")
        # PLOTLY BAR CHART DISPUTE OVER PRODUCTS
        dispute_resolved_bar_plotly=px.bar(data, x="Product", color="Consumer disputed?",color_discrete_sequence=px.colors.sequential.Sunset)
        dispute_resolved_bar_plotly.update_xaxes(title_text="Product Name")
        dispute_resolved_bar_plotly.update_yaxes(title_text="Total Disputes")
        

        return product_pie_chart,response_to_consumer_pie_chart,figure_count,dispute_by_submission_bar_plotly,dispute_resolved_bar_plotly

    def show_figures(self, submitted_year):
        """
        Responsible for returning the analytics figure

        parameter:
            submitted_year: str

        Requires: 
            data
        
        Returns: 
            a list of figure to render our application
        """
        if submitted_year == "Overall":
            return self.generate_figures(self.data)
        else:
            data = self.data[self.data['year'] == submitted_year]
            return self.generate_figures(data)