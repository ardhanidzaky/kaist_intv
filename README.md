# KAIST Interview Preparation
## Project 1: Natural Language Tool for Charts

- **Goal**: Extract the displayed data of a Vega-Lite specification as a table as well as the chart encodings (e.g., population → y-length, age → x-position). 
- **Paper reference:** Kim, Dae Hyun, Enamul Hoque, and Maneesh Agrawala. "Answering questions about charts and generating visual explanations." Proceedings of the 2020 CHI conference on human factors in computing systems. 2020. 

- [x] Extract raw data and encoding.
- [x] Extract raw data (.csv) and encoding.
- [ ] Transform data based on 'encoding' only.
    - [ ] Encoding: 'aggregate'.
        - [x] One column aggregation.
        - [ ] Two column aggregation
    - [x] Encoding: 'timeUnit'.
        - [x] Year
        - [x] Quarter
        - [x] Month
        - [x] Date
        - [x] Week
- [ ] Transform data based on 'transform'