#!/usr/bin/env python
# coding: utf-8

# # Installing Libraries

# In[1]:


import pandas as pd
import numpy as np
import math
import pytz
import berserk # A Python client for the Lichess API.
import os
import datetime


# # Data Extraction

# ### Conection to *Berserk Client (API)*

# In[2]:


token = os.environ.get('TOKEN')
session = berserk.TokenSession(token)
client = berserk.Client(session=session)
extract = client.games.export_by_player('YourKingIsInDanger',
            as_pgn=False, since=None, until=None, max=None, vs=None, rated=True, 
            perf_type=None, color=None, analysed=None, moves=True, tags=True, 
            evals=False, opening=True)
data = list(extract)


# ### Understanding the Extracted Data

# In[3]:


type(data), type(data[0])


# In[4]:


data[0]


# In[5]:


raw_df = pd.DataFrame(data)
raw_df.head(1)


# In[6]:


raw_df.columns


# # Data Cleaning

# In our data we have\
# 1. id - *A unique game id of each game.*\
# 2. rated - *Is game rated or not: True/False*\
# 3. variant - *Game Variant: Standard, Chess960, From Position, CrazyHouse, etc.*\
# 4. speed - *Game Type: Rapid, Blitz, Bullet & classical*\
# 5. perf - *Similar of Game Type: Rapid, Blitz, Bullet & classical*\
# 6. createdAt - *Time at which game started: YYYY-MM-DD HH:MM:SS.ns+IST*\
# 7. lastMoveAt - *Time at which game ended: YYYY-MM-DD HH:MM:SS.ns+IST*\
# 8. status - *How the game ended: checkmate,resign,timeout,etc.*\
# 9. players - *Dictionary of players details Colorwise: Rating, Rating Change & id.*\
# 10. winner - *Color of the winner*\
# 11. opening - *A dictionary with Opening name, Eco & Ply for standard games.*\
# 12. moves -  *A string of the moves.*\
# 13. clock - *Time control of the game.*\
# 14. tournament - *Tournament id if the game is played in a tournament.*\
# 15. intialFen - *Opening for the game other than standard chess.*
# 
# ---
# I want to study my standard games as this is normal chess and it can only be analysed.\
# • So I will select the variant as standard and rated as True.

# #### Inspecting each field

# ###### 1. id

# - This is a unique game id, which refers to a particular game on the Lichess Server.

# In[7]:


# Renaming the column for better understanding
raw_df.rename(columns = {'id': 'Game ID'}, inplace = True)


# ###### 2. rated

# In[8]:


raw_df['rated'].unique()


# - It has only one value, so this column is no use of us

# ###### 3. variant 

# In[9]:


raw_df['variant'].unique()


# - I only want standard variant so removing all others

# In[10]:


raw_df = raw_df[raw_df['variant'] == 'standard'].copy()


# - Now as all of the records have same variant that is standard, So this column is also no use of us

# ###### 4 & 5. speed & perf

# In[11]:


raw_df['speed'].unique()


# In[12]:


raw_df['perf'].unique()


# - Both looks kind of same so let's check, if there are some data, where they differ in value

# In[13]:


raw_df[raw_df['speed'] != raw_df['perf']]


# - No, they are exactly same over all records. So, we can keep only 1 of them.

# - Now, I only want Blitz, Rapid and Bullet so removing classical

# In[14]:


raw_df = raw_df[raw_df['perf'] != 'classical'].copy()


# In[15]:


# Formating
raw_df.rename(columns = {'perf': 'Game Type'}, inplace = True)
raw_df['Game Type'] = raw_df['Game Type'].str.capitalize()


# ###### 6 & 7. createdAt & lastMoveAt

# In[16]:


raw_df[['createdAt','lastMoveAt']].dtypes


# - These are datetime objects but the timezone is UTC, we want Asia/Kolkata Timezone so,

# In[17]:


raw_df['createdAt'] = raw_df['createdAt'].dt.tz_convert('Asia/Kolkata')
raw_df['lastMoveAt'] = raw_df['lastMoveAt'].dt.tz_convert('Asia/Kolkata')


# In[18]:


raw_df[['createdAt','lastMoveAt']].head(1)


# - They contain microseconds, but we don't need that. so,

# In[19]:


