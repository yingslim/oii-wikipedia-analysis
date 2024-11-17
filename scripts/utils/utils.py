
import pyarrow.feather as feather
import pandas as pd
import re

#write helper function
def read_feather_in_chunks(file_path, chunk_size):
    table = feather.read_table(file_path)
    df = table.to_pandas()
    total_rows = len(df)
    for start in range(0, total_rows, chunk_size):
        yield df[start:start + chunk_size]


def read_feather_data(file_path, chunk_size=2000):
    chunks = []
    for chunk in read_feather_in_chunks(file_path, chunk_size):
        chunks.append(chunk)
    output = pd.concat(chunks, ignore_index=True)
    return output


def preprocess(content):
    #remove unncess characters
    to_remove = ['url','https','org','cite','Cite','status','archive','web','title','access','date','ref','January','February','March','April','May','June','July','August','September','October','November','December']
    content = re.sub(r'\\[a-z]+\d*', '', content)
    content = re.sub(r'{|}', '', content)
    content = re.sub(r'\\\'..', '', content)
    content = re.sub(r'\s+', ' ', content)
    start = content.find("Taylor Alison Swift")
    content = content[start:] if start != -1 else content

    for word in to_remove:
        content = content.replace(word, '')

    return content