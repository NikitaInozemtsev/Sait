import webbrowser

import requests
from bs4 import BeautifulSoup

url = 'https://yandex.ru/pogoda/moscow'
r = requests.get(url)  # отправляем HTTP запрос и получаем результат
soup = BeautifulSoup(r.text)  # Отправляем полученную страницу в библиотеку для парсинга
tables = soup.find_all('div', {'class': 'forecast-briefly__day'})  # Получаем все таблицы с вопросами
tables1 = soup.find_all('div', {'class': 'forecast-briefly__day_weekend'})
i = 1
result = []
for item in tables:
    if (i > 3 and i < 14):
        item1 = tables[i]
        weekday = item1.find('div', {'class': 'forecast-briefly__name'}).text
        weekend = ''
        for it in tables1:
            if(item1 == it):
                weekend = 'weekend'

        data = item1.find('time', {'class': 'forecast-briefly__date'}).text
        temp = item1.find('div', {'class': 'forecast-briefly__temp_day'})
        if (temp.find('span', {'class': 'temp__pre'})):
          temp_day = temp.find('span', {'class': 'temp__pre'}).text + ' ' + temp.find('span', {'class': 'temp__value'}).text + temp.find('span', {'class': 'temp__unit'}).text
        else:
          temp_day = temp.find('span', {'class': 'temp__value'}).text + temp.find('span', {'class': 'temp__unit'}).text
        temp = item1.find('div', {'class': 'forecast-briefly__temp_night'})
        if(temp.find('span', {'class': 'temp__pre'})):
          temp_night = temp.find('span', {'class': 'temp__pre'}).text + ' ' + temp.find('span', {'class': 'temp__value'}).text + temp.find('span', {'class': 'temp__unit'}).text
        else:
          temp_night = temp.find('span', {'class': 'temp__value'}).text + temp.find('span', {'class': 'temp__unit'}).text
        condition = item1.find('div', {'class': 'forecast-briefly__condition'}).text
        img = item1.find('img').get('src')
        res = f'''<div class="item">
			<h2 class="{weekend}">{weekday}</h2>
			<span>{data}</span>
			<img src="{img}" width="48px" height="48px">
			<h2>{temp_day}</h2>
			<span>{temp_night}</span><br>
			<span>{condition}</span>
		</div>'''
        res = res.replace('\u2212', '-')
        result.append(res)
    i += 1
with open('index.html', 'w') as output_file:
  output_file.write('''<!DOCTYPE html>
<html>
<head>
	<title>Task7</title>
</head>

<style type="text/css">
	body, html {
		height: 100%;
		overflow: hidden;
	}
	#widget {
		width: 50%;
		height: 30%;
		display: flex;
		flex-direction: column;
	}
	#upper {
		display: flex;
		flex-direction: row;
		width: 100%;
	}
	#lower {
		display: flex;
		flex-direction: row;
		justify-content: center;
	}
	
	a {
		background-color: #eceef2;
		color : #222426;
		border-radius: 20px;
		padding: 6px 16px;
		font-size: 14px;
		text-decoration: none;
   		outline: 0;    
    	touch-action: manipulation;
    	cursor: pointer;
    	align-self: center;
    	margin-left: 8px;
	}
	a:hover {
		background-color: #dfe1e7;
	}
	.item {
		display: flex;
		flex-direction: column;
		width: 10%;
		height: 100%;
		padding: 2px;
	}
	.item:hover {
		border: solid 2px gray;
		padding: 0;
	}
	h2 {
		font-size: 18px;
		margin: 0;
		padding: 0;
		font-family: 'YS Text Web',Helvetica Neue,Arial;
	}

	.weekend {
		color:red;
	}
	span {
		font-size: 14px;
		color: #939cb0;
		font-family: 'YS Text Web',Helvetica Neue,Arial;
	}
</style>
<body>


<div id="widget">
	<div id="upper">
		<h1>Прогноз на 10 дней </h1>
		<a href="https://yandex.ru/pogoda/details?lat=55.682533&lon=37.623493&via=ms">Подробный прогноз на 10 дней</a>
		<a href="https://yandex.ru/pogoda/month?lat=55.682533&lon=37.623493&via=ms">На месяц</a>
	</div>
	<div id="lower">
		
	''')
  for tmp in result:
    output_file.write(tmp)

  output_file.write('''</div>
</div>


</body>
</html>''')

import http.server

webbrowser.open_new_tab("http://127.0.0.1:80")
address = ("", 80)
server = http.server.HTTPServer(address, http.server.CGIHTTPRequestHandler)
server.serve_forever()

