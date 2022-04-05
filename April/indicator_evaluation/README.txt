1. indicators.py 

- This file contains the implementation of 5 indicators for Experiment 1. 
- The “main” code i.e. function "test_code_indicators" in indicators.py generates the charts that illustrate the indicators in the report.


2. marketsimcode.py
- This file contains the market simulator analysis that we did in project 5. 
- The compute_portvals() function is used to evaluate the trades_df that will be returned by TOS and Benchmark Strategy. 


3. TheoreticallyOptimalStrategy.py 
- This file contains the implementation of Theoretically Optimal Strategy & Benchmark strategy for Experiment 2.
- It implements testPolicy() which returns a trade_df data frame
- The “main” code i.e. function "compare_tos_vs_benchmark" calls the marketsimcode (function "compute_portvals") to generate the plot and statistics for TOS and Benchmark stategy as present in the report.


4. testproject.py 
- This file contains all the necessary calls to indicators.py & TheoreticallyOptimalStrategy.py with the appropriate parameters to run everything needed for the report in a single Python call.


To run the code- 

- We only need to call testproject.py and all the charts and stats will be generated via this file 

  PYTHONPATH=../:. python testproject.py