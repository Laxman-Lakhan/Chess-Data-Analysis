# Installing Libraries


```python
import pandas as pd
import numpy as np
import math
import pytz
import berserk # A Python client for the Lichess API.
import os
import datetime
```

# Data Extraction

### Conection to *Berserk Client (API)*


```python
token = os.environ.get('TOKEN')
session = berserk.TokenSession(token)
client = berserk.Client(session=session)
extract = client.games.export_by_player('YourKingIsInDanger',
            as_pgn=False, since=None, until=None, max=None, vs=None, rated=True, 
            perf_type=None, color=None, analysed=None, moves=True, tags=True, 
            evals=False, opening=True)
data = list(extract)
```

### Understanding the Extracted Data


```python
type(data), type(data[0])
```




    (list, dict)




```python
data[0]
```




    {'id': 'qnrlibcn',
     'rated': True,
     'variant': 'standard',
     'speed': 'blitz',
     'perf': 'blitz',
     'createdAt': datetime.datetime(2022, 6, 14, 13, 20, 41, 543000, tzinfo=datetime.timezone.utc),
     'lastMoveAt': datetime.datetime(2022, 6, 14, 13, 30, 45, 745000, tzinfo=datetime.timezone.utc),
     'status': 'resign',
     'players': {'white': {'user': {'name': 'YourKingIsInDanger',
        'id': 'yourkingisindanger'},
       'rating': 1659,
       'ratingDiff': -8},
      'black': {'user': {'name': 'Agustin_Perez', 'id': 'agustin_perez'},
       'rating': 1606,
       'ratingDiff': 7}},
     'winner': 'black',
     'opening': {'eco': 'C50',
      'name': 'Italian Game: Hungarian Defense',
      'ply': 6},
     'moves': 'e4 e5 Nf3 Nc6 Bc4 Be7 c3 d6 d4 exd4 cxd4 Bg4 h3 Bxf3 Qxf3 Nf6 Be3 O-O O-O a6 Nc3 b5 Bb3 Na5 Bd5 Nxd5 Nxd5 Nc4 b3 Nxe3 fxe3 Bg5 Rf2 c5 Raf1 f6 g3 Ra7 h4 Bh6 Qf5 Raf7 Kh2 Qd7 Qf3 cxd4 exd4 Qe6 Qf5 Qxf5 Rxf5 a5 g4 Bd2 Kg3 b4 Kf2 g6 Rf3 Kg7 Ke2 Bh6 e5 dxe5 dxe5 fxe5 Rxf7+ Rxf7 Rxf7+ Kxf7 Kd3 Bf8 Ke4 Bd6 Nb6 Ke6 Nc4 Bc7 h5 gxh5 gxh5 Kf6 Kd5 Kf5 Ne3+ Kf4 Nc4 e4 Kd4 Kg5 Kxe4 Kxh5 Kd5 Kg4 Kc6 Bd8 Kb5 h5 Nxa5 Bxa5 Kxa5 h4 Kxb4 h3 a4 h2 a5 h1=Q a6 Qa8 a7 Qxa7 Kc4 Qb6 Kc3',
     'clock': {'initial': 300, 'increment': 0, 'totalTime': 300}}




```python
raw_df = pd.DataFrame(data)
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>perf</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>status</th>
      <th>players</th>
      <th>winner</th>
      <th>opening</th>
      <th>moves</th>
      <th>clock</th>
      <th>tournament</th>
      <th>initialFen</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>blitz</td>
      <td>2022-06-14 13:20:41.543000+00:00</td>
      <td>2022-06-14 13:30:45.745000+00:00</td>
      <td>resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>{'eco': 'C50', 'name': 'Italian Game: Hungaria...</td>
      <td>e4 e5 Nf3 Nc6 Bc4 Be7 c3 d6 d4 exd4 cxd4 Bg4 h...</td>
      <td>{'initial': 300, 'increment': 0, 'totalTime': ...</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
raw_df.columns
```




    Index(['id', 'rated', 'variant', 'speed', 'perf', 'createdAt', 'lastMoveAt',
           'status', 'players', 'winner', 'opening', 'moves', 'clock',
           'tournament', 'initialFen'],
          dtype='object')



# Data Cleaning

In our data we have\
1. id - *A unique game id of each game.*\
2. rated - *Is game rated or not: True/False*\
3. variant - *Game Variant: Standard, Chess960, From Position, CrazyHouse, etc.*\
4. speed - *Game Type: Rapid, Blitz, Bullet & classical*\
5. perf - *Similar of Game Type: Rapid, Blitz, Bullet & classical*\
6. createdAt - *Time at which game started: YYYY-MM-DD HH:MM:SS.ns+IST*\
7. lastMoveAt - *Time at which game ended: YYYY-MM-DD HH:MM:SS.ns+IST*\
8. status - *How the game ended: checkmate,resign,timeout,etc.*\
9. players - *Dictionary of players details Colorwise: Rating, Rating Change & id.*\
10. winner - *Color of the winner*\
11. opening - *A dictionary with Opening name, Eco & Ply for standard games.*\
12. moves -  *A string of the moves.*\
13. clock - *Time control of the game.*\
14. tournament - *Tournament id if the game is played in a tournament.*\
15. intialFen - *Opening for the game other than standard chess.*

