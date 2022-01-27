#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
import csv
import xlrd
import json

# In[4]:

st.set_page_config(layout="wide")
st.title("KW Tagging/Labelling")
st.sidebar.header("What's this tool about?")
st.sidebar.write('''
		Clustering Keywords into larger buckets among a number of defined dimensions allows to uncover
		broader trends and visualise these more easily. This script is nothing more than a thought starter for those interested,
		taking a .xlsx file with 2 tabs as input
		
		- **Tab 1**: list or table. 1 column should contain a list of KW with a column header of **keyword**.
		Additional columns with labels you may already have can be added
		
		- **Tab 2**: list or table of tags. Column header should be group (e.x. `gender`, `products`,...). Values underneath should be characteristics (e.x. Men, Women's,...)
		Make sure to also add plurals, term variations and/or synonyms you want to be found. In particular if you use the advanced feature of uploading your own map (see bottom of sidebar) 
		
		Output is a .csv file with the keywords being labelled. This happens based on a simple reverse-search labeling the keywords if the tag characteristic is present in the keywords
			
		''')
st.sidebar.image("https://i.ibb.co/hRV5Gmt/eee.png")
with st.sidebar.expander("Upload your own mapping (advanced)"):
	st.write('''Why would you upload you custom mapping?
				Keywords are not always as structured and linear as we would want them to be. Term Variations (Womens, Women's, Women), Singular/Plurals (Girl, Girls) or Synonyms (Ladies, Women) 
				can lead for simple reverse search results to be incomplete. With a [custom mapping](https://s10.gifyu.com/images/ezgif.com-gif-maker-1136ff9593a918186.gif) you can account for it as your endeavour requires it and group these together under a single label. 
				The custom mapping should be a JSON file where keys represent the Tag Groups (e.x. `gender`, `products`, ...) from the Excel upload. Values are word pairs you want group.
				E.x.: if keyword contains "Ladies", tag as "Women". See example Schema below.
			''') 
	mapping = st.file_uploader("Upload JSON file", type=["json"])
	if mapping is not None:
		mapping = json.load(mapping)

	st.info("Please ensure (level 1) keys match the Excel Tag Group names (ex. gender, products,...)")
	st.write("Example of JSON schema")
	st.json('''
					{"gender":
						{"Womens":"Women","Women's":"Women","Ladies":"Women"},
					"products":
						{"Shoe":"Shoes","Pants":"Trousers"}
					}
				'''
				)

st.image("https://s10.gifyu.com/images/demo42141da877a812d4.gif")

upload = st.file_uploader("Upload File", type=["xlsx"])
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
		
		if mapping is not None:
			try:
				col_map = mapping.get(cols[i])
				col_map = { k.capitalize():v.capitalize() for k,v in col_map.items() }
				keywords[cols[i]] = keywords[cols[i]].replace(col_map)
				#st.write(col_map)
			except AttributeError:
				pass
			
	st.table(keywords)
	
	csv = keywords.to_csv().encode('utf-8')
	st.download_button(
    	label="Download table as CSV",
    	data=csv,
    	file_name='kws_tagged.csv',
    	mime='text/csv')

