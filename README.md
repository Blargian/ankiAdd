# ankiAdd
An application to quickly populate Anki cards for vocabulary. 

05/12/2019

Have added functions to access openrussian db, to obtain pictures using the Pixabay API and to get the pronounciation using the Forvo API. 

07/12/2019 

Fixed some bugs with the fetching of images and pronounciation. 

12/12/2019 

Added GUI functionality using python eel and HTML,CSS,Javascript and Bootstrap. 

13/12/2019

Added Google images API functionality. The images now display in a grid on the page for a desired search term. 

TO DO 
The app works okay as a basic prototype however it has some problems which I would like to improve:
- The database being used is SQL and it's a bit of a pain to set that up. I'd like to migrate it to a mongodb database and then run the whole app using nodeJS.
- I have sphagetti code for the DOM manipulation. I'd like to redo the front end using React and implement state management using Redux. 
- I'd like to try and use electron rather than eel and use a node python plugin for running the python script.