---
I want to study my standard games as this is normal chess and it can only be analysed.\
• So I will select the variant as standard and rated as True.

#### Inspecting each field

###### 1. id

- This is a unique game id, which refers to a particular game on the Lichess Server.


```python
# Renaming the column for better understanding
raw_df.rename(columns = {'id': 'Game ID'}, inplace = True)
```

###### 2. rated


```python
raw_df['rated'].unique()
```




    array([ True])



- It has only one value, so this column is no use of us

###### 3. variant 


```python
raw_df['variant'].unique()
```




    array(['standard', 'chess960', 'crazyhouse', 'fromPosition'], dtype=object)



- I only want standard variant so removing all others


```python
raw_df = raw_df[raw_df['variant'] == 'standard'].copy()
```

- Now as all of the records have same variant that is standard, So this column is also no use of us

###### 4 & 5. speed & perf


```python
raw_df['speed'].unique()
```




    array(['blitz', 'rapid', 'bullet', 'classical'], dtype=object)




```python
raw_df['perf'].unique()
```




    array(['blitz', 'rapid', 'bullet', 'classical'], dtype=object)



- Both looks kind of same so let's check, if there are some data, where they differ in value


```python
raw_df[raw_df['speed'] != raw_df['perf']]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>perf</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>status</th>
      <th>players</th>
      <th>winner</th>
      <th>opening</th>
      <th>moves</th>
      <th>clock</th>
      <th>tournament</th>
      <th>initialFen</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



- No, they are exactly same over all records. So, we can keep only 1 of them.

- Now, I only want Blitz, Rapid and Bullet so removing classical


```python
raw_df = raw_df[raw_df['perf'] != 'classical'].copy()
```


```python
# Formating
raw_df.rename(columns = {'perf': 'Game Type'}, inplace = True)
raw_df['Game Type'] = raw_df['Game Type'].str.capitalize()
```

###### 6 & 7. createdAt & lastMoveAt


```python
raw_df[['createdAt','lastMoveAt']].dtypes
```




    createdAt     datetime64[ns, UTC]
    lastMoveAt    datetime64[ns, UTC]
    dtype: object



- These are datetime objects but the timezone is UTC, we want Asia/Kolkata Timezone so,


```python
raw_df['createdAt'] = raw_df['createdAt'].dt.tz_convert('Asia/Kolkata')
raw_df['lastMoveAt'] = raw_df['lastMoveAt'].dt.tz_convert('Asia/Kolkata')
```


```python
raw_df[['createdAt','lastMoveAt']].head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2022-06-14 18:50:41.543000+05:30</td>
      <td>2022-06-14 19:00:45.745000+05:30</td>
    </tr>
  </tbody>
</table>
</div>



- They contain microseconds, but we don't need that. so,


```python
raw_df['createdAt'] = pd.to_datetime(raw_df['createdAt'].dt.strftime('%Y-%m-%d %H:%M:%S'))
raw_df['lastMoveAt'] = pd.to_datetime(raw_df['lastMoveAt'].dt.strftime('%Y-%m-%d %H:%M:%S'))
```


```python
# Creating Seperate Date and Time fields for Day Analysis.
raw_df['Start Time'] = raw_df['createdAt'].dt.time
raw_df['Start Date'] = (raw_df['createdAt'].dt.date).astype('datetime64')

raw_df['End Time'] = raw_df['lastMoveAt'].dt.time
raw_df['End Date'] = (raw_df['lastMoveAt'].dt.date).astype('datetime64')
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>status</th>
      <th>players</th>
      <th>winner</th>
      <th>opening</th>
      <th>moves</th>
      <th>clock</th>
      <th>tournament</th>
      <th>initialFen</th>
      <th>Start Time</th>
      <th>Start Date</th>
      <th>End Time</th>
      <th>End Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>{'eco': 'C50', 'name': 'Italian Game: Hungaria...</td>
      <td>e4 e5 Nf3 Nc6 Bc4 Be7 c3 d6 d4 exd4 cxd4 Bg4 h...</td>
      <td>{'initial': 300, 'increment': 0, 'totalTime': ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>18:50:41</td>
      <td>2022-06-14</td>
      <td>19:00:45</td>
      <td>2022-06-14</td>
    </tr>
  </tbody>
</table>
</div>



###### 8. status


```python
raw_df['status'].unique()
```




    array(['resign', 'outoftime', 'timeout', 'mate', 'draw', 'stalemate'],
          dtype=object)




```python
raw_df.rename(columns = {'status':'Status'}, inplace = True)
```


```python
# Formating
raw_df['Status'].replace({'outoftime':'Out Of Time', 'timeout': 'Game Abandoned', 
                          'resign': 'Resign', 'mate': 'Checkmate', 'stalemate': 'Stalemate',
                         'draw': 'Draw'}, inplace = True)
