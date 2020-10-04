#!/usr/bin/env python
# coding: utf-8

# In[264]:


import pandas as pd
from datetime import datetime
from datetime import date
from flask import Flask, request, render_template
import calendar


# In[265]:

app = Flask(__name__)

import csv
from nltk import tokenize
import nltk
stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

# In[266]:

data = pd.read_csv("conf-finalfile-cons.csv", sep=",")


# In[267]:


inverted_idx = {}
# convert date 
new = data["date"].str.split("-", n = 1, expand = True)
data["Start Date"] = new[0]
data["End Date"] = new[1]



# In[269]:


data["Start Date"] = data["Start Date"].str.strip()
data["End Date"] = data["End Date"].str.strip()


# In[270]:


start_date_split = data["Start Date"].str.split(" ", n = -1, expand = True)
end_date_split = data["End Date"].str.split(" ", n= -1, expand= True)
data["Start Weekday"] = start_date_split[0]
data["Start Day"] = start_date_split[1]
data["Start Month"] = start_date_split[2]
data["Start Year"] = start_date_split[3]
data["End Weekday"] = end_date_split[0]
data["End Day"] = end_date_split[1]
data["End Month"] = end_date_split[2]
data["End Year"] = end_date_split[3]



# In[272]:


new_data = data 
month = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
for i, row in new_data.iterrows():
    
    if row['Start Day'] in month:
        
        m = row['Start Day']
        n = row['Start Month']
        row['Start Month'] = m
        row['Start Day'] = n

    
       


# In[273]:


for i, r in new_data.iterrows():
    
    if row['End Date'] is not None:
        if row['End Month'] == "Nov":
            row['End Year'] = "2019"
        if row['End Month'] == "Dec":
            row['End Year'] = "2019"
        if row['End Month'] == "Jan":
            row['End Year'] = "2020"
        if row['End Month'] == "Feb":
            row['End Year'] = "2019"
 

    


# In[274]:


for i, row in new_data.iterrows():
    if row['city'] == 'NY':
        row['city'] = "New York"
        
    if row['Start Month'] is None:
        row['Start Month'] = row['End Month']  


# In[275]:


for i, row in new_data.iterrows():
    
    if row['Start Year'] is None:
        if row['End Year'] is None:
            if row['Start Month'] == 'Nov':
                row['Start Year'] = "2019"
            if row['Start Month'] == "Dec":
                row['Start Year'] = "2019"
            if row['Start Month'] == "Jan":
                row['Start Year'] = "2020"
            if row['Start Month'] == "Feb":
                row['Start Year'] = "2019"
        else:
            row['Start Year'] = row['End Year'] 




# In[278]:


new_data.replace(to_replace=[None], value="", inplace=True)


# In[279]:


new_data['start'] = new_data[['Start Day', 'Start Month', 'Start Year']].apply(lambda x : " ".join(x), axis=1)


# In[280]:


new_data['end'] = new_data[['End Day', 'End Month', 'End Year']].apply(lambda x : " ".join(x), axis=1)


# In[282]:


new_data['end'] = new_data['end'].str.strip()


# In[283]:


new_data.replace(to_replace="", value=0 , inplace=True)


# In[284]:


new_data['st']=pd.to_datetime(new_data['start'], errors='coerce')


# In[285]:


new_data['ed']=pd.to_datetime(new_data['end'], errors='coerce')

df = pd.DataFrame(data=new_data)

# remove stop words
def remove_stop_words(words):
    filtered = []
    #word = words.split() 
    for r in words: 
        if not r in stopwords:
            filtered.append(r)
    return filtered
def get_text_ready(text):
    #tockenize
    tokens = nltk.word_tokenize(text)
    #remove stop words 
    tokens = remove_stop_words(tokens)
    #normalize
    tokens = [word.lower() for word in tokens]
    return tokens


# In[292]:


#text_corpus = []
with open('conf-finalfile-cons.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    for i, row in enumerate(reader):
        text = " ".join([row[1], row[4]])
        filt = get_text_ready(text)   
        for word in filt:
            if word not in inverted_idx:
                inverted_idx[word] = []
            if i not in inverted_idx[word]:
                inverted_idx[word].append(i)


# In[293]:


def retrive(doc, location, time1, time2):
    text = []
    for index, row in df.iterrows():
        if location == "Any Location":
            if doc == index:
                if row['st'] >= time1 and row['st'] <= time2:
                    text = [row.st,row.ed , row.title, row.venue, row.city, row.description, row.start, row.end]
        else:
            if doc == index and row['city'] == location:
                if row['st'] >= time1 and row['st'] <= time2:
                    text = [row.st,row.ed , row.title, row.venue, row.city, row.description, row.start, row.end]
            
    return text




# In[297]:


def search(query, location, time1, time2):
    date_time_obj1 = datetime.strptime(time1, '%Y-%m-%d')
    t1 = date_time_obj1.date()
    date_time_obj2 = datetime.strptime(time2, '%Y-%m-%d')
    t2 = date_time_obj2.date()
    result = []
    for word in get_text_ready(query):
        if word in inverted_idx:
            doc_number = inverted_idx[word]
            for i in doc_number:
                ret = retrive(i, location, t1, t2)
                if ret: 
                    result.append(ret)
    if not result:
        result = 0
        final_list = result
        
    else:
        res = pd.DataFrame(data = result)
        res = res.sort_values(by = 0)  
    
        final_list = res.values.tolist()

    return final_list             
   
@app.route('/')
def index():
    query = request.args.get("query", None)
    city = request.args.get("city", None)
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    if city:
        print(city + str(type(city)))
        loclist =["Any Location", "New York", "Jersey City", "Newark"]
        loclist.remove(city)
    if query:
        if not start_date:
            start_date = str(date.today())
        if not end_date:
            this_year = int(start_date.split('-')[0])
            end_date = start_date.replace(str(this_year), str(this_year+1))
        app.logger.info("Query {} received".format(query))
        st_year = str(start_date).split("-")[0]
        st_month = calendar.month_abbr[int(str(start_date).split("-")[1])]
        st_day = str(int(str(start_date).split("-")[2]))
        st_date = st_month + " " + st_day + " " + st_year
        en_year = str(end_date).split("-")[0]
        en_month = calendar.month_abbr[int(str(end_date).split("-")[1])]
        en_day = str(int(str(end_date).split("-")[2]))
        en_date = en_month + " " + en_day + " " + en_year
        if en_date == st_date:
            check = "on"
        else:
            check = "between"
        results = search(query, city, start_date, end_date)
        return render_template('results.html', query=query, results=results, city=city, en_date=en_date, st_date=st_date, check=check, start_date=start_date,end_date=end_date, loclist=loclist)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
