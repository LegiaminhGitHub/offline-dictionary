import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import json

all_words = {}
update_data_count = 0
def get_word_data(find_the_word):
    synonyms = []
    antonyms = []
    api_url = "https://api.api-ninjas.com/v1/thesaurus?word=" + find_the_word
    response = requests.get(api_url, headers={'X-Api-Key': '2q6zn2pst8ogrceRbe5Lkw==GzcUiQru1oPthc40'})

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        word_list = data['synonyms']
        word_list_antonyms = data['antonyms']
        for i in range(10):
            antonyms.append(word_list[i])
            synonyms.append(word_list_antonyms[i])

        try:
            with open('data_syn.json', 'r') as f:
                data = json.load(f)
                data_add_json = {find_the_word : {"synonyms" : synonyms, "antonyms" : antonyms}}
                data_add_json.update(data)
            with open('data_syn.json', 'w') as f:
                json.dump(data_add_json, f , indent=2)
        except:
            with open("data_syn.json" , "w") as file:
                file.write("{ \n \n }")

        return synonyms, antonyms
    else:
        print("Error:", response.status_code, response.text)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.input = TextInput(hint_text='Enter a word')
        self.synonym_label = Label(text='')
        self.antonym_label = Label(text='')
        button = Button(text='Find synonyms and antonyms')
        button.bind(on_press=self.display_syn_ant)
        layout.add_widget(self.input)
        layout.add_widget(button)
        layout.add_widget(self.synonym_label)
        layout.add_widget(self.antonym_label)

        return layout

    def display_syn_ant(self, instance):
        word = self.input.text
        antonym_scroll = ScrollView()
        try:
            synonyms, antonyms = get_word_data(word)
            with open('data_syn.json', 'r') as f:
                data = json.load(f)
                # if word in data:
                #     for i in range (len(antonyms)):
                #         label_antonym = Label(text= antonyms[i])
                #         antonym_scroll.add_widget(label_antonym)
                self.synonym_label.text = 'Synonyms: ' + ', '.join(synonyms)
                self.antonym_label.text = 'Antonyms: ' + ', '.join(antonyms)
        except:
                self.synonym_label.text = 'Synonyms: NOT FOUND'
                self.antonym_label.text = 'Antonyms: NOT FOUND'

if __name__ == '__main__':
    MyApp().run()
