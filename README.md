# KAIST Interview Preparation
## Project 1: Natural Language Tool for Charts

- **Goal**: Extract the displayed data of a Vega-Lite specification as a table as well as the chart encodings (e.g., population → y-length, age → x-position). 
- **Paper reference:** Kim, Dae Hyun, Enamul Hoque, and Maneesh Agrawala. "Answering questions about charts and generating visual explanations." Proceedings of the 2020 CHI conference on human factors in computing systems. 2020. 

- [x] Extract basic data and encoding.
- [x] Extract basic data (.csv) and.
- [ ] Transform data (.csv) based on encoding.
    - [ ] Encoding: 'aggregate'.
    - [ ] Encoding: 'timeUnit'.
- [ ] Supported mark.
    - [x] Mark: 'bar'.
    - [ ] Mark: 'point'.
    - [ ] Mark: 'line'.