```


```python
raw_df['Status'].unique()
```




    array(['Resign', 'Out Of Time', 'Game Abandoned', 'Checkmate', 'Draw',
           'Stalemate'], dtype=object)



#### 9. players


```python
raw_df['players']
```




    0       {'white': {'user': {'name': 'YourKingIsInDange...
    1       {'white': {'user': {'name': 'Hanber', 'id': 'h...
    2       {'white': {'user': {'name': 'YourKingIsInDange...
    3       {'white': {'user': {'name': 'Gryym', 'id': 'gr...
    4       {'white': {'user': {'name': 'YourKingIsInDange...
                                  ...                        
    1223    {'white': {'user': {'name': 'Osla', 'id': 'osl...
    1224    {'white': {'user': {'name': 'Sanyi80', 'id': '...
    1225    {'white': {'user': {'name': 'YourKingIsInDange...
    1226    {'white': {'user': {'name': 'VeenaG', 'id': 'v...
    1227    {'white': {'user': {'name': 'YourKingIsInDange...
    Name: players, Length: 1212, dtype: object




```python
raw_df['players'][0]
```




    {'white': {'user': {'name': 'YourKingIsInDanger', 'id': 'yourkingisindanger'},
      'rating': 1659,
      'ratingDiff': -8},
     'black': {'user': {'name': 'Agustin_Perez', 'id': 'agustin_perez'},
      'rating': 1606,
      'ratingDiff': 7}}



- The entry is a dictionary, with alot of data, so creating new columns to save that data


```python
raw_df['White_id'] = [x['white']['user']['id'] for x in raw_df['players']]
raw_df['White ELO'] = [x['white']['rating'] for x in raw_df['players']]
raw_df['White ELO Change'] = [x['white']['ratingDiff'] for x in raw_df['players']]

raw_df['Black_id'] = [x['black']['user']['id'] for x in raw_df['players']]
raw_df['Black ELO'] = [x['black']['rating'] for x in raw_df['players']]
raw_df['Black ELO Change'] = [x['black']['ratingDiff'] for x in raw_df['players']]
```

- The data is stored in geenral way on basis of color but i want data basis on player so,


```python
raw_df['My ID'] = ''
raw_df['My Rating'] = ''
raw_df['My Rating Change'] = ''

raw_df['Opponent ID'] = ''
raw_df['Opponent Rating'] = ''
raw_df['Opponent Rating Change'] = ''
raw_df['My Color'] = ''
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>Status</th>
      <th>players</th>
      <th>winner</th>
      <th>...</th>
      <th>Black_id</th>
      <th>Black ELO</th>
      <th>Black ELO Change</th>
      <th>My ID</th>
      <th>My Rating</th>
      <th>My Rating Change</th>
      <th>Opponent ID</th>
      <th>Opponent Rating</th>
      <th>Opponent Rating Change</th>
      <th>My Color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>Resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>...</td>
      <td>agustin_perez</td>
      <td>1606</td>
      <td>7</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>1 rows × 32 columns</p>
</div>




```python
raw_df.columns
```




    Index(['Game ID', 'rated', 'variant', 'speed', 'Game Type', 'createdAt',
           'lastMoveAt', 'Status', 'players', 'winner', 'opening', 'moves',
           'clock', 'tournament', 'initialFen', 'Start Time', 'Start Date',
           'End Time', 'End Date', 'White_id', 'White ELO', 'White ELO Change',
           'Black_id', 'Black ELO', 'Black ELO Change', 'My ID', 'My Rating',
           'My Rating Change', 'Opponent ID', 'Opponent Rating',
           'Opponent Rating Change', 'My Color'],
          dtype='object')



- Index of the columns:\
• 'White_id' - 19         • 'White ELO' - 20         • 'White ELO Change' - 21\
• 'Black_id' - 22         • 'Black ELO' - 23         • 'Black ELO Change' - 24\
• 'My ID' - 25            • 'My Rating' - 26         • 'My Rating Change' - 27\
• 'Opponent ID' - 28      • 'Opponent Rating' - 29   • 'Opponent Rating Change' - 30\
• 'My Color' - 31


```python
## Creating a function which will arrange the data on basis of players
def opp_my_distributor(checker, my, white, opp, black):
    for i in range(len(raw_df)):
        if raw_df.iloc[i,checker] == 'yourkingisindanger':
            raw_df.iloc[i,my] = raw_df.iloc[i,white]
            raw_df.iloc[i,opp] = raw_df.iloc[i,black]
            
        else:
            raw_df.iloc[i,my] = raw_df.iloc[i,black]
            raw_df.iloc[i,opp] = raw_df.iloc[i,white]
```


