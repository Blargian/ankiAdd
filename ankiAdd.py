import mysql.connector
import time
import urllib.request
import requests
import os
from pathlib import Path
from multiprocessing import Pool
import eel
import json
import sys
import module_locator
import shutil

# "C:\Program Files\Anki\anki" -b "C:\Users\Shaun\Desktop"

eel.init('web')

#Please add your keys to your system env variables 
google_api_key = os.environ.get('google_api_key')
google_cx= os.environ.get('google_cx')
dir_path = os.path.dirname(os.path.realpath(__file__))
mydb = mysql.connector.connect(
    host='localhost',
    user="root",
    passwd= os.environ.get('mysql_db_password'),
    database="ankiadd",
    auth_plugin='mysql_native_password'
)

#Dictionary which will store data and be used to covert it to a JSON file (RESTful API type idea)
word_data = {}
sys.path.append("C:/Users/Shaun/Documents/Personal_Projects/ankiExperiment/anki-scripting/anki")
from anki.storage import Collection
PROFILE_HOME = os.path.expanduser("C:/Users/Shaun/Desktop/User 1")
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

#This function takes in a word as parameter and returns the word and type
@eel.expose
def getData(word):
    
    cursor = mydb.cursor(buffered=True)
    search_string = word

    #return the word from the database
    sql_query = "SELECT bare FROM words WHERE bare = \"{}\" ".format(search_string)
    cursor.execute(sql_query)
    result=cursor.fetchone()

    #check if there is a match on the word and if there is then also query for the word_id, type
    if(result!=None):
        #get the word
        word = ''.join(result[0])
		
		#get the accented
        id_query = "SELECT accented FROM words WHERE bare = \"{}\" ".format(word)
        cursor.execute(id_query)
        result=cursor.fetchone()
        accented = result[0]
        
        #get the ID
        id_query = "SELECT id FROM words WHERE bare = \"{}\" ".format(word)
        cursor.execute(id_query)
        result=cursor.fetchone()
        id = result[0]
		
		#get the translations
        id_query = "SELECT tl FROM translations WHERE word_id={} and lang=\"en\" ".format(id)
        cursor.execute(id_query)
        result=cursor.fetchone()
        translation = result[0]

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

        #Add to the dictionary for JSON
        word_data['word'] = word
        return word, category, translation, accented
    else:
        print("not found")
        return False

# This function uses the Pixabay API to pull through 10 images
@eel.expose
def get_pronounciation(word):

    UTF8 = word.encode()
    #remove the b' and trailing '
    UTF8 = str(UTF8)[2:-1]
    UTF8 = UTF8.replace("\\x","%").upper()
    #print(UTF8)
    forvo_key = os.environ.get('forvo_key')
    search = "https://apifree.forvo.com/action/word-pronunciations/format/json/word/{}/id_lang_speak/138/key/{}/".format(UTF8,forvo_key)
    #print(search)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        pronounciation_json = requests.get(search,headers=headers)
    except:
        print("Forvo API response: "+str(pronounciation_json))
    
    pronounciation_json = pronounciation_json.json()
    items = pronounciation_json["items"]
    urls = []

    for i in range(len(items)):
        urls.append(items[i]["pathmp3"])

    if(len(urls)!=0):
        pronounce_request = requests.get(urls[0],headers=headers)
        if pronounce_request.status_code == 200:
            try:
                with open(dir_path+r'\\audio\\{}.mp3'.format(word),'wb') as f:
                    f.write(pronounce_request.content)
            except:
                    os.mkdir(dir_path+r'\\audio\\')
                    with open(dir_path+r'\\audio\\{}.mp3'.format(word),'wb') as f:
                        f.write(pronounce_request.content)   
            word_data['pronounciation'] = {'audio_name':word,'audio_url':dir_path+r'\\audio\\{}.mp3'.format(word)}
    else:
        print("There was a problem retrieving pronounciation")
        return False
        
    

#This function uses the Forvo API to pullthrough the audio pronounciation.
@eel.expose
def get_image(search_term):

    number_images = 10
    pixabay_key = os.environ.get('pixabay_key')
    images = requests.get("https://pixabay.com/api/?key={}&q={}&per_page={}".format(pixabay_key,search_term,number_images))
    if (images != 200):
        return False 
    images_json_dict = images.json()

    hits = images_json_dict["hits"]
    urls = []
    for i in range(len(hits)):
        urls.append(hits[i]["webformatURL"])

    return urls   

@eel.expose
def persist_image(url,word):
    picture_request = requests.get(url)
    if picture_request.status_code == 200:
            try:
                with open(dir_path+r'\\images\\{}.jpg'.format(word),'wb') as f:
                    f.write(picture_request.content)
            except:
                    os.mkdir(dir_path+r'\\images\\')
                    with open(dir_path+r'\\images\\{}.jpg'.format(word),'wb') as f:
                        f.write(picture_request.content)
            word_data['image'] = {'image_name':word,'img_url':dir_path+r'\\img\\{}.jpg'.format(word)}
    return True

