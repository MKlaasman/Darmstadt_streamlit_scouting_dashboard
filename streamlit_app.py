import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
# To show image of player
import requests
# plotting:
import seaborn as sns
import streamlit as st
from PIL import Image
from io import BytesIO
from matplotlib.colors import ListedColormap


## HOW TO RUN IN ANACONDA CMD:

#1) Go to right directory: "cd C:\Users\milan\Coding projects\Darmstadt_98\sofifa"
#2) "pip install --upgrade streamlit" in cmd
#3) Check whether it worked usin: "streamlit hello" in cmd , should open a new window in browser with the streamlit hello page
#4) Use Ctrl+C to exit the streamlit app, in Anaconda cmd.
#5) run this file using: "streamlit run streamlit_app.py" in cmd
#6) When making changes only save this python file, to update the dashboard!
##



## PUSHING TO HEROKU using git:
# https://towardsdatascience.com/from-streamlit-to-heroku-62a655b7319
# 1) "heroku login" in Anaconda cmd (opens browser with heroku login)
# 2) "heroku create" in Anaconda cmd
# 3) "git push heroku master", if this doesn't work, craete a new branch using: "git checkout -b masterbranch",
#     and then push using: "git push heroku masterbranch"
#git checkout -b masterbranch
##

# test
def plot_scatter(column_1, df, kpi_1, kpi_2, player_row, should_highlight_player=False):
    column_1.subheader('Scatterplot of two selected variables')
    if not should_highlight_player:
        fig = go.Figure(data=[go.Scatter(x=df[kpi_1], y=df[kpi_2],

                   mode='markers',
                   name='markers',
                   marker_color='royalblue',
                   hovertext= df[["Player Name", "Team", 'League']],
                   #hovertext2 = df["League"],
                   hoverlabel=dict(namelength=0),
                   hovertemplate='%{hovertext[0]} <br> %{hovertext[1]} <br> %{hovertext[2]} <br>x: %{x} <br>y: %{y}'
                   #hoverinfo='text'#hovertext=[df["Player_Name"], df["League"]]
                   )])
        fig.update_layout(title=f'Scatterplot of: {kpi_1} against {kpi_2}', autosize=False,
                          xaxis_title=f"{kpi_1}",
                          yaxis_title=f"{kpi_2}",
                          width=800, height=800,
                          margin=dict(l=40, r=40, b=40, t=40))

    else:
        fig =  go.Figure(
                    data=[go.Scatter(x=df[kpi_1], y=df[kpi_2], marker_color='lightgrey',
                                     mode='markers',
                                     name='Other players',
                                     hovertext=df[["Player Name", "Team", 'League']],
                                     hoverlabel=dict(namelength=0),
                                     hovertemplate='%{hovertext[0]} <br> %{hovertext[1]} <br> %{hovertext[2]} <br>x: %{x} <br>y: %{y}'

                                     )])

        fig.add_trace(go.Scatter(x=player_row[kpi_1], y=player_row[kpi_2], marker_color='royalblue',
                   mode='markers',
                   name=f"{player_row['Player Name'].iloc[0]}",
                   hovertext=player_row.loc[0, ["Player Name", "Team", 'League']],
                   hovertemplate='%{hovertext[0]} <br> %{hovertext[1]} <br> %{hovertext[2]} <br>x: %{x} <br>y: %{y}',
                   ))
        fig.update_layout(title=f'Scatterplot of: {kpi_1} against {kpi_2}', autosize=False,
                          xaxis_title=f"{kpi_1}",
                          yaxis_title=f"{kpi_2}",
                          width=800, height=800,
                          margin=dict(l=40, r=40, b=40, t=40))
    column_1.plotly_chart(fig)





## Settings:
max_width = 2000
padding_top = 5
padding_right = 5
padding_left = 5
padding_bottom = 5
COLOR = 'grey'
BACKGROUND_COLOR = 'white'
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )

#  extra layout:
# Create columns
#col1, col2 = st.beta_columns(2)
col0_small, col1, col2 = st.beta_columns([1, 20, 20])
# Create full column:
#col0_full, full_col = st.beta_columns([1, 40])
## To be continued


