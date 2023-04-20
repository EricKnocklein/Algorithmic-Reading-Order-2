import json
import os
import re

article_nodes = {}  # holds all the information about all the articles
names_dict = {}  # mapping of article ID to article name
ignored_dirs = []  # holds folders that we to ignore in this analysis

# the directory that holds the articles in relation to the location of the code
directory = "2022-09-15T19_17-export/worlds/Telluriam/articles"


def get_articles(name):
    for article in os.scandir(name):
        article_path = os.fsdecode(article)
        if os.path.isdir(article_path):  # if the current object is another folder
            if article_path[article_path.rfind("\\") + 1:] not in ignored_dirs: # filter out ignored folders
                get_articles(article_path) # recurse on sub-folder
        elif article_path.endswith(".json") and not article_path.endswith("metadata.json"):  # filter non-articles
            f = open(article_path, "r", encoding="utf8")  # open file with read permission
            current_article = json.load(f)  # get the json as a dictionary
            current_article_txt = str(current_article)  # convert ^ to string
            f.close()  # close the file
            article_name = current_article["title"]  # extract the name of the article
            article_id = current_article["id"]  # extract the id of the article
            linked_ids = re.findall(r'data-article-id="(.*?)"', current_article_txt)  # scan text for links
            article_nodes[article_id] = {
                "name": article_name,
                "word_count": current_article["wordcount"],
                "links": linked_ids,
                "directory": re.findall(r'articles\\(\w*)', name)[0]
            }  # save all the information we need
            names_dict[article_id] = article_name  # save the name of the article


get_articles(directory)  # call the function on the desired directory

# save the dictionaries to text files
json.dump(article_nodes, open("article_nodes.txt", "w"))
json.dump(names_dict, open("names_dict.txt", "w"))
