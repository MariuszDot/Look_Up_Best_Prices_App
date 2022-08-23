import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup as bs


sg.theme('DarkGrey13')
layout = [
    [sg.Push(), sg.Text('What would you like me to find?', key= '-TEXT-', font= 'Courier 18'), sg.Push()],
    [sg.Push(), sg.Input('Enter your thing', key= '-INPUT-', font= 'Courier 8'), sg.Push()],
    [sg.Push(), sg.Button('Look for best prices\n press Enter', key= '-BUTTON-', font= 'Courier 10', size= (25,3))],
    [sg.Push(), sg.Multiline("I'll get you three best offers from:\n\n Media Markt\n Media Expert\n RTV-Euro-AGD\n Ole-Ole!", key= '-OUTPUT-', size= (450, 50), font= 'Courier 10'), sg.Push()]
]

def media_markt_search(phrase):
    # Making a soup from Media Markt website search
    url = f'https://mediamarkt.pl/search?query%5Bmenu_item%5D=&query%5Bquerystring%5D={phrase.replace(" ", "%20")}'
    session = requests.session()
    session.headers['User-Agent'] = 'Chrome/94.0.4606.81'
    html = session.get(url, timeout= 7)
    soup = bs(html.text, 'html.parser')

    prices_list = []
    links_list = []
    # Searching for containers that contain prices and links - then storing them in usefully formatted lists
    divs_of_items = soup.find_all('div', index=True)
    for div in divs_of_items:
        div_price = div.find_all('div', {"class", "main-price is-big"}) # Regular prices
        div_discount = div.find_all('div', {"class", "main-price for-action-price is-big"}) # Limited time discounts prices
        div_links = div.find_all('a', href=True, uid=True, attrs={"class": "is-hover-underline spark-link"}) # Links
        for price in div_price:
            prices_list.append(price.text.replace('\n', '').replace(',-', '').replace(' ','').strip())
        for price in div_discount:
            prices_list.append(price.text.replace('\n', '').replace(',-', '').replace(' ','').strip())
        for link in div_links:
            links_list.append(link['href'])
    for index, element in enumerate(prices_list):
        if not index // 2 == 0:
            del prices_list[index]
    try:
        prices_list.pop(0) # First element is always unuseful '/'
    except:
        pass

    # Getting results from Media Markt website search, depending on the amount of items found
    if len(prices_list) >= 3:
        answer_media_markt = f" Media Markt offers:\n\n{prices_list[0]} at mediamarkt.pl{links_list[0]}\n{prices_list[1]} at mediamarkt.pl{links_list[1]}\n{prices_list[2]} at mediamarkt.pl{links_list[2]}"
    elif len(prices_list) == 2:
        answer_media_markt = f" Media Markt offers:\n\n{prices_list[0]} at mediamarkt.pl{links_list[0]}\n{prices_list[1]} at mediamarkt.pl{links_list[1]}"
    elif len(prices_list) == 1:
        answer_media_markt = f" Media Markt offers:\n\n{prices_list[0]} at mediamarkt.pl{links_list[0]}"
    else:
        answer_media_markt = ' Media Markt has nothing to offer\n\n'
    return answer_media_markt

def x_kom_search(phrase):
    # Making a soup from x-kom website search
    url = f'https://www.x-kom.pl/szukaj?q={phrase.replace(" ", "%20")}'
    session = requests.session()
    session.headers['User-Agent'] = 'Chrome/94.0.4606.81'
    html = session.get(url, timeout= 7)
    soup = bs(html.text, 'html.parser')

    # Searching for containers that contain prices and links - then storing them in a usefully formatted lists
    prices_list = []
    links_list = []
    divs_of_items = soup.find_all('div', {"class": "sc-1s1zksu-0 dzLiED sc-162ysh3-1 irFnoT"})
    for div in divs_of_items:
        un_test = div.find_all('div', {"class": "sc-1yu46qn-17 gFeuWr"}) # Those are the items that are not available for an unknown period of time
        if not un_test:
            div_price = div.find_all('span', {"class", "sc-6n68ef-0 sc-6n68ef-3 guFePW"})
            div_links = div.find_all('a', href = True, attrs= {"class": "sc-1h16fat-0 dNrrmO"})
            for price in div_price:
                prices_list.append(price.text)
            for link in div_links:
                links_list.append(link['href'])
    # Getting an answer based on the amount of found items
    if len(prices_list) >= 3:
        answer_x_kom = f"\n\n X-kom offers:\n\n{prices_list[0]} at www.x-kom.pl{links_list[0]}\n{prices_list[1]} at www.x-kom.pl{links_list[1]}\n{prices_list[2]} at " \
            f"www.x-kom.pl{links_list[2]}"
    elif len(prices_list) == 2:
        answer_x_kom = f"\n\n X-kom offers:\n\n{prices_list[0]} at www.x-kom.pl{links_list[0]}\n{prices_list[1]} at www.x-kom.pl{links_list[1]}"
    elif len(prices_list) == 1:
        answer_x_kom = f"\n\n X-kom offers:\n\n{prices_list[0]} at www.x-kom.pl{links_list[0]}"
    else:
        answer_x_kom = '\n\n X-kom has nothing to offer\n\n'
    return answer_x_kom

