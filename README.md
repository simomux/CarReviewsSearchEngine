# Project for the Information Management Exam A.Y. 2023/2024

## Modules Content

### `main.py`
Creates approximately 300,000 files from a specified `.csv` file given as the first argument and stores them in a directory specified as the second argument. Each file corresponds to a line in the `.csv` file, with each argument separated by a newline. This forms the base dataset for the creation of the inverted index.

### `concurrent.py`
Since `main.py` has to create a large number of files and has a linear time complexity cost of O(n), this is a parallel version of the script that utilizes threads to parallelize the computation, reducing the time by approximately 33%. This conclusion is based on various tests conducted on different PCs.

### `index_generator.py`
This script creates the inverted index from the files generated with `main.py`, taking the directory of the files as the first argument. The inverted index is then saved in the current directory.

TODO:
- Fix DATETIME type for the `<date>` argument in the index scheme.

### `query.py`
This script prompts the user for a query input and returns the results using the BM25F model, *for now*.

TODO:
- Finish tuning the model.

Project Members: Mussini Simone, Siena Andrea, Stomeo Paride