raw_df['createdAt'] = pd.to_datetime(raw_df['createdAt'].dt.strftime('%Y-%m-%d %H:%M:%S'))
raw_df['lastMoveAt'] = pd.to_datetime(raw_df['lastMoveAt'].dt.strftime('%Y-%m-%d %H:%M:%S'))


# In[20]:


# Creating Seperate Date and Time fields for Day Analysis.
raw_df['Start Time'] = raw_df['createdAt'].dt.time
raw_df['Start Date'] = (raw_df['createdAt'].dt.date).astype('datetime64')

raw_df['End Time'] = raw_df['lastMoveAt'].dt.time
raw_df['End Date'] = (raw_df['lastMoveAt'].dt.date).astype('datetime64')


# In[21]:


raw_df.head(1)


# ###### 8. status

# In[22]:


raw_df['status'].unique()


# In[23]:


raw_df.rename(columns = {'status':'Status'}, inplace = True)


# In[24]:


# Formating
raw_df['Status'].replace({'outoftime':'Out Of Time', 'timeout': 'Game Abandoned', 
                          'resign': 'Resign', 'mate': 'Checkmate', 'stalemate': 'Stalemate',
                         'draw': 'Draw'}, inplace = True)


# In[25]:


raw_df['Status'].unique()


# #### 9. players

# In[26]:


raw_df['players']


# In[27]:


raw_df['players'][0]


# - The entry is a dictionary, with alot of data, so creating new columns to save that data

# In[28]:


raw_df['White_id'] = [x['white']['user']['id'] for x in raw_df['players']]
raw_df['White ELO'] = [x['white']['rating'] for x in raw_df['players']]
raw_df['White ELO Change'] = [x['white']['ratingDiff'] for x in raw_df['players']]

raw_df['Black_id'] = [x['black']['user']['id'] for x in raw_df['players']]
raw_df['Black ELO'] = [x['black']['rating'] for x in raw_df['players']]
raw_df['Black ELO Change'] = [x['black']['ratingDiff'] for x in raw_df['players']]


# - The data is stored in geenral way on basis of color but i want data basis on player so,

# In[29]:


raw_df['My ID'] = ''
raw_df['My Rating'] = ''
raw_df['My Rating Change'] = ''

raw_df['Opponent ID'] = ''
raw_df['Opponent Rating'] = ''
raw_df['Opponent Rating Change'] = ''
raw_df['My Color'] = ''


# In[30]:


raw_df.head(1)


# In[31]:


raw_df.columns


# - Index of the columns:\
# • 'White_id' - 19         • 'White ELO' - 20         • 'White ELO Change' - 21\
# • 'Black_id' - 22         • 'Black ELO' - 23         • 'Black ELO Change' - 24\
# • 'My ID' - 25            • 'My Rating' - 26         • 'My Rating Change' - 27\
# • 'Opponent ID' - 28      • 'Opponent Rating' - 29   • 'Opponent Rating Change' - 30\
# • 'My Color' - 31

# In[32]:


## Creating a function which will arrange the data on basis of players
def opp_my_distributor(checker, my, white, opp, black):
    for i in range(len(raw_df)):
        if raw_df.iloc[i,checker] == 'yourkingisindanger':
            raw_df.iloc[i,my] = raw_df.iloc[i,white]
            raw_df.iloc[i,opp] = raw_df.iloc[i,black]
            
        else:
            raw_df.iloc[i,my] = raw_df.iloc[i,black]
            raw_df.iloc[i,opp] = raw_df.iloc[i,white]


# In[33]:


opp_my_distributor(19, 25, 19, 28, 22) ## ID
opp_my_distributor(19, 26, 20, 29, 23) ## Rating
opp_my_distributor(19, 27, 21, 30, 24) ## Rating Change


# In[34]:


raw_df.loc[raw_df['White_id'] == 'yourkingisindanger', 'My Color'] = 'White'
raw_df.loc[raw_df['Black_id'] == 'yourkingisindanger', 'My Color'] = 'Black'


# In[35]:


raw_df.head(1)


# ###### 10. winner

# In[36]:


raw_df['winner'].unique()


# - The nan values in winner denotes the matches where the result is Draw

# In[37]:


