import json
import requests
import pycountry
from tqdm import tqdm

def complete_number(number:str) -> int:
    if number == "thousand":
        return 1000
    if number == "million":
        return 1000000
    elif number == "billion":
        return 1000000000
    elif number == "trillion":
        return 1000000000000
    else:
        return 1

def makefloat(string:str) -> float:
    return float(string.replace(",", ""))

class EnegryUsagePerCapita():
    def __init__(self, countries:iter=list(pycountry.countries)) -> None:
        self.countries = countries

    def get_energy_usage_per_capita(self, withTQDM:bool=False) -> dict:
        failed = {}
        result = {}
        for country in tqdm(self.countries) if withTQDM else self.countries:
            jsonasstring = requests.get("https://www.cia.gov/the-world-factbook/page-data/countries/{}/page-data.json".format(country.name.replace(",", "").replace(" ", "-").lower()), allow_redirects=True)
            if jsonasstring.status_code != 200:
                failed[country.name] = jsonasstring.status_code
            else:
                try: 
                    splited = json.loads(json.loads(jsonasstring.content)["result"]["data"]["country"]["json"])["categories"][6]["fields"][10]["content"].split()
                except IndexError as e:
                    failed[country.name] = e
                else:
                    result[country.name] = makefloat(splited[0])*complete_number(splited[1])/3412
        self.failed = failed
        self.result = result
        return {"result":result, "failed":failed}



# print(EnegryUsagePerCapita(list(pycountry.countries)).get_energy_usage_per_capita(withTQDM=True))

# to the string part:       ROOT.result.data.country.json
# the string part as json:  ROOT.categories[6].fields[10].content


