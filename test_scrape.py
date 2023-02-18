import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# https://www.sejm.gov.pl/Sejm9.nsf/poslowie.xsp?type=A
# https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id=001&type=A
#
#
# https://www.sejm.gov.pl/Sejm8.nsf/poslowie.xsp?type=P
# https://www.sejm.gov.pl/Sejm8.nsf/posel.xsp?id=001&type=P
#
# https://www.sejm.gov.pl/Sejm7.nsf/poslowie.xsp?type=P
# https://www.sejm.gov.pl/Sejm7.nsf/posel.xsp?id=001&type=P


def get_pm_name(soup):
    return soup.find('h1').text


def get_value(soup, text):
    try:
        tag = soup.find_all(string=text)
        value = tag[0].parent.find_next_sibling().text
        return value
    except:
        print(text)
        return "brak danych"


def get_pm_profile(soup, variable_list):
    pm_profile = []
    pm_profile.append(get_pm_name(soup))

    for i in variable_list:
        pm_profile.append(get_value(soup, re.compile(i)))

    return pm_profile

def get_all_pm_profiles(parliament_term, type, variable_list):
    all_pm_profiles = []
    for i in range(1, 461):
        no_with_zeros = str(i).zfill(3)
        url = f'https://www.sejm.gov.pl/Sejm{parliament_term}.nsf/posel.xsp?id={no_with_zeros}&type={type}'
        soup = BeautifulSoup(requests.get(url).text, 'lxml')
        pm_profile = get_pm_profile(soup, variable_list)
        all_pm_profiles.append(pm_profile)
    return all_pm_profiles

def pm_profiles_to_pandas(pm_profiles):
    pm_profiles_zip = list(zip(*pm_profiles))
    d = {'Imię i nazwisko': pm_profiles_zip[0],
         'Data wyboru': pm_profiles_zip[1],
         'Lista': pm_profiles_zip[2],
         'Okręg wyborczy': pm_profiles_zip[3],
         'Liczba głosów': pm_profiles_zip[4],
         'Ślubowanie': pm_profiles_zip[5],
         'Staż parlamentarny': pm_profiles_zip[6],
         'Klub lub koło:': pm_profiles_zip[7],
         'Data i miejsce urodzenia': pm_profiles_zip[8],
         'Wykształcenie': pm_profiles_zip[9],
         'Ukończona szkoła': pm_profiles_zip[10],
         'Zawód': pm_profiles_zip[11],
         }
    df = pd.DataFrame(data=d)

    return df


variable_list = ["Wybran.* dnia:", "Lista:", "Okręg wyborczy:", "Liczba głosów:",
                "Ślubowanie:", "Staż parlamentarny:", "Klub/koło:", "Data i miejsce urodzenia:",
                "Wykształcenie:", "Ukończona szkoła:", "Zawód:"]

print("Dane 9 kadencja semju:")
pm_profiles_9 = get_all_pm_profiles(9, "A", variable_list)
pm_profiles_9_df = pm_profiles_to_pandas(pm_profiles_9)

print(pm_profiles_9_df)

print("Dane 8 kadencja semju:")
pm_profiles_8 = get_all_pm_profiles(8, "P", variable_list)
pm_profiles_8_df = pm_profiles_to_pandas(pm_profiles_8)

print(pm_profiles_8_df)

print("Dane 7 kadencja semju:")
pm_profiles_7 = get_all_pm_profiles(7, "P", variable_list)
pm_profiles_7_df = pm_profiles_to_pandas(pm_profiles_9)

print(pm_profiles_9_df)
