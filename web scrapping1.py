
# The urllib.request module is used to open URLs. The Beautiful Soup package is used to extract data from html files.
# The Beautiful Soup library's name is bs4 which stands for Beautiful Soup, version 4.
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://www.hubertiming.com/results/2017GPTR10K"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
type(soup)

# Get the title
title = soup.title
print(title)

# Print out the text
text = soup.get_text()
#print(soup.text)

#how to extract all the hyperlinks within the webpage.
soup.find_all('a')

#get('"href") method to extract and print out only hyperlinks.
all_links = soup.find_all("a")
for link in all_links:
    print(link.get("href"))

#To print out table rows only, pass the 'tr' argument in soup.find_all().
rows = soup.find_all('tr')
print(rows[:10])

#our aim is to take a table from a webpage and convert it into a dataframe for easier manipulation using Python.
for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)

#remove html tags
# Pass the string of interest into BeautifulSoup() and use the get_text() method to extract the text without html tags.
str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)

#After compiling a regular expression, you can use the re.sub() method to find all the substrings where the regular expression matches and replace
# them with an empty string. The full code below generates an empty list, extract text in between html tags for each row, and append it to the assig

import re
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame(list_rows)
df.head(10)

#Data Manipulation and Cleaning
#split the "0" column into multiple columns at the comma position.
df1 = df[0].str.split(',', expand=True)
df1.head(10)

#strip() method to remove the opening square bracket on column "0."
df1[0] = df1[0].str.strip('[')
df1.head(10)

#The table is missing table headers. we can use the find_all() method to get the table headers.
col_labels = soup.find_all('th')

#extract text in between html tags for table headers.
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)

#convert the list of headers into a pandas dataframe.
df2 = pd.DataFrame(all_header)
df2.head()

#split column "0" into multiple columns at the comma position for all rows.
df3 = df2[0].str.split(',', expand=True)
df3.head()

#The two dataframes can be concatenated into one using the concat() method
frames = [df3, df1]
df4 = pd.concat(frames)
df4.head(10)

df5 = df4.rename(columns=df4.iloc[0])
df5.head()

# Overview of the data.
df5.info()
df5.shape

#The table has 597 rows and 14 columns. drop all rows with any missing values.
df6 = df5.dropna(axis=0, how='any')

#table header is replicated as the first row in df5. It can be dropped
df7 = df6.drop(df6.index[0])
df7.head()

# renaming columns
df7.rename(columns={'[Place': 'Place'},inplace=True)
df7.rename(columns={' Team]': 'Team'},inplace=True)
df7.head()

#The final data cleaning step involves removing the closing bracket for cells in the "Team" column.
df7['Team'] = df7['Team'].str.strip(']')
df7.head()


# Data Analysis and Visualization

#The first question to answer is, what was the average finish time (in minutes) for the runners? You need to convert the column "Chip Time" into just minutes.
# One way to do this is to convert the column to a list first for manipulation.

time_list = df7[' Chip Time'].tolist()
# You can use a for loop to convert 'Chip Time' to minutes
time_mins = []
for i in time_list:
    if(len(i)==6):
        m, s = i.split(':')
        math = round(((int(m) * 60 + int(s)) / 60),2)
    else:
        h, m, s = i.split(':')
        math = round(((int(h) * 3600 + int(m) * 60 + int(s))/60),2)
    time_mins.append(math)
#print(time_mins)

#The next step is to convert the list back into a dataframe and make a new column ("Runner_mins") for runner chip times expressed in just minutes.
df7['Runner_mins'] = time_mins
df7.head()

#calculate statistics for numeric columns only in the dataframe.
df7.describe(include=[np.number])

#visualize summary statistics (maximum, minimum, medium, first quartile, third quartile, including outliers)
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5

df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
qplt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])

#The second question to answer is: Did the runners' finish times follow a normal distribution?
x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()

#The third question deals with whether there were any performance differences between males and females of various age groups.
f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']==' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()

#The distribution indicates that females were slower than males on average.
g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)

#The average chip time for all females and males was ~66 mins and ~58 mins, respectively. Below is a side-by-side boxplot comparison of male and female finish times.
df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")