##  load in data;
#df = pd.read_csv('fbref_output.csv', index_col=0)
df = pd.read_csv('dashboard_df.csv', index_col = 0)
updated_df = df.copy()
league_list = [ 'Spain Primera Division', 'Italian Serie A',
       'English Premier League', 'French Ligue 1', 'German 1. Bundesliga',
       'Holland Eredivisie', 'Belgian Jupiler Pro League',
       'Swiss Super League', 'Danish Superliga', 'German 2. Bundesliga',
       'Austrian Football Bundesliga', 'Swedish Allsvenskan',
       'German 3. Bundesliga']

position_list = ['LWB','LB','CB','RB','RWB',
                'LM', 'CM', 'CAM', 'CDM', 'RM',
                'LW','ST','RW', 'CF']


## Create sidebar
logo = Image.open('darmstadt_logo.png')
st.sidebar.image(logo)#, caption='SV Darmstadt 98 scouting dashboard')
#col2.image(logo)#, caption='SV Darmstadt 98 scouting dashboard')
col1.title('Scouting Dashboard - SV Darmstadt 98')
#col1.title('')

#st.sidebar.title("KPI selection")
#st.sidebar.markdown("Choose here which KPIs you would like to see in the charts on the right 🐦")


features_updating_list = []

# widgets
#column_list = [ 'Age', 'Height', 'Weight','Sprint Speed']
#for col in column_list:

#    # 1) add sidebar
#    features_updating_list.append(st.sidebar.slider(col,df[col].min(), df[col].max(), (df[col].min(), df[col].max()) ))


# 2) select two features from list:
#kpis = df.columns
#kpi_1 =st.sidebar.selectbox("Select Scatterplot KPI 1", kpis, 4)
#kpi_2 =st.sidebar.selectbox("Select Scatterplot KPI 2", kpis, 3)


# 3) select the leagues of interest
#league_choices = st.sidebar.multiselect("Select specific leagues", league_list)
#if len(league_choices) > 0: # thus not empty
#    updated_df = updated_df[updated_df['League'].isin(league_choices)]

# 4) select the position of interest
#position_choices = st.sidebar.multiselect("Select positions", position_list)
#if len(position_choices) > 0: # thus not empty
#    esc_lst = [re.escape(s) for s in position_choices]
#    pattern = '|'.join(esc_lst)
#    updated_df = updated_df[updated_df['Position'].str.contains(pattern, case=False, na= False)]

# 5) Select one player from the DataFrame
#selected_player =st.sidebar.selectbox("Select Scatterplot KPI 2", list(df['Player Name'].unique()), 1)


## UPDATE DATAFRAME

count = 0
for feature in features_updating_list:
    updated_df = updated_df[(updated_df[column_list[count]] >= feature[0]) & (updated_df[column_list[count]] <= feature[1])]
    count += 1
# league
#updated_df = updated_df[(updated_df[column_list[count]] >= feature[0]) & (updated_df[column_list[count]] <= feature[1])]


with st.beta_expander("Analyze league"):
    st.subheader('Select your league')
    selected_league = st.selectbox("Analyze your league:", df['League'].unique())
    #with col1:
    # st.dataframe(updated_df)
    selected_league_df = df[df.League == selected_league]
    st.write(selected_league_df)
