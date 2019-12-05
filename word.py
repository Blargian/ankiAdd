class word:

    def __init__(self,word,image,pronounciation,example_sentences,selected_image):
        self.word = word
        self.image = image
        self.pronounciation = pronounciation
        self.example = example_sentences
        self.selected_image

class verb(word):
    
    def __init__(self,word,image,pronounciation,example_sentences,aspect):
        super().__init__(word,image,pronounciation,example_sentences,aspect)
        self.aspect = aspect

