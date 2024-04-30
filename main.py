import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from constant import *
from utils import read_yaml

class Consumer:
    def __init__(self, config_file_path=CONFIG_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.data = pd.read_csv(self.config.data_path)
        self.data['Date received'] = pd.to_datetime(self.data['Date received'])
        self.data['year'] = self.data['Date received'].dt.year

    def show_basic_analysis_fun(self, submitted_year, submitted_by):
        
        if submitted_by == "Overall" and submitted_year == "Overall":

            Overall_data={"Unique Product List":len((self.data['Product'].unique())),
                        "Total Year":len(self.data['year'].unique()),
                        "Overall Dispute Submittion Mode":len(self.data['Submitted via'].unique()),
                        "Total Consumer Disputes":len(self.data[self.data['Consumer disputed?']=='Yes'])
                          }
            overall_data=pd.DataFrame(Overall_data,index=[0])
            
            top_issues=self.data['Issue'].value_counts()[0:6]
            company_response=self.data['Company response to consumer'].value_counts()[0:6]
            total_dispute=self.data['Consumer disputed?'].value_counts()
            return overall_data,top_issues,company_response,total_dispute
    

        elif submitted_by == "Overall":
            return self.data[self.data['year'] == submitted_year].iloc[:10, 1:-1]
        elif submitted_year == "Overall":
            return self.data[self.data['Submitted via'] == submitted_by].iloc[:10, 1:-1]
        else:
            return self.data[(self.data['Submitted via'] == submitted_by) & (self.data['year'] == submitted_year)].iloc[:10, 1:-1]


    def year_list_for_sidebar(self):
        data_years = self.data['year'].unique().tolist()
        data_years.sort()
        data_years.insert(0, "Overall")
        return data_years

    def figure(self, submitted_year):
        figure_count, axes=plt.subplots(1,2,figsize=(12,8))
        data=self.data
        if submitted_year == "Overall":
            
            # Plotly Pie chart
            figure_pie = px.pie(data, values=data['year'], names="Product", color_discrete_sequence=px.colors.sequential.RdBu)
            # Seaborn bar chart
            sns.countplot(y=data["Product"], order=data["Product"].value_counts(ascending=True).index,ax=axes[0])
            sns.countplot(x = data['Submitted via'], data = data,ax=axes[1])
            figure_bar=px.bar(data,x = 'Product', y = 'Consumer disputed?')
            plt.xlabel('Submitted', fontsize = 15)

            return figure_pie,figure_count,figure_bar
        else:
            data = self.data[self.data['year'] == submitted_year]
            # Plotly Pie chart
            figure_pie = px.pie(data, values=data['year'], names="Product", color_discrete_sequence=px.colors.sequential.RdBu)
            # Seaborn bar chart
            sns.countplot(y=data["Product"], order=data["Product"].value_counts(ascending=True).index,ax=axes[0])
            sns.countplot(y=data['Submitted via'], data = data,ax=axes[1])
            figure_bar=px.bar(data,x = 'Product', y ='count',color='Consumer disputed?')


            plt.xlabel('Submitted', fontsize = 15)
            
            return figure_pie, figure_count
