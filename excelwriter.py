from sitescraper import EnegryUsagePerCapita
import pandas as pd

def write_to_excel(result:dict, columns:iter, excelfile:str="result.xlsx", sheetname:str="Sheet1"):
    pd.DataFrame(list(zip(result.keys(), result.values())), columns=columns).to_excel(excelfile, sheet_name=sheetname, index=False)

def sitescrape_to_excel():
    write_to_excel(EnegryUsagePerCapita().get_energy_usage_per_capita(withTQDM=True)["result"], ["Country","Energy Usage per Capita"], excelfile="energyusagepercapita.xlsx", sheetname="main")

if __name__ == "__main__":
    sitescrape_to_excel()