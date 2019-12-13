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

    eel.get_pronounciation(word);

    // eel.get_image(word)(function(ret){
    //     eel.image_download(ret);
    // });

    //handling of the images

    eel.google_image(word)(function(ret) {

        if(String(ret)=="False"){
            console.log("No results found");
        }

        var ele_row = document.getElementsByClassName('row text-center text-lg-left')[0];
        console.log(ele_row);
        
        for (i=0;i<8;i++){
            var ele_div_outer =document.createElement("div");
            ele_div_outer.className = "col-lg-3 col-md-4 col-6";
            ele_a = document.createElement("a");
            ele_a.className = "d-block mb-4 h-100";
            ele_img = document.createElement("img");
            ele_img.className="img-fluid img-thumbnail";
            ele_img.setAttribute('src', ret[i]);
            ele_row.appendChild(ele_div_outer);
            ele_div_outer.appendChild(ele_a);
            ele_a.appendChild(ele_img);
        }

    });  
};

    // eel.get_image(word)(function(ret){
    //     eel.image_download(ret);
    // });
    

