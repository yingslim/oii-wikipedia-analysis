# wikipedia_analysis 
This is a group project for OII's social data science class. <br/>

## Research question: 
Does the media play a role in exacerbating social biases during conflicts between major pop stars? <br/>

## Research plan: 
<u>Unit of Analysis:</u> Text data from Wikipedia
<u>Object of Interest:</u> Taylor Swift and Kenya West
<u>Operationalisation:<u>
- Fetch edit histories of page Taylor Swift and Kanye West
- Time series analysis to see how the edit amounts corresponds to their conflicts
- Compare if there’s significant differences on edits / contradictory edits (wiping facts and write in contradictory arguments) between the two
- Whether it Gender bias? racial bias? What kind of bias? 
- Collective memory creation?
- Public sphere to judge public figures?


## Setup your environment

1.Setup python path: ```export PYTHONPATH="scripts"```<br/>
2. Create virtual environment on your termianl: ``` python -m venv .venv```<br/>
3. Install python libraries and dependencies: ```pip install -r requirements.txt``` <br/>
4. Update requirements.txt file, if necessary: ```pip freeze > requirements.txt```


## Folders 
Section describes the project structure of this repository.

### Scripts
Folder contains all of the scripts. 
1. `data_scraper`: to scrape the related dataset from wikipedia.  Data scraped will be sent to `./data` directory directly. Processed DataFrames will be kept in the github, however, raw scraped data is added to .gitignore. You can find the raw data on [our drive](https://drive.google.com/drive/folders/1JdVMY3asgYR94n4M4ifBRCqP4cNXIyu0?usp=drive_link). (It is a large zip file!)
2. `data_processing`: scripts for data processing purposes
3. `data_analysis`: mainly `.ipynb` to visualise graphs/relationships, or to conduct statistical tests.

### Data
Import the scraped data from [our drive](https://drive.google.com/drive/folders/1JdVMY3asgYR94n4M4ifBRCqP4cNXIyu0?usp=drive_link) and upload them in this folder.


### Output
Any files from the analysis will be uploaded in this folder. Upload it on [our drive](https://drive.google.com/drive/folders/1JdVMY3asgYR94n4M4ifBRCqP4cNXIyu0?usp=drive_link) too. 

### Deck
PDF version of our presentation slides.


# wikipedia_project
