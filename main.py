from bs4 import BeautifulSoup
import requests,xlsxwriter
import pandas as pd
import os
from UliPlot.XLSX import auto_adjust_xlsx_column_width
from pathlib import Path
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Getting the html file from the server
html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text
soup = BeautifulSoup(html_text,'lxml')

#Getting all the jobs with python experience (search for python)
jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')

#Creating pandas dataframe
column_names = ["Company name", "Skills", "Published date","Link"]
df = pd.DataFrame(columns=column_names)

#Counter for indexing in df
counter = 0

#Getting the information from every job
for job in jobs:
    lst = []
    company_name = job.find('h3',class_='joblist-comp-name').text.replace('\r','').replace('\n','').strip()
    skills = job.find('span',class_='srp-skills').text.replace('\r','').replace('\n','').strip()
    pub_date = job.find('span',class_='sim-posted').text.replace('\r','').replace('\n','').strip()
    link = job.find('a').get('href')

    #Writing the info to the dataframe
    df.loc[counter,'Company name'] = company_name
    df.loc[counter,'Skills'] = skills
    df.loc[counter,'Published date'] = pub_date
    df.loc[counter,'Link'] = link

    #Incrementing the counter for next job
    counter += 1

#Creating the excel file
workbook = xlsxwriter.Workbook('Jobs.xlsx')
worksheet = workbook.add_worksheet()
workbook.close()

#Exporting the dataframe in excel file with auto adjusting excel columns
with pd.ExcelWriter("Jobs.xlsx") as writer:
    df.to_excel(writer, sheet_name="MySheet")
    auto_adjust_xlsx_column_width(df, writer, sheet_name="MySheet", margin=0)

#Opneing the excel file
absolutePath = Path('Jobs.xlsx').resolve()
os.system(f'start Jobs.xlsx "{absolutePath}"')




