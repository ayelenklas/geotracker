import pandas as pd
import json
import glob
import os

FIELDS = ["position", "title", 
                    "category/title", "vicinity", 
                    "tags", "openingHours/text"]

class Transformer():

    def __init__(self, csvfolder, jsonfolder):
        self.csvfolder = csvfolder
        self.jsonfolder = jsonfolder

    def json_to_df(self, *params):
    #give directory name and encode it for iteration
        directory = os.fsencode(self.jsonfolder)

        def split_title_tags(tags):
            # handle empty tags
            if isinstance(tags.tags, float):
                return {'tag_0': None}

            # use set to avoid duplicate
            titles = set()
            
            # get title for each tag, add to set
            for tag in tags.tags:
                titles.add(tag.get('title'))

            # return as dictionary for column names
            return {f'tag_{i}':title for i,title in enumerate(titles)}

        #iterate
        for i, file in enumerate(os.listdir(directory)):
            
            #give file a iterable name
            filename = os.fsdecode(file)
            
            if filename.endswith(".json"):
                
                #open file
                with open(f"../jsondumps/{filename}") as f:
                    j = json.load(f)
                    
                if len(j["results"]["items"]) == 0:
                    continue
                    
                #process
                df = pd.json_normalize(j["results"]["items"], errors="ignore", sep="/")
                    
                try:
                    df_new = df[FIELDS]
                except KeyError:
                    tmp = FIELDS.remove("openingHours/text")
                    df_new = df[tmp] # TODO REMOVE HARDCODING
                    
                appiled_df = df_new[['tags']].apply(split_title_tags, axis=1, result_type='expand')

                # append split dataframe to original datafram            
                df_full = pd.concat([df_new, appiled_df], axis=1)\
                .drop(columns=["tags"])

                # dump
                df_full.to_csv(f"{self.csvfolder}/data_{i}.csv", index=False, header=True, errors="ignore")

    def csv_merger(self, extension):
        
        os.chdir(self.csvfolder)
        all_filenames = [e for e in glob.glob('*.{}'.format(extension))]

        for filez in all_filenames:
            
            temp_csv = pd.read_csv(filez)
            combined_csv = pd.concat([combined_csv, temp_csv], axis=0)
            
        combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')