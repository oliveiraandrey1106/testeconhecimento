from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests


url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={ac0aeb1cccb064fe73078a975dcdd738}&lang={pt_br}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_tempo(cidade):
    resultado = requests.get(url.format(cidade, api_key))
    if resultado:
        json = resultado.json()
        # (Cidade, País, temp_celsius,  temp_fahrenheit, ícone, tempo)
        cidade = json['nome']
        pais= json['sys']['pais']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin -  273.15
        temp_fahrenheit = (temp_kelvin -  273.15) * 9 / 5  + 32
        icone = json ['tempo'][0]['icon']
        tempo =  json ['tempo'][0]['main']
        final = (cidade, pais, temp_celsius, temp_fahrenheit, icone , tempo)
        return final
    else:
        return None

def busca():
    cidade = cidade_text.get()
    tempo = get_tempo(cidade)
    if tempo:
        loc_lbl['texto'] = '{}, {}'.format(tempo[1])
        imagem['bitmap'] = 'icones/{}.png'.format(tempo[4])
        temp_lbl['texto'] = '{:.2f}°C, {:.2f}°F'.format(tempo[2], tempo[3])
        tempo_lbl['texto'] = tempo[5]
    else:
        messagebox.showerror('Erro', 'Sem informações.')


app = Tk()
app.title('Previsão do Tempo')
app.geometry('700x350')

cidade_text = StringVar()
cidade_entrada = Entry(app, textvariable=cidade_text)
cidade_entrada.pack()

busca_btn = Button(app, text='Consulta de tempo', width=16, command=busca)
busca_btn.pack()

loc_lbl = Label(app, text='', font=('bold', 20))
loc_lbl.pack()

imagem = Label(app, bitmap='')
imagem.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()

tempo_lbl = Label(app, text='')
tempo_lbl.pack()

app.mainloop()