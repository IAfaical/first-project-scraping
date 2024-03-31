from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

from detoxify import Detoxify
from fastapi.responses import JSONResponse

import pandas as pd
from scraping.model import FacebookPost

from src.scraping import scrape_posts


app=FastAPI()


#connection to Mongodb 
client = MongoClient('mongodb://mongo:27017/')
db= client['mongo_db']
collection=db['facebook_posts']

#scrap-post function 

@app.post("/scrap-and-insert/")
async def scraping_post(url:str,cookie:str):
       posts= scrape_posts(url,cookie)  

       post_dataframe=pd.DataFrame(posts,columns=['content'])
       
       #large Model for the prediction of toxicity   
       results= Detoxify('original').predict(posts)
       print('toxicity prediction', results) 

       for i,(key,values) in enumerate(results.items):
               post_dataframe.insert(i+1,key, values,True)
       
       inserted_ids=[]
       for index, row in post_dataframe.iterrows():
              row_dic= row.to_dict()
              facebook_post=FacebookPost(**row_dic)

        
             #insertion on the mongodb collection
              inserted_posts = collection.insert_one(facebook_post.dict())
              inserted_ids.append(str(inserted_posts.inserted_id))
                       
       return {"inserted_ids": inserted_ids ,"message":"post scraped and inserted"}           
       



#get posts from mongo database 
@app.get('/posts/')
async def get_posts():
       posts = list(collection.find({},{"_id":0}))
       for post in posts:
           if '_id' in post:
            post['id']= str(post['id'])
    
       return JSONResponse(content=posts)