# Making a Result with where i can record if i won, lose or draw.
raw_df.loc[raw_df['My Color'].str.lower() == raw_df['winner'], 'Result'] = "Won"
raw_df.loc[~(raw_df['My Color'].str.lower() == raw_df['winner']), 'Result'] = 'Lose'
raw_df.loc[raw_df['winner'].isna(), 'Result'] = 'Draw'


# In[38]:


raw_df.head(1)


# #### 11. opening

# In[39]:


raw_df['opening']


# - It is a Dictionary, so extracting the data using list comprehension

# In[40]:


raw_df['Opening ECO'] = [ x['eco'] for x in raw_df['opening']]
raw_df['Opening'] = [ x['name'] for x in raw_df['opening']]
raw_df['Opening Ply'] = [ x['ply'] for x in raw_df['opening']]


# In[41]:


raw_df['Opening']


# - The Opening name consists of the Main name and the variation, I want them seperately So,

# In[42]:


def seperator(x,y):
    try:
        l = x.split(':')
        if y == 0:
            return l[y]
        else:
            if len(l) == 1:
                return None
            else:
                return l[y]
            
    except:
        return None


# In[43]:


raw_df['Opening Name'] = [seperator(x,0) for x in raw_df['Opening']]
raw_df['Opening Variation'] = [seperator(x,1) for x in raw_df['Opening']]


# In[44]:


raw_df[['Opening','Opening Name', 'Opening Variation']].head()


# ###### 12. moves

# In[45]:


raw_df['moves'][0]


# - a move in chess means 1 by each player so only e4 is half move, e4 e5 is a 1st move

# In[46]:


## Calculating No. of Moves
raw_df['No. of Moves'] = [math.ceil(len(x.split())/2) for x in raw_df['moves']]


# In[47]:


## Extracting first 4 Moves
raw_df['1.0 Move'] = [ x.split()[0]  for x in raw_df['moves']]
raw_df['1.1 Move'] = [ x.split()[1]  for x in raw_df['moves']]
raw_df['2.0 Move'] = [ x.split()[2]  for x in raw_df['moves']]
raw_df['2.1 Move'] = [ x.split()[3]  for x in raw_df['moves']]


# In[48]:


## Alloting the first 4 moves to players
raw_df.loc[raw_df['My Color'] == 'White', 'M.1'] = raw_df[raw_df['My Color'] == 'White']['1.0 Move']
raw_df.loc[raw_df['My Color'] == 'White', 'M.2'] = raw_df[raw_df['My Color'] == 'White']['2.0 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'M.1'] = raw_df[raw_df['My Color'] == 'Black']['1.1 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'M.2'] = raw_df[raw_df['My Color'] == 'Black']['2.1 Move']

raw_df.loc[raw_df['My Color'] == 'White', 'O.1'] = raw_df[raw_df['My Color'] == 'White']['1.1 Move']
raw_df.loc[raw_df['My Color'] == 'White', 'O.2'] = raw_df[raw_df['My Color'] == 'White']['2.1 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'O.1'] = raw_df[raw_df['My Color'] == 'Black']['1.0 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'O.2'] = raw_df[raw_df['My Color'] == 'Black']['2.0 Move']


# In[49]:


raw_df.head(1)


# #### 13. clock

# In[50]:


raw_df['clock']


# In[51]:


raw_df['clock'][0]


# - Fomating it to the format: 5 Min + 0 Sec

# In[52]:


