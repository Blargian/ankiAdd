import mysql.connector
import time
import urllib.request
import requests
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
mydb = mysql.connector.connect(
    host='localhost',
    user="root",
    passwd="MySQLBl@rg1@n95",
    database="ankiadd"
)

#This function takes in a word as parameter and returns the word and type
def getData(word):
    
    cursor = mydb.cursor()
    search_string = word

    #return the word from the database
    sql_query = "SELECT bare FROM words WHERE bare = \"{}\" ".format(search_string)
    cursor.execute(sql_query)
    result=cursor.fetchone()

    #check if there is a match on the word and if there is then also query for the word_id, type
    if(result!=None):
        #get the word
        word = ''.join(result[0])
        
        #get the ID
        id_query = "SELECT id FROM words WHERE bare = \"{}\" ".format(word)
        cursor.execute(id_query)
        result=cursor.fetchone()
        id = result[0]

        #get the category
        category_query = "SELECT type FROM words WHERE bare = \"{}\" ".format(word)
        cursor.execute(category_query)
        result=cursor.fetchone()
        category = ''.join(result[0])

        #If the category is a verb, return perfective or imperfective, return partner.
        if(category=="verb"):
            aspect_query="SELECT aspect FROM verbs WHERE word_id= {} ".format(id)
            cursor.execute(aspect_query)
            result=cursor.fetchone()
            aspect = ''.join(result[0])

            aspect_query="SELECT partner FROM verbs WHERE word_id= {} ".format(id)
            cursor.execute(aspect_query)
            result=cursor.fetchone()
            partner = ''.join(result[0])

        print(id,word,category)
    else:
        print("not found")

# This function uses the Pixabay API to pull through 10 images

def get_pronounciation(word):

    pronounciation = requests.get("https://apifree.forvo.com/key/de6f30e76ae422dd36a2b7367439d5fd/format/json/action/word-pronunciations/word/{}/cat/language/ru".format(word))
    pronounciation_json = pronounciation.json()
    items = pronounciation_json["items"]
    urls = []

    for i in range(len(items)):
        urls.append(items[i]["pathmp3"])

    pronounce_request = requests.get(urls[0])
    if pronounce_request.status_code == 200:
        try:
            with open(dir_path+r'\\audio\\{}.mp3'.format(word),'wb') as f:
                f.write(pronounce.content)
        except:
                os.mkdir(dir_path+r'\\audio\\')
                with open(dir_path+r'\\audio\\{}.mp3'.format(word),'wb') as f:
                    f.write(pronounce_request.content)

#This function uses the Forvo API to pullthrough the audio pronounciation.
def get_image(search_term):

    number_images = 10
    images = requests.get("https://pixabay.com/api/?key=14522522-8f22d055987d89c99c8dc4f24&q={}&per_page={}".format(search_term,number_images))
    images_json_dict = images.json()

    hits = images_json_dict["hits"]
    urls = []
    for i in range(len(hits)):
        urls.append(hits[i]["webformatURL"])

    count =0
    for url in urls:
        picture_request = requests.get(url)
        if picture_request.status_code == 200:
            try:
                with open(dir_path+r'\\images\\{}.jpg'.format(count),'wb') as f:
                    f.write(picture_request.content)
            except:
                    os.mkdir(dir_path+r'\\images\\')
                    with open(dir_path+r'\\images\\{}.jpg'.format(count),'wb') as f:
                        f.write(picture_request.content)
        count+=1

if __name__ == '__main__':
    word = input("Please enter a word: ")
    getData(word)
    get_image(word)
    get_pronounciation(word)