def rtv_euro_agd_search(phrase):
    # Making a soup from RTV Euro AGD website search
    url = f'https://www.euro.com.pl/search.bhtml?keyword={phrase.replace(" ", "%20")}'
    session = requests.session()
    session.headers['User-Agent'] = 'Chrome/94.0.4606.81'
    html = session.get(url, timeout= 7)
    soup = bs(html.text, 'html.parser')

    prices_list = []
    links_list = []
    # Searching for containers that contain prices and links - then storing them in a usefully formatted lists
    divs_of_items = soup.find_all('div', {"class": "product-for-list"})
    for div in divs_of_items:
        div_price = div.find_all('div', {"class": "price-normal selenium-price-normal"})
        div_link = div.find_all('a', {"class": "js-save-keyword"}, href= True)
        for price in div_price:
            prices_list.append(price.text.replace('\n','').replace('\t','').replace("\xa0",''))
        for link in div_link:
            if link["href"] in links_list or link["href"][-7:] == '#opinie': # Removing duplicates and review subsites
                pass
            else: links_list.append(link["href"])
    # Removing duplicate positions
    for index, element in enumerate(prices_list):
        if not index // 2 == 0:
            del prices_list[index]
    try: prices_list.pop(0)
    except: pass
    # Getting an answer based on the amount of items found
    if len(prices_list) >= 3:
        answer_rtv_euro_agd = f"\n\n RTV-Euro-AGD offers:\n\n{prices_list[0]} at www.euro.com.pl{links_list[0]}\n{prices_list[1]} at www.euro.com.pl{links_list[1]}\n{prices_list[2]} at " \
            f"www.euro.com.pl{links_list[2]}"
    elif len(prices_list) == 2:
        answer_rtv_euro_agd = f"\n\n RTV-Euro-AGD offers:\n\n{prices_list[0]} at www.euro.com.pl{links_list[0]}\n{prices_list[1]} at www.euro.com.pl{links_list[1]}"
    elif len(prices_list) == 1:
        answer_rtv_euro_agd = f"\n\n RTV-Euro-AGD offers:\n\n{prices_list[0]} at www.euro.com.pl{links_list[0]}"
    else:
        answer_rtv_euro_agd = '\n\n RTV-Euro-AGD has nothing to offer\n\n'
    return answer_rtv_euro_agd

def ole_ole_search(phrase):
    url = f'https://www.oleole.pl/search.bhtml?keyword={phrase.replace(" ", "%20")}'
    session = requests.session()
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    html = session.get(url, timeout= 7)
    soup = bs(html.text, 'html.parser')

    prices_list = []
    links_list = []
    # Searching for containers that contain prices and links - then storing them in a usefully formatted lists
    divs_of_items = soup.find_all('div', {"class": "product-for-list"})
    for div in divs_of_items:
        div_price = div.find_all('div', {"class": "price-normal selenium-price-normal"})
        div_link = div.find_all('a', {"class": "js-save-keyword"}, href= True)
        for price in div_price:
            prices_list.append(price.text.replace('\n','').replace('\t','').replace('\xa0',''))
        for link in div_link:
            if link["href"] in links_list or link["href"][-7:] == '#opinie':  # Removing duplicates and review subsites
                pass
            else:
                links_list.append(link["href"])
    for index, element in enumerate(prices_list):
        if not index // 2 == 0:
            del prices_list[index]
    try:
        prices_list.pop(0)
    except:
        pass
    # Getting an answer based on the amount of items found
    if len(prices_list) >= 3:
        answer_ole_ole = f"\n\n Ole-Ole offers:\n\n{prices_list[0]} at www.oleole.pl{links_list[0]}\n{prices_list[1]} at www.oleole.pl{links_list[1]}\n{prices_list[2]} at " \
            f"www.oleole.pl{links_list[2]}"
    elif len(prices_list) == 2:
        answer_ole_ole = f"\n\n Ole-Ole offers:\n\n{prices_list[0]} at www.oleole.pl{links_list[0]}\n{prices_list[1]} at www.oleole.pl{links_list[1]}"
    elif len(prices_list) == 1:
        answer_ole_ole = f"\n\n Ole-Ole offers:\n\n{prices_list[0]} at www.oleole.pl{links_list[0]}"
    else:
        answer_ole_ole = '\n\n Ole-Ole has nothing to offer\n\n'
    return answer_ole_ole


## GUI ###
def play():
    window = sg.Window(" Prices checker ", layout, size= (1250, 500), finalize = True)
    window['-INPUT-'].bind("<Return>", "_Enter")
    window['-INPUT-'].bind("<Button>", "_Mouse")
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED: break
        if "_Mouse" and values["-INPUT-"] == 'Enter your thing':
            window["-INPUT-"].update('')
        if event == '-BUTTON-' or event == '-INPUT-' + '_Enter':
            phrase_to_search = values['-INPUT-']
            try: answer_media_markt = media_markt_search(phrase_to_search)
            except requests.exceptions.ReadTimeout: answer_media_markt = ' Media Markt is not answering'
            try: answer_x_kom = x_kom_search(phrase_to_search)
            except requests.exceptions.ReadTimeout: answer_x_kom = ' X-kom is not answering'
            try: answer_rtv_euro_agd = rtv_euro_agd_search(phrase_to_search)
            except requests.exceptions.ReadTimeout:  answer_rtv_euro_agd = ' RTV-Euro-AGD is not answering'
            try: answer_ole_ole = ole_ole_search(phrase_to_search)
            except requests.exceptions.ReadTimeout: answer_ole_ole = ' Ole-Ole is not answering'
            window['-OUTPUT-'].update(answer_media_markt + answer_x_kom + answer_rtv_euro_agd + answer_ole_ole)

    window.close()

if __name__ == '__main__':
    play()