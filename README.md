# KAIST Interview Mini-coding Task
## Project 1: Natural Language Tool for Charts

- **Goal**: Extract the displayed data of a Vega-Lite specification as a table as well as the chart encodings (e.g., population → y-length, age → x-position). 
- **Paper reference:** Kim, Dae Hyun, Enamul Hoque, and Maneesh Agrawala. "Answering questions about charts and generating visual explanations." Proceedings of the 2020 CHI conference on human factors in computing systems. 2020. 

- [x] Extract raw data and encoding.
- [x] Extract raw data (.csv) and encoding.
- [x] Transform data based on 'encoding' only.
    - [x] Encoding: Aggregation
        - [x] Basic two column aggregation (categorical and numerical).
            - [x] Supported with third grouping (color).
        - [x] Binning aggregation (categorical with count).
            - [x] Supported with third grouping (color).
        - [x] Time unit aggregation.
            - [x] Year
            - [x] Quarter
            - [x] Month
            - [x] Date
            - [ ] Supported third grouping (color).
    - [x] Encoding: No Aggregation
        - [x] Basic two column (both numerical).
        - [x] No aggregation with third gruoping (color).
- [ ] Transform data based on 'transform'

## How to Use
This web application allows users to convert Vega-Lite specifications into Vega specifications. It also provides the option to include CSV data in the conversion process.

To use this application, follow these steps:

1. Clone this repository to your local machine using Git.
`https://github.com/ardhanidzaky/kaist_intv.git`

2. Create a Python virtual environment for the project using your preferred tool (e.g. venv or conda).
`python3 -m venv myenv`

3. Activate the virtual environment.
`source myenv/bin/activate`

4. Install the required packages from the requirements.txt file.
`pip install -r requirements.txt`

5. To run the application, start the development server with the following command:
`python3 manage.py runserver`

Then, open your web browser and go to http://localhost:8000/. You should see the homepage of the Vega-lite Specification Converter. Follow the instructions on the page to convert your Vega-Lite specifications.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Dataset
Dataset used for testing is available on **./dataset**