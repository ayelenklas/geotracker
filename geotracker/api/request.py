import requests
import os
import json
from geotracker.api.params import URL, PARAMS
from geotracker.api.HERE_transformer import Transformer
from geotracker.api.cleaner import Cleaner


class Requester:
    def __init__(self, url, params):
        self.url = url
        self.params = params

    def fetch_data(self, dumpname):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            return response
        else:
            data = response.json()
            print(os.getcwd())
            with open(f"jsondumps/data_{dumpname}.json", "w+", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    url = URL
    params = PARAMS
    # for i, param in enumerate(params):
    #     requester = Requester(url, param)
    #     requester.fetch_data(i)
    print(os.curdir)
    t = Transformer("csv", "jsondumps")
    t.json_to_df()
    t.csv_merger()
    c = Cleaner("csv")
    c.clean()



