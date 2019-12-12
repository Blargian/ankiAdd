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

    // eel.get_image(word)(function(ret){
    //     eel.image_download(ret);
    // });

    //handling of the images

    eel.get_image(word)(function(ret) {

        //Create the first row within the div which has id="retrieved_images" and give it an id of row 0.
        // row_number functions as a variable to be incremented when three images have been added per row
        // and used within the naming of rows so that subsequent groups of three images are added to a 
        //new row. 

        var ele_row = document.createElement("div");
        ele_row.className = "row";
        row_number = 0;
        ele_row.id = "row" + String(row_number);

        document.getElementById("retrieved_images").appendChild(ele_row);

        for (i = 0;i < 10; i++) {

            if(i/3 !=1){
                var ele_div = document.createElement("div");
                ele_div.className = "col-md-4";
                ele_div.id = "image_column" + String(i)

                var ele_image = document.createElement("img");
                ele_image.src=ret[i];

                ele_image.width=200;
                ele_image.height=200;

                document.getElementById("row" + String(row_number)).appendChild(ele_div);
                document.getElementById("image_column" + String(i)).appendChild(ele_image);
            } else {
                row_number++;
                var ele_row = document.createElement("div");
                ele_row.className = "row";
                ele_row.id = "row" + String(row_number);
                document.getElementById("retrieved_images").appendChild(ele_row);
            }
        }
    });  
};

    eel.get_image(word)(function(ret){
        eel.image_download(ret);
    });
    

