# wikipedia_analysis 
This is a group project for OII's social data science class. <br/>

## Research question: 
How do celebrities' social events influence content curation on Wikipedia? <br/>
- Hypothesis 1: Major events amplify the breadth of the information network surrounding a celebrity, as evidenced by a complexified interlinked information source network.
- Hypothesis 2: Major events enhance the velocity of information curation, as evidenced by a frequency increase in Wikipedia page edits.

## Research plan: 
**Unit of Analysis**: Wikipedia edit <br/>
**Object of Interest**: 
1. Velocity of information curation from celebrities’ activity -> edit frequency
2. Width of information creation from celebrities’ activity -> number of interlinked internal/external information sources

**Operationalisation**:
1. Fetch edit histories of page Taylor Swift and Kanye West
2. Time series analysis to see how the edit amounts corresponds to their conflicts
3. Compare if there’s significant differences on edits / contradictory edits (wiping facts and write in contradictory arguments) between the two
   - Collective information creation reflected through the proliferated interlinks.
4. Editor analysis, common editors updating both public figures' pages


## Setup your environment
1. Create virtual environment on your termianl: ``` python -m venv .venv```<br/>
2. Install python libraries and dependencies: ```pip install -r requirements.txt``` <br/>
3. Update requirements.txt file, if necessary: ```pip freeze > requirements.txt```


## Folders 
Section describes the project structure of this repository.

### Scripts
Folder contains all of the scripts. 
2. [data_scraper](scripts\data_scraper\README.md): To scrape the related dataset from wikipedia.  Data scraped will be sent to `./data` directory directly (scraped XML files and processed DataFrames). You can find the raw data on [our drive](https://drive.google.com/drive/folders/1JdVMY3asgYR94n4M4ifBRCqP4cNXIyu0?usp=sharing). (Warning: It is a large zip file!)
2. [utils](scripts\utils\README.md): Contains helper functions to import data, plot graphs and for data processing purposes
3. `data_analysis.ipynb`: To visualise graphs/relationships.

### Data
Import the scraped data from [our drive](https://drive.google.com/drive/folders/1JdVMY3asgYR94n4M4ifBRCqP4cNXIyu0?usp=drive_link) and upload them in this folder.

### Network
Contains the gephi format to plot the network.

### Output
Contains png and html of plots

### Deck
PDF version of our presentation slides.
