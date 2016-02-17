# airscribe

### Inspiration
Medical hospitals often conduct “discharge interviews” with healing patients deemed healthy enough to leave the premises. The purpose of this test is to determine what accommodations patients will require post-hospital-admittance. For instance, elderly patients who live in multi-level houses might require extra care and attention. The issue, however, is that doctors and nurses must conduct such interviews and then spend about 30 to 40 minutes afterwards documenting the session. This is an inefficient use of time. A faster, streamlined system would allow medical professionals to spend their time on more pressing matters, such as examining or interviewing more patients.

### What it does
Airscribe is a smart, automated interview transcriber that is also able to do a cursory examination of the exchange and give recommendations to the patient. (We don’t intend for this to be the sole source of recommendations, however. Doctors will likely review the documents afterwards and follow up accordingly.)

### How we built it
Speech-to-text: built on IBM Watson.

Text-to-better-text: Interviewer and patient’s comments are processed with a Python script that breaks text into Q & A dialogue. Algorithm evaluates patient’s response to find key information, which is displayed in easy-to-read, standardized survey format. Based on patient’s responses to questions, suggestions and feedback for the patient after hospital discharge are generated.

### Challenges we ran into
Getting speech recognition to work, recognizing question types, recognizing answer types, formatting them into the HTML.

### Accomplishments that we're proud of
After talking with health professionals we decided this idea was a better direction than our first idea and completed it in 8 hours.

### What we learned
Teamwork! Javascript! Python! Web development for mobile is difficult (* cough * phonegap) !

### What's next for Airscribe
- Smarter, more flexible natural language processing.
- Draw from a database and use algorithms to generate better feedback/suggestions.
- A more extensive database of questions.

### Built With
- python
- javascript
- amazon-web-services
- css
- bluemix
- ibm-watson
- html5

### How To Use
You can download and use it yourself on your local machine but seeing as how it's specifically running on our AWS server it probably won't work unless you set it up yourself. Run app.py and airscribe.py on your machine.
