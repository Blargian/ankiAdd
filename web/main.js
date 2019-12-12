document.addEventListener("DOMContentLoaded", function(event) { 
    var word_searched = document.getElementById('word_searched');
    var category = document.getElementById('word_category');
    event.preventDefault()
});


function getWord(){
    word = String(document.getElementById("form_word").value);
    word = word.replace(/^\s+/g, '');
    //put the returned values into html elements
    eel.getData(word)(function(ret) {
        var word = ret[0];
        var category = ret[1];
        var translation = ret[2];
        word_searched.textContent = word;
        word_category.textContent = category;
        word_translation.textContent = translation;
    });
    console.log("got here")
    eel.get_pronounciation(word);
    eel.get_image(word)(function(ret){
        eel.image_download(ret);
    });
    
}