# Site-Scraper
## Introduction
This Module contains one Class, ***EnegryUsagePerCapita()***. It's used to scrape the energy usage per capita of all countries from the CIA-WorldFactBook-Site. The outcome is a dictionary with the country as key and the energy usage per capita as value. The outcome is saved in ***self.result***. The countries that couldn't be scraped are saved in ***self.failed***. The outcome is a dictionary with the country as key and the error as value.

## the Code
#### Imports
These imports are all important.
The ***requests*** is used to scrape from the CIA-WorldFactBook-Site.
The ***json*** is used to load the json from the CIA-WorldFactBook-Site.
The ***tqdm*** is used to show a progressbar.
The ***pycountry*** is used to have a list with all countries.
```python
import json
import requests
import pycountry
from tqdm import tqdm
```

#### integer complete_number(string) -> integer
This function is used to complete the number.
If the number is "thousand", it returns 1000.
If the number is "million", it returns 1000000.
If the number is "billion", it returns 1000000000.
If the number is "trillion", it returns 1000000000000.
If the number is none of these, it returns 1.
Then the outcome-number (from the function) is multiplied by another number in front of it.
```python
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
```
An example is:
```python
a = "300 million".split()					=> ["300", "million"]
float(a[0]) * complete_number(a[1])			=> float("300") * complete_number("million") => 300 * 1000000 = 300000000
=> 300000000
```

#### float makefloat(string) -> floating-point-number
This function replaces the commas with dots (because of the after-3-digit-commas) and returns the outcome as a float (through the integrated string to float conversion).
```python
def makefloat(string:str) -> float:
    return float(string.replace(",", ""))
```

### EnegryUsagePerCapita()
This class is used to get the energy usage per capita from the CIA-WorldFactBook-Site. It's a class because it's easier to use it as a class.
```python
class EnegryUsagePerCapita():
```

#### __init__(iterable) -> None
There's only one iterable object neede, a ***country***-array.
That iterable object is saved in ***self.countries***.
```python
	def __init__(self, countries:iter=list(pycountry.countries)) -> None:
		self.countries = countries
```

#### get_energy_usage_per_capita(boolean) -> dictionary
First three dictionaries are created. ***failed*** and ***result***.
***failed*** is used to save the countries that couldn't be scraped.
***result*** is used to save the countries that could be scraped.
The ***countries*** are looped through. And every single ***country*** is made lowercase and spaces are replaced with dashes, commas are removed.
and scraped from the CIA-WorldFactBook-Site.
If the status code is not 200 (= failed), the country is added to ***failed***.
If the status code is 200 (= not failed), the country is added to ***result***.
The ***result*** and ***failed*** is returned as a dictionary ({"result":result, "failed":failed}).
If withTQDM is True, a progressbar is shown. If withTQDM is False, no progressbar is shown. The default is False.
The scraping works like this:
The ***jsonasstring*** is the json from the CIA-WorldFactBook-Site. It's loaded to json, so the way to the important part can be accessed. The problem is that an important part of the json inside of the json is a string. That's why inside of the json is loaded again to json. The important part is the ***content*** of the ***content*** of the ***country*** of the ***json***. That outcome is split into a list. The first element is the number and the second element is the unit. The number is converted to a float (with the ***makefloat***-function) and the unit is converted to a number with the ***complete_number()***-function. The outcome is divided by 3412 to get the energy usage per capita in TWh.
```python
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
```




# Excel-Writer
## Introduction
This Module contains two Functions, ***write_to_excel()*** and ***sitescrape_to_excel()***.
***write_to_excel()*** is a bit more general. ***sitescrape_to_excel()*** uses ***write_to_excel()*** and does the exact thing wanted.
After the Site-Scarping, the results are put into an excel-dcoument. That's what the ***Excel-Writer*** does.

## the Code
#### Imports
These imports are all important. The ***sitescraper*** and ***pandas*** are imported.
Pandas does this working around with excel, 2D-Arrays, etc. and the sitescraper scrapes from the CIA-WorldFactBook-Site.
```python
from sitescraper import EnegryUsagePerCapita
import pandas as pd
```

#### write_to_excel(dictionary, iterable, string, string) -> None
The dictionary (***result***) is the target to be put in the excel sheet.
The iterable (***columns***) contains the two overcategories of the keys and values from ***result***.
The first string (***excelfile***) is the name of the Excel-File to be created.
The second string (***sheetname***) is the name of the Excel-Sheet to be created.
The only step needed is writing the ***result***s keys into the first column (***columns***\[0\]) and the ***result***s values into the second column (***columns***\[1\]) into the file ***excelfile*** in the sheet ***sheetname*** with help of the pandas-module.
```python
def write_to_excel(result:dict, columns:iter, excelfile:str="result.xlsx", sheetname:str="Sheet1") -> None:
	pd.DataFrame(list(zip(result.keys(), result.values())), columns=columns).to_excel(excelfile, sheet_name=sheetname, index=False)
```

#### sitescrape_to_excel() -> None
This function doesn't have any parameters because it's a unpersonalizable process. It calls the ***write_to_excel(dictionary, iterable, string, string)***-function with following parameters:
the dictionary (***result***)					=		EnegryUsagePerCapita().get_energy_usage_per_capita(withTQDM=True)\["result"\]
\\-> the thing that is put in the table are the countries with their energy usage
the iterable (***columns***)				=		\["Country","Energy Usage per Capita"\]
\\-> the thing that is put in the table are the countries with their energy usage
the first string (***excelfile***)			=		energyusagepercapita.xlsx
\\-> just a name describing the file a bit
the second string (***sheetname***)	=		main
\\-> main, because it's the only sheet (the main sheet)
```python
def sitescrape_to_excel() -> None:
	write_to_excel(EnegryUsagePerCapita().get_energy_usage_per_capita(withTQDM=True)["result"], ["Country","Energy Usage per Capita"], excelfile="energyusagepercapita.xlsx", sheetname="main")
```

#### __name__ == "__main__"
If the file is executed by itself, the ***sitescrape_to_excel()*** is called, so that the actuall purpose of this file happens.
```python
if __name__ == "__main__":
	sitescrape_to_excel()
```
