import requests
from prettytable import PrettyTable

#free api key 400 requests per day
mykey = '9e5lco28r1ktc2hvb4bxs3igwsbbghpqyz0998fk'

def get_city_id(city, key):
    api_url = f"https://www.meteosource.com/api/v1/free/find_places_prefix?text={city}&language=en&key={key}"
    response = requests.get(api_url)
    data = response.json()
    table = PrettyTable()
    table.field_names = ['Num','City Name', 'State', 'Country']
    city_id_list = {}
    if data:
        for num, place in enumerate(data,1): 
            city_id_list[num] = place['place_id']
            table.add_row([num, place['name'], place['adm_area1'], place['country']])
    
        print("Following are the results of the cities found : \n")
        print(table)
        number = int(input("Enter the number of city you want the weather of : \n >"))
        try:
            return city_id_list[number]
        except KeyError:
            print('Please Enter a valid number !!!')
    
    else:
        print("Please enter a valid city name.")
        return None


def get_weather(city_id, key):
    api_url = f"https://www.meteosource.com/api/v1/free/point?place_id={city_id}&sections=current%2Cdaily&language=en&units=auto&key={key}"
    response = requests.get(api_url)
    data = response.json()
    if data:
        table = PrettyTable()
        table.field_names = ['Label', 'Description']
        table.add_rows([['Weather', data['current']['summary']],
                        ['Temperature', data['current']['temperature']],
                        ['Wind Speed', data['current']['wind']['speed']],
                        ['Wind Direction', data['current']['wind']['dir']]
        ])
        print(table)
    
        table2 = PrettyTable()
        table2.field_names = ['Label', 'Description']
    
        print(f"\n****FORECAST for tomorrow {data['daily']['data'][0]['day']}****\n")
    
        table2.add_rows([['Weather', data['daily']['data'][0]['weather']],
                         ['Summary', data['daily']['data'][0]['summary']],
                         ['Temperature', data['daily']['data'][0]['all_day']['temperature']],
                         ['Wind Speed',  data['daily']['data'][0]['all_day']['wind']['speed']],
                         ['Wind Direction',  data['daily']['data'][0]['all_day']['wind']['dir']]
        ])
        print(table2)


def main():
    print("This is a simple weather application.")
    while True:
        city_name = input('Please enter a city name (press Q/q to quit) : \n >')
        
        if city_name == 'q' or city_name == 'Q':
            exit()
        elif city_name == '':
            print('Please enter a city name')

        city_id = get_city_id(city_name, mykey)
        
        if city_id:
            get_weather(city_id, mykey)


if __name__ == "__main__":
    main()