#with full_col:
with st.beta_expander("Analyze individual player"):

            #if st.checkbox('Analyze individual player'):
            col1, col2 = st.beta_columns(2)

            with col1:
                selected_player = st.selectbox("Select player of interest", df['Player Name'], 0)
            with col2:
                analyse_as = st.selectbox("Analyze as what type of player:", ['Goalkeeper', 'Defender', 'Midfielder', 'Attacker'], 3)
            with col1:
                st.subheader(f'Analyze {selected_player} as a: {analyse_as}')
            player_row = df[df['Player Name'] == selected_player]
            player_url = df[df['Player Name'] == selected_player]['Image Page'].iloc[0]
            club_url = df[df['Player Name'] == selected_player]['Team Image Page'].iloc[0]

            try:
                response = requests.get(player_url)
                player_img = Image.open(BytesIO(response.content))
                with col1:
                    st.image(player_img)
            except:
                not_found_url = 'https://cdn.sofifa.com/players/notfound_0_240.png'
                response = requests.get(not_found_url)
                player_img = Image.open(BytesIO(response.content))
                with col1:
                    st.image(player_img)

            response = requests.get(club_url)
            club_img = Image.open(BytesIO(response.content))
            with col2:
                st.subheader(f"Playing at {player_row['Team'].iloc[0]}")
                st.image(club_img)
            if analyse_as == 'Goalkeeper':
                column_names = ['Total Goalkeeping', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning',
                                'GK Reflexes']
            elif analyse_as == 'Defender':
                column_names = ['Total Defending','Positioning', 'Interceptions',  'Marking', 'Standing Tackle',
                                'Sliding Tackle']
            elif analyse_as == 'Midfielder':
                column_names = ['Total Skill', 'Total Power', 'Total Defending', 'Total Attacking', 'Ball Control',
                                'Short Passing', 'Long Passing', 'Ball Control', 'Finishing']
            elif analyse_as == 'Attacker':
                column_names = ['Total Attacking', 'Finishing', 'Sprint Speed', 'Acceleration', 'Composure', 'Ball Control',
                                'Long Shots']

            barchart_names_x = column_names
            barchart_values_y = player_row[column_names].values[0]
            fig, ax = plt.subplots()
            ax.barh(barchart_names_x, barchart_values_y,  align='center') #xerr=error,
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Percentual performance')
            ax.set_title(f'Attributes of player: {selected_player} as a {analyse_as}')
            with col2:
                st.pyplot(fig)


            kpis = df.columns
            # show swarmplot:
            with col1:

                individual_swarmplot_kpi = st.selectbox("Select a KPI for swarm plot:", kpis, 2)
                # plot examples:
                fig, ax = plt.subplots()
                sns.set(style="whitegrid")

                # cmap = plt.get_cmap('tab10')
                cmap = ListedColormap(['gold', 'crimson', 'teal', 'orange'])
                player_value = player_row[individual_swarmplot_kpi]
                league_df = df[df.League == player_row.League.iloc[0]]
                ax = sns.swarmplot(x=league_df[individual_swarmplot_kpi],  alpha = 0.5)#color='grey',
                for col in ax.collections:
                    y = col.get_offsets()[:, 0]
                    perc = np.percentile(y, [25, 50, 75])
                    col.set_cmap(cmap)
                    col.set_array(np.digitize(y, perc))
                sns.swarmplot(x=player_value, color = 'black')

                plt.title(f"{selected_player}'s {individual_swarmplot_kpi}, against players of {player_row.League.iloc[0]}")
                plt.annotate(player_row['Player Name'].iloc[0], xy=(player_value, -0.02))
                st.pyplot(fig)


            ## scatterplot individual player:
            if st.checkbox('Show Scatterplot:'):
                kpi_1 = col1.selectbox("Select Individual Scatterplot KPI 1", kpis, 4)
                kpi_2 = col1.selectbox("Select Individual Scatterplot KPI 2", kpis, 3)
                plot_scatter(col1, updated_df, kpi_1, kpi_2, player_row, True)



with st.beta_expander("Analyze between leagues:"):
    col_leagues_1, col_leagues_2 = st.beta_columns(2)
    updated_df = df.copy()
    st.subheader('Dataframe')
    league_choices = st.multiselect("Select the leagues:", league_list, ("Spain Primera Division")
                                    )
    column_choices = st.multiselect("Select the KPIs of interest:", df.columns)

    #if st.checkbox('Select specific KPIs'):

    if len(column_choices) > 0:
            list_to_add = []
            if not 'Player Name' in column_choices:
                list_to_add.append('Player Name')
            if not 'League' in column_choices:
                list_to_add.append('Team')
            if not 'Player Name' in column_choices:
                list_to_add.append('League')
            column_choices = list_to_add + column_choices
            updated_df = updated_df[column_choices]
    if len(league_choices) > 0:  # thus not empty
            updated_df = updated_df[updated_df['League'].isin(league_choices)]
    st.write(updated_df)

    #with col2:
    # Create a Check box to display the raw data.
    st.subheader('Scatterplot')
    kpis = df.columns
    kpi_1 = st.selectbox("Select Scatterplot KPI 1", kpis, 4)
    kpi_2 = st.selectbox("Select Scatterplot KPI 2", kpis, 3)
    if st.checkbox('Show Between Leagues Scatterplot:'):
        plot_scatter(col_leagues_1, updated_df, kpi_1, kpi_2, updated_df.iloc[0], False)








