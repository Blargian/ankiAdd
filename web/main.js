
// This function takes the word to search and retrieves a list of image urls from Python
// then populates the images on the page as html elements.

function retrieve_images(word) {

    if(word == false){
        return;
    }

    eel.google_image(word)(get_url);

    function get_url(ret){

        google_urls = ret;

        var ele_row = document.getElementsByClassName('row text-center text-lg-left')[0];
    
        for (i=0;i<8;i++){
            var ele_div_outer =document.createElement("div");
            ele_div_outer.className = "col-lg-3 col-md-4 col-6";
            ele_a = document.createElement("a");
            ele_a.className = "d-block h-100";
            var wrapper = document.createElement('div');
            wrapper.className = "view";
            ele_img = document.createElement("img");
            ele_img.className="img-fluid img-thumbnail";
            ele_img.id=String(i);
            ele_img.setAttribute('src', google_urls[i]);
            ele_img.setAttribute('onclick', 'selectImage(this);');
            ele_row.appendChild(ele_div_outer);
            ele_div_outer.appendChild(ele_a);
            var parent = ele_a.parentNode;
            parent.replaceChild(wrapper, ele_a);
            wrapper.appendChild(ele_a);
            ele_div_outer.appendChild(wrapper);
            wrapper.appendChild(ele_img);
            var overlay = document.createElement('div');
            overlay.setAttribute('onclick', 'selectImage(this);');
            overlay.id = "overlay_id"+String(i);
            ele_img.parentNode.insertBefore(overlay,ele_img.nextSibling);
        }
    }
} 

//This function clears the image results 

function clear_images(){
    var ele_row = document.getElementsByClassName('row text-center text-lg-left')[0];
    var child = ele_row.lastElementChild;
    while (child) { 
        ele_row.removeChild(child); 
        child = ele_row.lastElementChild; 
    }
}

//This function is called when the search button is clicked. It formats the search term and then if the
//words does exist in the database it calls the function for the google search and image population. 

function getWord(){

    word = String(document.getElementById("form_word").value);
    word = word.replace(/^\s+/g, '');
    var icon = document.getElementById("icon");
    icon.className = "icon-bubbles m-auto text-primary";
    //put the returned values into html elements
    eel.getData(word)(function(ret) {

        if(ret ==false){
            clear_images();
            return;
        } else{

            document.addEventListener("DOMContentLoaded", function(event) { 
                var word_searched = document.getElementById('word_searched');
                var category = document.getElementById('word_category');
                event.preventDefault()
            });

            word_searched.textContent = ret[0];
            word_category.textContent = ret[1];
            word_translation.textContent = ret[2];

            clear_images();
            retrieve_images(word);
            }
    });

    //eel.get_pronounciation(word);

    // eel.get_image(word)(function(ret){
    //     eel.image_download(ret);
    // });

    //handling of the images
};



//Functions for green overlay on image selection

var selected_before = false;
var previously_selected_id = 11; //should be more than the number of images
var url_selected_image = ""; //Stores the url of the selected image

function selectImage(elem){

//Each img has an ID corresponding to the image number. If a picture is clicked once the element passed to selectImage is 
//an IMG but once the overlay class is applied clicking the image a second time passes a DIV to the selectImage function.
//This part gets the image number to be used further down for checking if that image was previously selected.
    if(elem.tagName == "IMG"){
        var image_no = parseInt(elem.id);
    } else {
        var image_no = parseInt(elem.previousSibling.id);
    }    

//If the image wasn't selected before then apply the class to the overlay, set selected_before == true and then
//set global variable previously_selected_id to the image_no (the image clicked). Return out of the function
//so as not to run the second if statement.

    if(selected_before == false){
        var url_selected_image = elem.src;
      
        var overlay = document.getElementById("overlay_id"+String(image_no));
        overlay.className = "mask flex-center rgba-green-strong";
        selected_before=true;
        previously_selected_id = image_no;
        return
    };

//If the image clicked was already selected then remove the overlay class effectively hiding the
//green overlay. And turn selected_before back to false to enable the process to happen again. 

    if(image_no == previously_selected_id){
        var overlay = document.getElementById("overlay_id"+String(image_no));
        overlay.classList.remove("rgba-green-strong");
        overlay.classList.remove("flex-center");
        overlay.classList.remove("mask");
        selected_before=false;
    };
};

    // eel.get_image(word)(function(ret){
    //     eel.image_download(ret);
    // });
    

