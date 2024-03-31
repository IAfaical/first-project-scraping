import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
import pandas as pd


def scrape_posts(url: str = 'https://mbasic.facebook.com/groups/526003374274383/?hoisted_section_header_type=recently_seen&multi_permalinks=2353777014830334', cookie : str):
    try:
        # Send a GET request to the URL with the account cookie
        response = requests.get(url, headers={'cookie':cookie})
        # extrqct content from html page : p div with id m_group_stories_container
        list_posts = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.find('div',id='m_group_stories_container').find_all('p')
            for post in posts:
                post_content = post.get_text()
                list_posts.append(post_content)
        return list_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape posts: {str(e)}")


  #creation dataframe 
  #posts_dataframe=pd.DataFrame(list_posts, columns=['content'])


  #get the large Model to predict the toxicity in the post_content 
 # from detoxify import Detoxify 
  #results = Detoxify('original').predict(list_posts)
  #print(results)

  #for i,(key,values) in results.items():
  #   posts_dataframe(i+1,key,values,True)  