#Uses the google image search API
@eel.expose
def google_image(search_term):
    urls = []
    google_request = requests.get("https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&searchType=image&fileType=jpg&imgSize=medium&alt=json".format(google_api_key,google_cx,search_term))
    google_request = google_request.json()
    hits = google_request["items"]
    #print(google_request)

    for i in range(len(hits)):
         urls.append(hits[i]["link"])
    return urls   
	
# @eel.expose
# def image_download(url):
#     pool = Pool(20)
#     results = pool.map(persist_image, url)

@eel.expose
def createJSON():
    with open('word_data.json','w') as outfile:
        json.dump(word_data,outfile)

class Word:
    def __init__(self,doc):
        self.doc = doc

    def title(self):
        return self.doc['word']

    def audio_url(self):
        if "pronounciation" in self.doc:
            return self.doc["pronounciation"]["audio_url"]

    def image_url(self):
        if "image" in self.doc:
            return self.doc["image"]["img_url"]
    
#Credit for this code belongs to Julien Sobczak and modified slightly for my purposes   
def load(col,filepath):

    audio_directory = os.path.join(os.path.dirname(filepath),'audio')
    image_directory = os.path.join(os.path.dirname(filepath),'images')
    basename = os.path.basename(filepath)

    media_directory = os.path.join(os.path.dirname(col.path),"collection.media")
    print("media directory: ", media_directory)

    print("Opening file %s" % filepath)
    with open(filepath, 'r') as f:
        json_content = f.read()
        doc = json.loads(json_content)
        word = Word(doc)

        fields = {}
        fields["Word"] = word.title()
        fields["example sentence"] = "no example sentence"
        fields["Gender, Personal Connection, Extra Info (Back side)"] = "N/A"

        if word.audio_url():
            filename = "{}".format(word.title())
            possible_extensions = ['ogg', 'mp3']
            for extension in possible_extensions:
                audio_name = filename + '.' + extension
                audio_path = os.path.join(audio_directory, audio_name)
                if os.path.exists(audio_path):
                    source_path = audio_path
                    target_path = os.path.join(media_directory, audio_name)
                    print("Copying media file %s to %s" %
                        (source_path, target_path))
                    col.media.addFile(source_path)
                    #shutil.copyfile(source_path, target_path)
                    fields["Pronunciation (Recording and/or IPA)"] = "[sound:%s]" % audio_name

        if word.image_url():
            image_name = word.title()+".jpg"
            image_path = os.path.join(image_directory, image_name)
            if os.path.exists(image_path):
                source_path = os.path.join(image_directory, image_name)
                target_path = os.path.join(media_directory, image_name)
                print("Copying media file %s to %s" %
                    (source_path, target_path))
                col.media.addFile(source_path)
                #shutil.copyfile(source_path, target_path)
                fields["Picture"] = '<img src="%s">' % image_name

        # Ordered fields as defined in Anki note type

        # Get the deck

        modelBasic = col.models.byName('Picture Words')
        col.decks.current()['mid'] = modelBasic['id']

        deck = col.decks.byName("Russian Test")

        # Instantiate the new note
        note = col.newNote()
        note.model()['did'] = deck['id']

        anki_fields = [
            "Word",
            "Picture",
            "Gender, Personal Connection, Extra Info (Back side)",
            "Pronunciation (Recording and/or IPA)",
            "example sentence"
        ]

        for field, value in fields.items():
            note.fields[anki_fields.index(field)] = value

        # Add the note and save to the database
        col.addNote(note)
        col.save()
        col.close()
        print("added to database")

@eel.expose
def callLoad():
    col = Collection(cpath, log=True)
    json_pattern = "word_data.json"
    main_script_path = module_locator.module_path()
    file_pattern = os.path.join(main_script_path,json_pattern)
    load(col,file_pattern)
 
#function to delete the audio and images folder on startup
@eel.expose
def clearSpace():

    json_pattern = "word_data.json"
    main_script_path = module_locator.module_path()
    file_pattern = os.path.join(main_script_path,json_pattern)
    audio_directory = os.path.join(os.path.dirname(file_pattern),'audio\\').strip()
    image_directory = os.path.join(os.path.dirname(file_pattern),'images\\').strip()
    print(image_directory)
    print(os.path.exists(image_directory))
    if os.path.exists(image_directory):
        shutil.rmtree(image_directory, ignore_errors=True)
        print('initialised')
    if os.path.exists(audio_directory):
        shutil.rmtree(audio_directory, ignore_errors=True)
        print('initialised')

if __name__ == '__main__':
    #Clear the environment
    clearSpace()
    eel.start('index.html', size=(1000, 600))
    #pass