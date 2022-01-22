#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
import csv

# In[4]:

st.set_page_config(layout="wide")
st.title("KW Tagging/Labelling")
st.sidebar.header("What's this tool about?")
st.sidebar.write('''
		Clustering Keywords into larger buckets among a number of defined dimensions allows to uncover
		broaders trends and visualise these more easily. This script is nothing more than a thought starter for those interested,
		taking a .xlsx file with 2 tabs as input
		
		- tab1: list or table. 1 column should contain a list of KW with a column header of "keyword".
		Additional columns with labels you may already have can be added
		
		- tab2: table of tags. Column header should be group (e.x. Gender, Products...). Values underneath should be characteristics (e.x. Men, Women's,)
		
		Output is a .csv file with the keywords being labelled. This happens based on a simple reverse-search labeling the keywords if the tag characteristic is present in the keywords
			
		''')
st.sidebar.image("https://i.ibb.co/hRV5Gmt/eee.png")
#st.sidebar.markdown("![Output Example](https://i.ibb.co/hRV5Gmt/eee.png)")

st.image("https://s10.gifyu.com/images/demo42141da877a812d4.gif")

upload = st.file_uploader("Upload List of crawled URLs", type=["xlsx"])
st.info("Upload a XLSX file as per description in the sidebar") 

if upload is not None:

	keywords = pd.read_excel(upload, sheet_name=0, converters={'keyword':str})
	tags = pd.read_excel(upload, sheet_name=1)
	cols = tags.columns

	# ---- create lists for categorisation

	catLst = []

	for i in cols:
		cat = tags[i]
		cat = [ i.strip() for i in cat if str(i) != 'nan' ]
		catLst.append(cat)

 	# ---- check if list value is in kw, if TRUE, value is used as category label 

	for i in range(len(cols)):
		keywords[cols[i]] = keywords['keyword'].str.title().str.findall(fr"(?i)\b({'|'.join(sorted(catLst[i],key=len,reverse=True))})\b").progress_apply(','.join)

	mapping = {
    
  		"Men's":"Men",
  		"Men'S":"Men",
  		"Mens": "Men",
  		"Womens":"Women",
  		"Women's":"Women",
  		"Women'S":"Women",
  		"Ladies":"Women",
  		"Children":"Kids",
  		"Boy":"Boys",
  		"Girl":"Girls",
  		"Infant":"Kids",
  		"Toddlers":"Kids",
  		"Toddler":"Kids",
  		"Infants":"Kids",
  		"Babies":"Kids",
  		"Baby":"Kids"

	}

	if "gender" in cols:
	
		keywords["gender"] = keywords["gender"].replace(mapping)
    
	st.table(keywords)
	csv = keywords.to_csv().encode('utf-8')
	st.download_button(
    	label="Download table as CSV",
    	data=csv,
    	file_name='kws_tagged.csv',
    	mime='text/csv')
