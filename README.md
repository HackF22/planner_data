# Data

## Usage

### `SetupMongodb.ipynb`

1. Empty the "requirement", "course", "major" and "wildcardcourse" collections.
1. Import the raw data into "requirement", "course" and "wildcardcourse" collections.
1. Change MongoClient() argument.
1. Change db database name in the line db = client["dbname"].
1. Run all the cells in the notebook.


## Caveats

* The biological sciences component in the CS Lab Sciences has not yet been
properly modelled.
* The 300+ and 400+ courses also contain the 600 level courses. This is yet
to be verified.

## Bugs

* Clear Courses.json before running Courses.py