```python
opp_my_distributor(19, 25, 19, 28, 22) ## ID
opp_my_distributor(19, 26, 20, 29, 23) ## Rating
opp_my_distributor(19, 27, 21, 30, 24) ## Rating Change
```


```python
raw_df.loc[raw_df['White_id'] == 'yourkingisindanger', 'My Color'] = 'White'
raw_df.loc[raw_df['Black_id'] == 'yourkingisindanger', 'My Color'] = 'Black'
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>Status</th>
      <th>players</th>
      <th>winner</th>
      <th>...</th>
      <th>Black_id</th>
      <th>Black ELO</th>
      <th>Black ELO Change</th>
      <th>My ID</th>
      <th>My Rating</th>
      <th>My Rating Change</th>
      <th>Opponent ID</th>
      <th>Opponent Rating</th>
      <th>Opponent Rating Change</th>
      <th>My Color</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>Resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>...</td>
      <td>agustin_perez</td>
      <td>1606</td>
      <td>7</td>
      <td>yourkingisindanger</td>
      <td>1659</td>
      <td>-8</td>
      <td>agustin_perez</td>
      <td>1606</td>
      <td>7</td>
      <td>White</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 32 columns</p>
</div>



###### 10. winner


```python
raw_df['winner'].unique()
```




    array(['black', 'white', nan], dtype=object)



- The nan values in winner denotes the matches where the result is Draw


```python
# Making a Result with where i can record if i won, lose or draw.
raw_df.loc[raw_df['My Color'].str.lower() == raw_df['winner'], 'Result'] = "Won"
raw_df.loc[~(raw_df['My Color'].str.lower() == raw_df['winner']), 'Result'] = 'Lose'
raw_df.loc[raw_df['winner'].isna(), 'Result'] = 'Draw'
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>Status</th>
      <th>players</th>
      <th>winner</th>
      <th>...</th>
      <th>Black ELO</th>
      <th>Black ELO Change</th>
      <th>My ID</th>
      <th>My Rating</th>
      <th>My Rating Change</th>
      <th>Opponent ID</th>
      <th>Opponent Rating</th>
      <th>Opponent Rating Change</th>
      <th>My Color</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>Resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>...</td>
      <td>1606</td>
      <td>7</td>
      <td>yourkingisindanger</td>
      <td>1659</td>
      <td>-8</td>
      <td>agustin_perez</td>
      <td>1606</td>
      <td>7</td>
      <td>White</td>
      <td>Lose</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 33 columns</p>
</div>



#### 11. opening


