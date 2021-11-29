import re
import pandas as pd
import string

class Cleaner():

    def __init__(self, csv_folder):
        self.csv_folder = csv_folder

    def clean(self):

        def address_splitterDE(self, df):
        
            try:
                df.insert(7, "Street", "")
                df.insert(8, "Bezirk", "")
                df.insert(9, "PLZ", "")
            except ValueError:
                pass

            for i in range(len(df.Address)):

                text = df.Address[i]

                try:
                    df["Street"][i] = re.match(r'^(\w*\s)*(?=\w+\s\d{5})', text)[0].strip(" ")
                except TypeError:
                    continue
                try:
                    df["Bezirk"][i] = re.search(r'(?<=(\d|\w))\s\w+\s(?=\d{5})', text)[0].strip(" ")
                except TypeError:
                    continue
                try:
                    df["PLZ"][i] = re.search(r'\d{5}', text)[0]
                except TypeError:
                    continue

        def punctuation(self, x):
            
            string.punctuation
            for punctuation in string.punctuation:
                x = x.replace(punctuation, '')
                
            return x

        def remove_br(self, x):
            
            x = x.replace("<br/>", " ")
            
            return x

        df = pd.read_csv(f"{self.csv_folder}combined_csv.csv")\
            .drop(columns=["Coordinates", "Name",
                            "Category", "Address", 
                            "Opening Hours", "Cuisine_1", 
                            "Cuisine_2", "Cuisine_3"], axis=1)
                            
        for i in range(2, 11):
            df = df.drop(columns=f"tag_{i}")

        df = df.drop_duplicates(subset=("position", "title"))

        df["openingHours/text"] = df["openingHours/text"]\
            .mask(df["openingHours/text"].isnull(), "")\
                .apply(lambda x: remove_br(x))

        df["vicinity"] = df["vicinity"].mask(df["vicinity"].isnull(), "")\
            .apply(lambda x: remove_br(x))\
                .apply(lambda x: punctuation(x))

        df = df.rename(columns={
            "position":"Coordinates",
            "title":"Name",
            "category/title":"Type",
            "vicinity":"Address",
            "openingHours/text":"Opening Hours",
            "tag_0":"Cuisine_1",
            "tag_1":"Cuisine_2"
        }).reset_index().drop(columns="index")

        address_splitterDE(df)

        df.to_csv("../data/final.csv", index=False, header=True ,encoding='utf-8-sig')