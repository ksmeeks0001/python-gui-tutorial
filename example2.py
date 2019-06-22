import django
from django.conf import settings
from django import forms
from django.template import Template, Context
import json

class MenuForm(forms.Form):
    name = forms.CharField(label="Item Name")
    price = forms.FloatField(label="Price")

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates'}
    ]

def setup():
    settings.configure(TEMPLATES=TEMPLATES)
    django.setup()
    
        
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
    