```python
raw_df['opening']
```




    0       {'eco': 'C50', 'name': 'Italian Game: Hungaria...
    1       {'eco': 'C50', 'name': 'Italian Game: Anti-Fri...
    2       {'eco': 'C42', 'name': 'Russian Game: Cozio At...
    3       {'eco': 'E70', 'name': 'King's Indian Defense:...
    4        {'eco': 'B00', 'name': 'Duras Gambit', 'ply': 2}
                                  ...                        
    1223    {'eco': 'C20', 'name': 'King's Pawn Game: Leon...
    1224    {'eco': 'A40', 'name': 'Modern Defense', 'ply'...
    1225    {'eco': 'C41', 'name': 'Philidor Defense', 'pl...
    1226    {'eco': 'A00', 'name': 'Saragossa Opening', 'p...
    1227    {'eco': 'B50', 'name': 'Sicilian Defense: Mode...
    Name: opening, Length: 1212, dtype: object



- It is a Dictionary, so extracting the data using list comprehension


```python
raw_df['Opening ECO'] = [ x['eco'] for x in raw_df['opening']]
raw_df['Opening'] = [ x['name'] for x in raw_df['opening']]
raw_df['Opening Ply'] = [ x['ply'] for x in raw_df['opening']]
```


```python
raw_df['Opening']
```




    0                         Italian Game: Hungarian Defense
    1                  Italian Game: Anti-Fried Liver Defense
    2                              Russian Game: Cozio Attack
    3       King's Indian Defense: Accelerated Averbakh Va...
    4                                            Duras Gambit
                                  ...                        
    1223                King's Pawn Game: Leonardis Variation
    1224                                       Modern Defense
    1225                                     Philidor Defense
    1226                                    Saragossa Opening
    1227                  Sicilian Defense: Modern Variations
    Name: Opening, Length: 1212, dtype: object



- The Opening name consists of the Main name and the variation, I want them seperately So,


```python
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
```


```python
raw_df['Opening Name'] = [seperator(x,0) for x in raw_df['Opening']]
raw_df['Opening Variation'] = [seperator(x,1) for x in raw_df['Opening']]
```


```python
raw_df[['Opening','Opening Name', 'Opening Variation']].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Opening</th>
      <th>Opening Name</th>
      <th>Opening Variation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Italian Game: Hungarian Defense</td>
      <td>Italian Game</td>
      <td>Hungarian Defense</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Italian Game: Anti-Fried Liver Defense</td>
      <td>Italian Game</td>
      <td>Anti-Fried Liver Defense</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Russian Game: Cozio Attack</td>
      <td>Russian Game</td>
      <td>Cozio Attack</td>
    </tr>
    <tr>
      <th>3</th>
      <td>King's Indian Defense: Accelerated Averbakh Va...</td>
      <td>King's Indian Defense</td>
      <td>Accelerated Averbakh Variation</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Duras Gambit</td>
      <td>Duras Gambit</td>
      <td>None</td>
    </tr>
  </tbody>
</table>
</div>



###### 12. moves


```python
raw_df['moves'][0]
```




    'e4 e5 Nf3 Nc6 Bc4 Be7 c3 d6 d4 exd4 cxd4 Bg4 h3 Bxf3 Qxf3 Nf6 Be3 O-O O-O a6 Nc3 b5 Bb3 Na5 Bd5 Nxd5 Nxd5 Nc4 b3 Nxe3 fxe3 Bg5 Rf2 c5 Raf1 f6 g3 Ra7 h4 Bh6 Qf5 Raf7 Kh2 Qd7 Qf3 cxd4 exd4 Qe6 Qf5 Qxf5 Rxf5 a5 g4 Bd2 Kg3 b4 Kf2 g6 Rf3 Kg7 Ke2 Bh6 e5 dxe5 dxe5 fxe5 Rxf7+ Rxf7 Rxf7+ Kxf7 Kd3 Bf8 Ke4 Bd6 Nb6 Ke6 Nc4 Bc7 h5 gxh5 gxh5 Kf6 Kd5 Kf5 Ne3+ Kf4 Nc4 e4 Kd4 Kg5 Kxe4 Kxh5 Kd5 Kg4 Kc6 Bd8 Kb5 h5 Nxa5 Bxa5 Kxa5 h4 Kxb4 h3 a4 h2 a5 h1=Q a6 Qa8 a7 Qxa7 Kc4 Qb6 Kc3'



- a move in chess means 1 by each player so only e4 is half move, e4 e5 is a 1st move


```python
## Calculating No. of Moves
raw_df['No. of Moves'] = [math.ceil(len(x.split())/2) for x in raw_df['moves']]
```


```python
## Extracting first 4 Moves
raw_df['1.0 Move'] = [ x.split()[0]  for x in raw_df['moves']]
raw_df['1.1 Move'] = [ x.split()[1]  for x in raw_df['moves']]
raw_df['2.0 Move'] = [ x.split()[2]  for x in raw_df['moves']]
raw_df['2.1 Move'] = [ x.split()[3]  for x in raw_df['moves']]
```


```python
## Alloting the first 4 moves to players
raw_df.loc[raw_df['My Color'] == 'White', 'M.1'] = raw_df[raw_df['My Color'] == 'White']['1.0 Move']
raw_df.loc[raw_df['My Color'] == 'White', 'M.2'] = raw_df[raw_df['My Color'] == 'White']['2.0 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'M.1'] = raw_df[raw_df['My Color'] == 'Black']['1.1 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'M.2'] = raw_df[raw_df['My Color'] == 'Black']['2.1 Move']

raw_df.loc[raw_df['My Color'] == 'White', 'O.1'] = raw_df[raw_df['My Color'] == 'White']['1.1 Move']
raw_df.loc[raw_df['My Color'] == 'White', 'O.2'] = raw_df[raw_df['My Color'] == 'White']['2.1 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'O.1'] = raw_df[raw_df['My Color'] == 'Black']['1.0 Move']
raw_df.loc[raw_df['My Color'] == 'Black', 'O.2'] = raw_df[raw_df['My Color'] == 'Black']['2.0 Move']
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>Status</th>
      <th>players</th>
      <th>winner</th>
      <th>...</th>
      <th>Opening Variation</th>
      <th>No. of Moves</th>
      <th>1.0 Move</th>
      <th>1.1 Move</th>
      <th>2.0 Move</th>
      <th>2.1 Move</th>
      <th>M.1</th>
      <th>M.2</th>
      <th>O.1</th>
      <th>O.2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>Resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>...</td>
      <td>Hungarian Defense</td>
      <td>58</td>
      <td>e4</td>
      <td>e5</td>
      <td>Nf3</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nc6</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 47 columns</p>
</div>



#### 13. clock


```python
raw_df['clock']
```




    0       {'initial': 300, 'increment': 0, 'totalTime': ...
    1       {'initial': 300, 'increment': 0, 'totalTime': ...
    2       {'initial': 300, 'increment': 0, 'totalTime': ...
    3       {'initial': 300, 'increment': 0, 'totalTime': ...
    4       {'initial': 300, 'increment': 0, 'totalTime': ...
                                  ...                        
    1223    {'initial': 180, 'increment': 0, 'totalTime': ...
    1224    {'initial': 180, 'increment': 0, 'totalTime': ...
    1225    {'initial': 180, 'increment': 0, 'totalTime': ...
    1226    {'initial': 180, 'increment': 0, 'totalTime': ...
    1227    {'initial': 180, 'increment': 0, 'totalTime': ...
    Name: clock, Length: 1212, dtype: object




```python
raw_df['clock'][0]
```




    {'initial': 300, 'increment': 0, 'totalTime': 300}



- Fomating it to the format: 5 Min + 0 Sec


```python
raw_df['Time Control'] = ['{} Min + {} Sec'.format((x['initial']//60), x['increment']) for x in raw_df['clock'] ]
```


```python
raw_df.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>rated</th>
      <th>variant</th>
      <th>speed</th>
      <th>Game Type</th>
      <th>createdAt</th>
      <th>lastMoveAt</th>
      <th>Status</th>
      <th>players</th>
      <th>winner</th>
      <th>...</th>
      <th>No. of Moves</th>
      <th>1.0 Move</th>
      <th>1.1 Move</th>
      <th>2.0 Move</th>
      <th>2.1 Move</th>
      <th>M.1</th>
      <th>M.2</th>
      <th>O.1</th>
      <th>O.2</th>
      <th>Time Control</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>True</td>
      <td>standard</td>
      <td>blitz</td>
      <td>Blitz</td>
      <td>2022-06-14 18:50:41</td>
      <td>2022-06-14 19:00:45</td>
      <td>Resign</td>
      <td>{'white': {'user': {'name': 'YourKingIsInDange...</td>
      <td>black</td>
      <td>...</td>
      <td>58</td>
      <td>e4</td>
      <td>e5</td>
      <td>Nf3</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>5 Min + 0 Sec</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 48 columns</p>
</div>



###### 14. tournament


```python
raw_df['tournament'].unique()
```




    array([nan, '7qLQnyrI', 'Kbq6hs06', '1NUtWJEq', 'Z1JJNSIj', 'UZu3qGKo',
           'ZYV0J6y4', 'r6oTBiYG', 'IPqQZGlp', 'lkwODJck', 'DBEYi5oB',
           'llRxupSK', 'VA9FDXDc', '90ubk1Kc', 'VCDjG9zz', 'K52V3lsw',
           'fkaxbE7M', 'bSUXiKLg', 'nJIzx6gv', '2VuIsji8', 'Ah8UZJ0q',
           'KEGrsI1X', 'FDpULmSl', 'iNaKmb1Q', 'tMjwUbJy', 'S0b6Su1w',
           'j4gzLrhD', 'DCqdT9XM', 'KiqK3dw9', 'IS972gpN', 'auAEb8Ea',
           'FcsYKtz3', 'M8Y2wNS0', 'uYI0yFDk', 'eeez5QYn', 'sCVzW92g',
           '0mScIt6f', 'DKBjiyqb', 'i1AeUK1a', 'iL1zBh0t', 'snbdoMJL',
           'iPdbatnK', 'r5FgKQae', 'PhPhROoO', 'qkib6R1a', 'HgCyVikw',
           'YYVetI00', 'CXHLrLsZ', 'kARcOy6S', 'xxu91IZP', 'Cix3nOtA',
           '6gzzLiBH', 'tM1o9SZB', 'AWI8SOSG', 'ln53skXN', 'fY3JY2yM',
           'hRoPjUvq', 'pSWL0meH', 'HyA1mM4y'], dtype=object)



So, if the game is played in a tournament it has a tournamnt id Where else there is None, so we'll make two columns,
1. Tournament Game - bool type
2. Tournament Id - str type


```python
raw_df.loc[raw_df['tournament'].isna(), 'Tournament Game'] = False
raw_df.loc[~(raw_df['tournament'].isna()), 'Tournament Game'] = True
```


```python
raw_df.rename(columns = {'tournament':'Tournament ID'}, inplace = True)
```

###### 15. initialFen


```python
raw_df['initialFen'].unique()
```




    array([nan], dtype=object)



It has nothing


```python
## Taking our Usefull Variables in a new Dataframe
```


```python
raw_df.columns
```




    Index(['Game ID', 'rated', 'variant', 'speed', 'Game Type', 'createdAt',
           'lastMoveAt', 'Status', 'players', 'winner', 'opening', 'moves',
           'clock', 'Tournament ID', 'initialFen', 'Start Time', 'Start Date',
           'End Time', 'End Date', 'White_id', 'White ELO', 'White ELO Change',
           'Black_id', 'Black ELO', 'Black ELO Change', 'My ID', 'My Rating',
           'My Rating Change', 'Opponent ID', 'Opponent Rating',
           'Opponent Rating Change', 'My Color', 'Result', 'Opening ECO',
           'Opening', 'Opening Ply', 'Opening Name', 'Opening Variation',
           'No. of Moves', '1.0 Move', '1.1 Move', '2.0 Move', '2.1 Move', 'M.1',
           'M.2', 'O.1', 'O.2', 'Time Control', 'Tournament Game'],
          dtype='object')




```python
Chess_df = raw_df[['Game ID', 'Start Date','Start Time', 'End Date', 'End Time', 'Game Type',
        'Time Control', 'Tournament Game', 'Tournament ID', 'createdAt', 'lastMoveAt',
        'My ID', 'My Rating', 'My Rating Change', 'My Color',
        'Opponent ID', 'Opponent Rating', 'Opponent Rating Change', 'Status',  'Result',
        'Opening ECO', 'Opening Ply', 'Opening', 'Opening Variation', 
        'No. of Moves', '1.0 Move', '1.1 Move', '2.0 Move', '2.1 Move', 
        'M.1', 'M.2', 'O.1', 'O.2']].copy()
```


```python
Chess_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>Start Date</th>
      <th>Start Time</th>
      <th>End Date</th>
      <th>End Time</th>
      <th>Game Type</th>
      <th>Time Control</th>
      <th>Tournament Game</th>
      <th>Tournament ID</th>
      <th>createdAt</th>
      <th>...</th>
      <th>Opening Variation</th>
      <th>No. of Moves</th>
      <th>1.0 Move</th>
      <th>1.1 Move</th>
      <th>2.0 Move</th>
      <th>2.1 Move</th>
      <th>M.1</th>
      <th>M.2</th>
      <th>O.1</th>
      <th>O.2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>2022-06-14</td>
      <td>18:50:41</td>
      <td>2022-06-14</td>
      <td>19:00:45</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-14 18:50:41</td>
      <td>...</td>
      <td>Hungarian Defense</td>
      <td>58</td>
      <td>e4</td>
      <td>e5</td>
      <td>Nf3</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nc6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CwbVPlQf</td>
      <td>2022-06-12</td>
      <td>14:46:40</td>
      <td>2022-06-12</td>
      <td>14:52:41</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-12 14:46:40</td>
      <td>...</td>
      <td>Anti-Fried Liver Defense</td>
      <td>33</td>
      <td>e4</td>
      <td>e5</td>
      <td>Bc4</td>
      <td>Nc6</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Bc4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>v4Jyr7UC</td>
      <td>2022-06-12</td>
      <td>14:39:05</td>
      <td>2022-06-12</td>
      <td>14:46:28</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-12 14:39:05</td>
      <td>...</td>
      <td>Cozio Attack</td>
      <td>26</td>
      <td>e4</td>
      <td>e5</td>
      <td>Nf3</td>
      <td>Nf6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nf6</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Fs56klNV</td>
      <td>2022-06-11</td>
      <td>21:07:25</td>
      <td>2022-06-11</td>
      <td>21:16:46</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-11 21:07:25</td>
      <td>...</td>
      <td>Accelerated Averbakh Variation</td>
      <td>36</td>
      <td>d4</td>
      <td>g6</td>
      <td>e4</td>
      <td>Bg7</td>
      <td>g6</td>
      <td>Bg7</td>
      <td>d4</td>
      <td>e4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>jv5yaYp9</td>
      <td>2022-06-10</td>
      <td>02:19:50</td>
      <td>2022-06-10</td>
      <td>02:28:04</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-10 02:19:50</td>
      <td>...</td>
      <td>None</td>
      <td>27</td>
      <td>e4</td>
      <td>f5</td>
      <td>exf5</td>
      <td>Kf7</td>
      <td>e4</td>
      <td>exf5</td>
      <td>f5</td>
      <td>Kf7</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 33 columns</p>
</div>



# Creating Calculated Fields

###### New Rating


```python
Chess_df['My New Rating'] = Chess_df['My Rating'] + Chess_df['My Rating Change']
```


```python
Chess_df.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>Start Date</th>
      <th>Start Time</th>
      <th>End Date</th>
      <th>End Time</th>
      <th>Game Type</th>
      <th>Time Control</th>
      <th>Tournament Game</th>
      <th>Tournament ID</th>
      <th>createdAt</th>
      <th>...</th>
      <th>No. of Moves</th>
      <th>1.0 Move</th>
      <th>1.1 Move</th>
      <th>2.0 Move</th>
      <th>2.1 Move</th>
      <th>M.1</th>
      <th>M.2</th>
      <th>O.1</th>
      <th>O.2</th>
      <th>My New Rating</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>2022-06-14</td>
      <td>18:50:41</td>
      <td>2022-06-14</td>
      <td>19:00:45</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-14 18:50:41</td>
      <td>...</td>
      <td>58</td>
      <td>e4</td>
      <td>e5</td>
      <td>Nf3</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>1651</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CwbVPlQf</td>
      <td>2022-06-12</td>
      <td>14:46:40</td>
      <td>2022-06-12</td>
      <td>14:52:41</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-12 14:46:40</td>
      <td>...</td>
      <td>33</td>
      <td>e4</td>
      <td>e5</td>
      <td>Bc4</td>
      <td>Nc6</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Bc4</td>
      <td>1659</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 34 columns</p>
</div>



##### Time Interval


```python
for i in range(24):
    Chess_df.loc[(datetime.time(i,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(i,59,59)), 'Time Interval'] = \
            '{} {} - {} {}'.format(12 if i == 0 else i if i < 13 else i-12, 'AM' if i < 12 else 'PM', 
                                   i+1 if i+1 < 13 else i+1 - 12, 'AM' if i==23 else 'AM' if i+1 < 12 else 'PM')
```

###### Day Time

• 4AM - 7AM : Early Morning\
• 7AM - 9AM : Morning\
• 9AM - 12AM : Late Morning\
• 12AM - 3AM : Afternooon\
• 3AM - 5AM : Late Afternoon\
• 5AM - 7AM : Early Evening\
• 7AM - 9AM : Evening\
• 9AM - 11AM : Late Evening\
• 11AM - 2AM : Night\
• 2AM - 4AM : Late night


```python
Chess_df.loc[(datetime.time(0,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(1,59,59)), 'Day Time'] = 'Night'

Chess_df.loc[(datetime.time(2,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(3,59,59)), 'Day Time'] = 'Late Night'

Chess_df.loc[(datetime.time(4,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(6,59,59)), 'Day Time'] = 'Early Morning'

Chess_df.loc[(datetime.time(7,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(8,59,59)), 'Day Time'] = 'Morning'

Chess_df.loc[(datetime.time(9,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(11,59,59)), 'Day Time'] = 'Late Morning'

Chess_df.loc[(datetime.time(12,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(14,59,59)), 'Day Time'] = 'Afternoon'

Chess_df.loc[(datetime.time(15,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(16,59,59)), 'Day Time'] = 'Late Afternoon'

Chess_df.loc[(datetime.time(17,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(19,59,59)), 'Day Time'] = 'Early Evening'

Chess_df.loc[(datetime.time(19,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(20,59,59)), 'Day Time'] = 'Evening'

Chess_df.loc[(datetime.time(21,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(22,59,59)), 'Day Time'] = 'Late Evening'

Chess_df.loc[(datetime.time(23,0,0) < Chess_df['Start Time']) & \
        (Chess_df['Start Time'] < datetime.time(23,59,59)), 'Day Time'] = 'Night'
```

##### Game Stage

0-15 Moves - Opening\
16-49 Moves - MidGame\
50+ Moves - EndGame



```python
Chess_df.loc[Chess_df['No. of Moves'] <= 15, 'Game Stage'] = 'Opening'
Chess_df.loc[(Chess_df['No. of Moves'] >= 16) &\
             (Chess_df['No. of Moves'] <= 49), 'Game Stage'] = 'Middlegame'
Chess_df.loc[Chess_df['No. of Moves'] >= 50, 'Game Stage'] = 'Endgame'
```

###### Is Rating Difference More Than Me


```python
Chess_df.loc[(Chess_df['Opponent Rating'] - Chess_df['My Rating']) > 0, 
             'Rating Difference More Than Me'] = True

Chess_df.loc[(Chess_df['Opponent Rating'] - Chess_df['My Rating']) <= 0, 
             'Rating Difference More Than Me'] = False
```

# Saving The File


```python
Chess_df.to_csv('Chess_df.csv')
```


```python
Chess_df.head(2)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Game ID</th>
      <th>Start Date</th>
      <th>Start Time</th>
      <th>End Date</th>
      <th>End Time</th>
      <th>Game Type</th>
      <th>Time Control</th>
      <th>Tournament Game</th>
      <th>Tournament ID</th>
      <th>createdAt</th>
      <th>...</th>
      <th>2.1 Move</th>
      <th>M.1</th>
      <th>M.2</th>
      <th>O.1</th>
      <th>O.2</th>
      <th>My New Rating</th>
      <th>Time Interval</th>
      <th>Day Time</th>
      <th>Game Stage</th>
      <th>Rating Difference More Than Me</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>qnrlibcn</td>
      <td>2022-06-14</td>
      <td>18:50:41</td>
      <td>2022-06-14</td>
      <td>19:00:45</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-14 18:50:41</td>
      <td>...</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Nf3</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>1651</td>
      <td>6 PM - 7 PM</td>
      <td>Early Evening</td>
      <td>Endgame</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CwbVPlQf</td>
      <td>2022-06-12</td>
      <td>14:46:40</td>
      <td>2022-06-12</td>
      <td>14:52:41</td>
      <td>Blitz</td>
      <td>5 Min + 0 Sec</td>
      <td>False</td>
      <td>NaN</td>
      <td>2022-06-12 14:46:40</td>
      <td>...</td>
      <td>Nc6</td>
      <td>e5</td>
      <td>Nc6</td>
      <td>e4</td>
      <td>Bc4</td>
      <td>1659</td>
      <td>2 PM - 3 PM</td>
      <td>Afternoon</td>
      <td>Middlegame</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 38 columns</p>
</div>


