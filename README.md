
-------------
REQUIREMENTS
-------------

Given the following JSON data
>

    [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 },
    { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 },
    { "Gender": "Male", "HeightCm": 180, "WeightKg": 77 },
    { "Gender": "Female", "HeightCm": 166, "WeightKg": 62},
    {"Gender": "Female", "HeightCm": 150, "WeightKg": 70},
    {"Gender": "Female", "HeightCm": 167, "WeightKg": 82}]
    
    as the input with weight and height parameters of a person, we have to perform
    the following:
        
        1) Calculate the BMI (Body Mass Index) using Formula 1, BMI Category and Health risk from Table 1 of the person 
        and add them as 3 new columns.
        2) Count the total number of overweight people using ranges in the column BMI
        Category of Table 1, check this is consistent programmatically and add any other observations in the documentation.
        3) Create build, tests to make sure the code is working as expected and this can be added to an 
        automation build / testing / deployment pipeline.

----------
USE-CASES
----------

>
    - Ability of the System to take user-inputs via a *json* file
    - Ability of the System to parse the *json* file and load records in-memory
    - Ability of the System to parse each record, refer to BMI Table and add details such as;
        - BMI Category
        - Health Risk
    - Ability of the System to store modified records into an Elastic-search index
    - Ability of the System to parse the calculated index and store all overweight people into new index
    - Ability of the System to be deployed as Containers/PODS
    - Ability of the System to process millions of records in an optimized manner

------------------------------
FORMULAS FOR BMI CALCULATIONS
------------------------------
>
    BMI(kg/m2) = mass(kg) / height(m)2

-------------------------
BMI CALCULATIONS EXAMPLE
-------------------------
>

    The BMI (Body Mass Index) in (kg/m2) is equal to the weight in kilograms (kg)
    divided by your height in meters squared (m)2. 
    For example, if you are 175cm (1.75m) in height and 75kg in weight, 
        - you can calculate your BMI as follows: 
            - 75kg/ (1.75m²) = 24.49kg/m²

-----------------------------------
BMI TABLE - CATEGORY - HEALTH RISK
-----------------------------------
>
    BMI-Category    BMI-Range(kg/m2)    Health-risk
    ------------    ----------------    ------------

    Underweight    | 18.4 and below   |   Malnutrition risk
    Normal weight  | 18.5 - 24.9      |   Low risk
    Overweight     | 25 - 29.9        |   Enhanced risk
    Moderately-obese | 30 - 34.9      |   Medium risk
    Severely-obese  | 35 - 39.9       |   High risk
    Very-severely-obese | 40 & above  |   Very high risk

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-----------------
TECHNOLOGY STACK
-----------------
>
    Programming - Python3
    Database - Elasticsearch (Can store several millions of records, search is optimized)
    Reports - Kibana
    Deployments - Dockers & K8s
    Unit-Testing - Pytests
    Code Repository - Github
    Docker Registry - docker.io

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

----------
ALGORITHM
----------
>
    ~ Run the solution as a Docker Image.
    ~ Read the contents of the *json* file input into memory.
    ~ Flush the following indexes before execution - (bmi-modified,bmi-results) .
    ~ Store the contents of the *json* file into in-memory for faster operations.
    ~ For each record in the json
        ~   Calculate the BMI (Body Mass Index) using Formula 1.
        ~   Refer BMI Category and Health risk from Table 1 of the person and add them as 3 new columns to the same record.
    ~ Push the modified records to a separate index (bmi-modified).
    ~   Count the total number of overweight people using ranges in the column BMI
        Category of Table 1 and push to a separate index (bmi-results).

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

---------------
EXECUTION STEPS
---------------

>
    Please run the module as follows to input the *json* file and receive the output

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
