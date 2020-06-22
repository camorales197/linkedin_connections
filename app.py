import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import streamlit as st
from PIL import Image


def fun(date):
    return datetime.datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d")

image = Image.open('get_data.png')


st.title("Exploring your Linkedin Conections")


st.write(
    'Since the arrival of GDPR law, websites are offering us the option of downloading "all" the personal data they have collected about us. '
    " However, without the proper tools or skills, this is not really useful for most users.")

st.write("This page guides and facilitates the process of extracting insights from your Linkedin data. "
         "You would be able to see a personalized graph like the one below. Just follow the steps. ")
'''
1. Log in in your Linkedin account and go to *"Settings & Privacy"*. 

2. Under the *"Privacy"* tab, in the *"How Linkedin uses your data"* click on *"Get a copy of your data"*

3. Mark only *"Connections"* and click on *"Request archive"*
'''
st.image(image, use_column_width=True)
'''
4. Now you need to wait for a few minutes while they prepare the data. They will send you an email when your download is ready. 

5. Once you receive the email, go back to the previous page, download it, and upload it in the file selector below.

'''

uploaded_file = st.file_uploader("Choose the *Connections.csv* file", type="csv")



if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Great! Your file has been successfully received. You can see the charts below.")

    df["Connected On"] = df["Connected On"].apply(fun)
    df = df.sort_values(by="Connected On")
    df.reset_index(inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns="index", inplace=True)
    df.rename(columns={"level_0": "number"}, inplace=True)
    df.drop(columns='Email Address', inplace=True)

    connections_line = px.line(df, x="Connected On", y="number", title='Evolution of the Number of Connections ',
                               template="simple_white", labels={'number': 'Number of Connections'})
    st.write(connections_line)


    def split_company(company):
        return company.split("-")[0]


    num_companies = 15
    height = 35 * num_companies

    top_companies = pd.DataFrame(df["Company"].value_counts().head(num_companies)).reset_index()
    top_companies.rename(columns={"index": "Company", "Company": "Number_Connections"}, inplace=True)
    top_companies["Company"] = top_companies["Company"].apply(split_company)
    fig = px.bar(top_companies, x='Number_Connections', y='Company', template="simple_white",
                 color="Company", title="Top {} Companies by Number of Connections".format(num_companies),
                 height=height)
    fig.update_layout(showlegend=False)
    st.write(fig)



    num_positions = 15
    height = 35 * num_positions

    top_positions = pd.DataFrame(df["Position"].value_counts().head(num_positions)).reset_index()
    top_positions.rename(columns={"index": "Position", "Position": "Number_Connections"}, inplace=True)

    fig = px.bar(top_positions, x='Number_Connections', y='Position', template="simple_white",
                 color="Position", title="Top {} Positions by Number of Connections".format(num_positions),
                 height=height)
    fig.update_layout(showlegend=False)
    st.write(fig)


    df = df.dropna()
    df.loc[df['Position'].str.contains('Intern'), 'Position'] = "Intern"
    Companies = df['Company']

    df['My Network'] = 'My Network'
    df["Full Name"] = df["First Name"] + " " + df["Last Name"]

    company_tree_map = px.treemap(df, path=['My Network', 'Company', 'Position', 'Full Name'], width=1000, height=800,
                                  template="simple_white", title="Treemap of Companies (click on it to zoom in)")
    st.plotly_chart(company_tree_map, use_container_width=True)

    positions_tree_map = px.treemap(df, path=['My Network', 'Position', 'Company', 'Full Name'], width=1000, height=800,
                                  template="simple_white", title="Treemap of Positions (click on it to zoom in)")
    st.plotly_chart(positions_tree_map, use_container_width=True)


st.write("")
st.write("Disclaimer: This site is just and MVP. It does not collect any information")
