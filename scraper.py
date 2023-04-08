import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Get ad data from page
def getAdsData(params: str):
    # Search URL
    url = "https://www.donedeal.ie/search/api/v4/find/"

    # POST Request
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    adsData = requests.post(
        url, data=params, headers=headers, verify=False, allow_redirects=False
    )
    return adsData.json()


# Convert price strings to ints
def getPrice(prc, currency):
    priceNum = int(prc.replace(",", ""))

    if currency != "EUR":
        priceNum = priceNum * 1.14

    return priceNum


# Convert mileage strings to ints and convert to kilometres
def getMileage(km):
    strLen = len(km)

    if km[strLen - 2 : strLen] == "mi":
        multiplier = 1.60934
    else:
        multiplier = 1

    km = km[0 : strLen - 3]

    kmVal = int(km.replace(",", ""))

    # If the user has given a value of 120 miles, they mean 120,000 miles
    # If mileage is over 1 million, divide by 10
    if kmVal < 1000:
        kmVal = kmVal * 1000
    elif kmVal > 1000000:
        kmVal = kmVal // 10

    return kmVal * multiplier


def gen_params_str(start_index: int = 0, num_results: int = 30) -> str:
    head_params = {"adType": "forsale", "max": 30, "start": 0, "section": "cars"}
    dependant_params = {
        "parentName": "make",
        "parentValue": "Audi",
        "childName": "model",
        "childValues": ["A6"],
    }
    end_params = {"price_to": "45000", "year_from": "2019"}

    param_str = f"""{str(head_params)[:-1]}, "dependant":[{{{str(dependant_params)[1:]}], {str(end_params)[1:]}"""
    param_str = param_str.replace("'", '"').replace(" ", "")

    return param_str


def main() -> None:
    params = gen_params_str()
    ads_data = getAdsData(params)["ads"]
    print("Done")


if __name__ == "__main__":
    correct_params = '{"adType":"forsale","max":30,"start":0,"section":"cars","dependant":[{"parentName":"make","parentValue":"Audi","childName":"model","childValues":["A6"]}],"price_to":"45000","year_from":"2019"}'
    # print(f"Correct: \t{correct_params}")
    # print(f"Gen: \t\t{gen_params_str()}")
    assert gen_params_str() == correct_params

    main()
