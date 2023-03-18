# Body-status
#### Video Demo:  <URL https://youtu.be/hPLGq8xA248>
#### Description:
### Summary
The "Body Status" web app allows users to log their medical symptoms to create a history for future reference. It uses a red marker to visualize the user’s mouse click for yet to be submitted new entries, orange color for already submitted current symptoms and blue markers for archived ones. Clicking on an existing marker highlights it. Users can hide/show history as well as edit, archive, activate and delete entries.

The app was created using skills and knowledge acquired while working on pset 9 “finance”. It allowed me to play around with image positioning on the web page and understand how coordinates of a mouse click are obtained. I also experimented with changing the style of different elements in response to those clicks, i.e. changing position, showing and hiding, altering the border property etc.

Admittedly, I do not yet have a full grasp of html, css and js. I should have definitely avoided using inline styling and putting "script" inside of the "body", but due to lack of experience at this stage I stopped optimizing when the app worked properly. There is definitely a room for improvement, but I decided to submit this version because ideas on how to improve and add new features kept pouring in and I was just afraid they would break the app.

### Folders and files
"static" folder contains images that are used by the application: 
- female0.png, male1.png and other.png represent the background image according to the user’s choice during registration
- marker.jpg, marker_blue.jpg and marker_red.jpg are used to visualize placing a marker on top of a background image
- script.js contains some, but not all of the javascript code. More specifically, how to obtain coordinates of a mouse click (found using google) and change some css properties and form values.
- styles.css contains styling properties for different elements, ids and classes

“templates” folder contains the following:
- index.html - the main page where everything is happening. It uses jinja syntax at the beginning to determine which image to show as a background. Then it adds hidden markers, which later will be used for visualizing mouse clicks and representing data from the database with the help of js. There is a main form where users input the info as well as some hidden forms with buttons “Delete”, “Archive” and “Activate”. Further down goes the js code to connect the SQL database with the page as well as what to show to and what to hide from the user based on page interactions.
- layout.html - a template containing the header with nav links using jinja syntax to display the relevant ones.
- login.html - a page with a for logging in
- register.html - a page with a form for registering a new user

Files in the root folder:
- app.py - the file where all the back-end logic is written. Some functions like “register”,  “login”, “login_required” and “logout” are borrowed from the “finance” pset and adapted for this application. “processUserInfo” function is written using google search. “submit” function responds to the “Submit” button and either inserts or updates the database. So do the “delete”, “archive” and “activate” functions. “index” function loads the homepage and SELECTs all the necessary data from the status.db file and sends it with the index.html template.
- requirements.txt - states which packages the application needs from PyPI (Python main package repository) in order to be able to run.
- status.db - the database file containing tables “users” and “symptoms”. The first one is used to store unique id, username, hash of a password and gender. The second one contains all the users’ symptoms, coordinates for markers, datetimes, notes and whether the symptom is archived or not.

### Conclusion
There are several possible applications for my work, like for example using it as a page in the user’s account of some hospital to visualize current and past injuries, symptoms, sensations etc. It can also be a personal log to create a bigger picture of the user's body condition and experiences. It can also be overhauled to represent markers on some other background image like notes of where the scratch on a car is or a place on a map.
