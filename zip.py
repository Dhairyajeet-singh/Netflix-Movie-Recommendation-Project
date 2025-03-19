import pickle
import gzip

# Load existing data
with open("similarity.pkl", "rb") as f:
    data = pickle.load(f)

# Save as compressed gzip file
with gzip.open("similarity.pkl.gz", "wb") as f:
    pickle.dump(data, f)
