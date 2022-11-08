from bs4 import BeautifulSoup
import argparse
import requests 
import json



def parse_itemssold(text):

    numbers =''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers) 
   
    else:
        return 0

def parse_price(text):

    numbers =''
    for char in text:
        if char in '1234567890':
            numbers += char
    if '$' in text:
        return int(numbers) 
    else:
        return 0

def parse_ship(text):

    numbers =''
    for char in text:
        if char in '1234567890':
            numbers += char
    if '$' in text:
        return int(numbers) 
    else:
        return 0   



parser = argparse.ArgumentParser(description='download from ebay and convert to json')
parser.add_argument('search_term')
args = parser.parse_args() 

print('args.search_term=', args.search_term)

items = []
for page_number in range(1,11):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn'
    url += str(page_number)
    url += '&rt=nc'
    print('url=',url)

    r = requests.get(url)
    status = r.status_code 
    print('status=', status)
    html = r.text
    #print('html', html[:50])


    soup = BeautifulSoup(html,'html.parser')
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:
        
        # extract name
        name = None
        tags_name = tag_item.select('.s-item__title')
        for tag in tags_name:
            name = tag.text

        # extract freereturns
        freereturns = False
        tags_freereturns = tag_item.select('.s-item__free-returns')
        for tag in tags_freereturns:
            freereturns = True

        # extract status
        status = None
        tags_status = tag_item.select('.SECONDARY_INFO')
        for tag in tags_status:
            status = tag.text

        # extract itemssold
        items_sold = None
        tags_itemssold = tag_item.select('.s-item__hotness') 
        for tag in tags_itemssold:
            items_sold = parse_itemssold(tag.text)
        # print('items_sold=', items_sold)

        # extract price
        items_price = None
        tags_itemsprice = tag_item.select('.s-item__price') 
        for tag in tags_itemsprice:
            items_price = parse_price(tag.text)
        #print('items_price=', items_price)

        # extract shipping 
        items_ship = None
        tags_itemsship = tag_item.select('.s-item__detail--primary') 
        print(tags_itemsship)
        for tag in tags_itemsship:
            
            items_ship = parse_ship(tag.text)
        print('items_ship=', items_ship)



        item = {
            'name': name,
            'free_returns': freereturns,
            'items_sold': items_sold,
            'status': status,
            'items_ship': items_ship,
            'items_price': items_price,
        }
        items.append(item)




    print('len(tag_items)=', len(tags_items))
    print('len(items)=', len(items))
    


# write json
filename = args.search_term + '.json'

with open(filename, 'w', encoding='ascii') as f:
    f.write(json.dumps(items))