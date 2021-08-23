import pandas as pd

data = pd.read_pickle('complexity_data/complexity_tree_v2.pkl').sample(frac=1)

train_index = int(len(data) * 0.8)

test_data = data[train_index:]
train_data = data[:train_index]

test_data.to_pickle('complexity_data/test.pkl')
train_data.to_pickle('complexity_data/train.pkl')
