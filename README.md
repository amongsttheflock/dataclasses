**SOLUTION:**
Run logic.py with python 3.7 and packages installed from requirements.txt


Having a data scheme (global_data_scheme):
1. Combine data from 3 sources:
    a. cities.json
    b. parks_and_recreations_info.json
    c. traffic_info.json

2. The data sets may contain errors - handle them in the best manner you see fit
    a. Assuming that the data set is a valid json file, the application must not crash or stop working if an error is spotted in some specific data entry

3. Propose and implement a text utility for displaying this data in a most ergonomical way
    or

4. Implement filtering engine that given a list of filters like in example_filters.json will find and print all entities that match provided filtering criteria.
    a. path to a filtered element is provided with a simple json-pointer syntax
    b. numerical types must support following filters
      * eq - equal to
      * ge - greater or equal
      * le - less or equal
      * lt - less than
      * gt - greater than
      * in - within a <min, max> bounds
    c. string types must support a full regular expression match
