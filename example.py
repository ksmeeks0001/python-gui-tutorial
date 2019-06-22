#Simple register program for restaurant

import eel
import json
import example2

def get_menu():
    """Attempt to read in menu from file as convert to dictionary or
    return an empty dictionary."""
    try:
        with open('menu.json' , 'r') as file:
            return json.loads(file.read())
    except:
        return dict()
        

def save(menu):
    #save the menu dictionary in json file
    with open('menu.json', 'w') as file:
        file.write(json.dumps(menu))

@eel.expose
def add_item(item):
    menu = get_menu()
    menu[item[0]] = item[1]
    save(menu)
    example2.refresh()
    



def display():
    eel.start('add_item_updated.html')
    
if __name__ == "__main__":
    example2.setup()
    example2.refresh()
    eel.init('static')
    display()
    
    