raw_df['Time Control'] = ['{} Min + {} Sec'.format((x['initial']//60), x['increment']) for x in raw_df['clock'] ]


# In[53]:


raw_df.head(1)


# ###### 14. tournament

# In[54]:


raw_df['tournament'].unique()


# So, if the game is played in a tournament it has a tournamnt id Where else there is None, so we'll make two columns,
# 1. Tournament Game - bool type
# 2. Tournament Id - str type

# In[55]:


raw_df.loc[raw_df['tournament'].isna(), 'Tournament Game'] = False
raw_df.loc[~(raw_df['tournament'].isna()), 'Tournament Game'] = True


# In[56]:


raw_df.rename(columns = {'tournament':'Tournament ID'}, inplace = True)


# ###### 15. initialFen

# In[57]:


raw_df['initialFen'].unique()


# It has nothing

# In[58]:


## Taking our Usefull Variables in a new Dataframe


# In[59]:


raw_df.columns


# In[60]:


Chess_df = raw_df[['Game ID', 'Start Date','Start Time', 'End Date', 'End Time', 'Game Type',
        'Time Control', 'Tournament Game', 'Tournament ID', 'createdAt', 'lastMoveAt',
        'My ID', 'My Rating', 'My Rating Change', 'My Color',
        'Opponent ID', 'Opponent Rating', 'Opponent Rating Change', 'Status',  'Result',
        'Opening ECO', 'Opening Ply', 'Opening', 'Opening Variation', 
        'No. of Moves', '1.0 Move', '1.1 Move', '2.0 Move', '2.1 Move', 
        'M.1', 'M.2', 'O.1', 'O.2']].copy()


# In[61]:


Chess_df.head()


# # Creating Calculated Fields

# ###### New Rating

# In[62]:


Chess_df['My New Rating'] = Chess_df['My Rating'] + Chess_df['My Rating Change']


# In[63]:


Chess_df.head(2)


# ##### Time Interval

# In[64]:


for i in range(24):
    Chess_df.loc[(datetime.time(i,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(i,59,59)), 'Time Interval'] =             '{} {} - {} {}'.format(12 if i == 0 else i if i < 13 else i-12, 'AM' if i < 12 else 'PM', 
                                   i+1 if i+1 < 13 else i+1 - 12, 'AM' if i==23 else 'AM' if i+1 < 12 else 'PM')


# ###### Day Time

# • 4AM - 7AM : Early Morning\
# • 7AM - 9AM : Morning\
# • 9AM - 12AM : Late Morning\
# • 12AM - 3AM : Afternooon\
# • 3AM - 5AM : Late Afternoon\
# • 5AM - 7AM : Early Evening\
# • 7AM - 9AM : Evening\
# • 9AM - 11AM : Late Evening\
# • 11AM - 2AM : Night\
# • 2AM - 4AM : Late night

# In[65]:


Chess_df.loc[(datetime.time(0,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(1,59,59)), 'Day Time'] = 'Night'

Chess_df.loc[(datetime.time(2,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(3,59,59)), 'Day Time'] = 'Late Night'

Chess_df.loc[(datetime.time(4,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(6,59,59)), 'Day Time'] = 'Early Morning'

Chess_df.loc[(datetime.time(7,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(8,59,59)), 'Day Time'] = 'Morning'

Chess_df.loc[(datetime.time(9,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(11,59,59)), 'Day Time'] = 'Late Morning'

Chess_df.loc[(datetime.time(12,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(14,59,59)), 'Day Time'] = 'Afternoon'

Chess_df.loc[(datetime.time(15,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(16,59,59)), 'Day Time'] = 'Late Afternoon'

Chess_df.loc[(datetime.time(17,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(19,59,59)), 'Day Time'] = 'Early Evening'

Chess_df.loc[(datetime.time(19,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(20,59,59)), 'Day Time'] = 'Evening'

Chess_df.loc[(datetime.time(21,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(22,59,59)), 'Day Time'] = 'Late Evening'

Chess_df.loc[(datetime.time(23,0,0) < Chess_df['Start Time']) &         (Chess_df['Start Time'] < datetime.time(23,59,59)), 'Day Time'] = 'Night'


# ##### Game Stage

# 0-15 Moves - Opening\
# 16-49 Moves - MidGame\
# 50+ Moves - EndGame
# 

# In[66]:


Chess_df.loc[Chess_df['No. of Moves'] <= 15, 'Game Stage'] = 'Opening'
Chess_df.loc[(Chess_df['No. of Moves'] >= 16) &             (Chess_df['No. of Moves'] <= 49), 'Game Stage'] = 'Middlegame'
Chess_df.loc[Chess_df['No. of Moves'] >= 50, 'Game Stage'] = 'Endgame'


# ###### Is Rating Difference More Than Me

# In[67]:


Chess_df.loc[(Chess_df['Opponent Rating'] - Chess_df['My Rating']) > 0, 
             'Rating Difference More Than Me'] = True

Chess_df.loc[(Chess_df['Opponent Rating'] - Chess_df['My Rating']) <= 0, 
             'Rating Difference More Than Me'] = False


# # Saving The File

# In[68]:


Chess_df.to_csv('Chess_df.csv')


# In[69]:


Chess_df.head(2)

