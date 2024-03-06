# import kivy
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.scrollview import ScrollView
import requests
import json



all_words = {}
update_data_count = 0
def mine_word_data(find_the_word):
    synonyms = []
    antonyms = []
    api_url = "https://api.api-ninjas.com/v1/thesaurus?word=" + find_the_word
    response = requests.get(api_url, headers={'X-Api-Key': '2q6zn2pst8ogrceRbe5Lkw==GzcUiQru1oPthc40'})

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text),
        word_list = data['synonyms']
        word_list_antonyms = data['antonyms']
        for i in range(10):
            try:
                antonyms.append(word_list[i])
                synonyms.append(word_list_antonyms[i])
            except:
                break;

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






# get_word_data("dump")

with open("words_alpha.txt" , "r") as txt_file:
    while True:
        lines = txt_file.readlines()
        for line in lines:
            stripped_line = line.strip()
            mine_word_data(stripped_line)