"""
This scripts analyzes sentiments of posts. Assumes they are .txt files in a folder called 'downloads'.
"""
from afinn import Afinn
from pathlib import Path
from collections import defaultdict
import pandas as pd

main = defaultdict(list)
for folder in Path('downloads').glob('*'):
    for txt in folder.glob('*.txt'):
        with open(txt, 'r') as f:
            x = f.read()
            main[folder.name].append(x)


df = pd.json_normalize(main).T.explode(0).reset_index()
df = df.drop_duplicates()
df.columns = ['location', 'text']

afinn = Afinn(language='da', emoticons=True)

df['sentiment'] = df.text.apply(afinn.score)

df.to_csv('sentiments.csv', index=False)
