# python-gui-tutorial
Using Django and Eel for python GUI development


The idea of developing a graphical interface to your python program may be overwhelming to newer coders. Using the TK interface is time consuming and ugly. Other python GUI libraries seem complicated and not worth the return in the time it takes to learn them. Do you already know some HTML, CSS and JavaScript?
Why not use those to create an interface for your python program?
You can use a lot of the same techniques used for web development to create your local application. Using a library called eel, you can use HTML and CSS for your frontend and actually call python functions from JavaScript. Using django’s template system you can make your application dynamic. Here I’ll walk you through an example so you can use this method on your next project.

In this example we will create a system for entering menu items and their prices. We will store the data in a json file. 

this will be our file structure for this example

-example.py
-example2.py
templates/
    -add_item.html
static/
    -add_item_updated.html


example.py
```python
import json

def get_menu():
    """Attempt to read in menu from file and convert to dictionary or
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

def add_item(item):             #item is a list with first element menu items name and second element the price
    menu = get_menu()
    menu[item[0]] = item[1]
    save(menu)  
```
Next we will use the django Form class to create a form for input. We also need to write a function to set up django for use outside of a project.

example2.py
```python
import django
from django.conf import settings
from django import forms

class MenuForm(forms.Form):
    name = forms.CharField(label="Item Name")
    price = forms.FloatField(label="Price")

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates'}
    ]

def setup():
    settings.configure(TEMPLATES=TEMPLATES)
    django.setup()
  ```
  Now that we have written our django form, let's write a template to use it in.
  
  add_item.html
  ```
  <h1>{{ restaurant }}</h1>
<h3>Add Item Form</h3>
<form> 
	{{ form }} 
	<button id="submit">ADD</button>
</form>
<ul id='item_list'>
{% for i in menu %}
<li>{{ i }}</li> 
{% endfor %}
</ul>
  ```
  Now lets add to example2.py to initialize our form and generate html for our template.
  
```python
import django
from django.conf import settings
from django import forms
from django.template import Template, Context
import json

''                     ''
def refresh():
  file = open(r'templates\add_item.html', 'r')
  template = Template(file.read())
  file.close()
  file = open('menu.json', 'r')
  menu = json.loads(file.read())
  file.close()
  items = list(menu.keys())
  context = Context( {'restaurant': "Kevin's BBQ",'form': MenuForm(), 'menu':items} )
  new_template = open(r'static\add_item_updated.html', 'w')
  new_template.write(template.render(context))
  new_template.close()
    
 ```
 
Now that we have our html file generated for us we can use eel to create our window. 

example.py

 ```python
import eel
import json
import example2

''                 ''

@eel.expose                                #adding eel decorator to make callable from javascript
def add_item(item):
    menu = get_menu()
    menu[item[0]] = item[1]
    save(menu)
    example2.refresh()                    #adding an item requires regenerating the template to include the new item in context
    
    
    
if __name__ == "__main__":
    example2.setup()                       #setup django
    example2.refresh()                     #generate the template
    eel.init('static')                     #tell eel whate directory your html files are located in
    eel.start('add_item_updated.html')     #opens window

```
Note: running from idle may cause hangups on importing eel. Run the script by double clicking

Adding the eel.expose decorator to our add_item function, sends that function into the page and actually allows us to call it from the javascript. All that's left now is write the javascript that will get the values from the inputs add them to a list and call the add_item function. Before doing that we also need to include the eel.js file. Add the following to the bottom of our template add_item.html

```javascript

<script type='text/javascript' src='/eel.js'></script>   //including /eel.js, notice the slash to properly add to file 
<script type='text/javascript'>
	let btn = document.getElementById("submit");
	btn.onclick = 
	function add_item(){
		let item = [                                  
					document.getElementById('id_name').value,
					document.getElementById('id_price').value
					];
		eel.add_item(item);                 //calling the python function from the javascript through the eel object. 
		
		}
</script>
```
notice the IDs for the inputs are 'id_name' and 'id_price'. This is based off of the name we gave them in the django form and can be found by actually looking at the add_item_updated.html file.

Now when running example.py you can add items to the menu. Doing so should create the json file for storing the state of your menu. You should also see current menu items populate below the form after adding them. 

There is obviously a lot more to django and eel than what is shown here but hopefully this was a decent introduction to concepts of both and an interesting way to combine the two. Don;t hesistate to provide me feedback about this tutorial. Thanks.

django     https://docs.djangoproject.com/en/2.2/
eel        https://github.com/ChrisKnott/Eel
