1. indicators.py 
- This file contains the implementation of the indicators. 
- The getsma, getBBP, getMomentum fucntions are used to compute indictaor values & called in other files.

2. marketsimcode.py
- This file contains the market simulator analysis that we did in project 5. 
- The compute_portvals() function is used to evaluate the trades_df that will be returned by Manual Strategy and Strategy Learner  

3. RTLearner.py
- This file contains the implementation of Random Tree Learner. 

4. BagLearner.py
- This file contains the implementation of BagLearner which in turn calls the RTLearner from RTLearner.py

5.ManualStrategy.py
- This file contains the implementation of rule based strategy. Strategy is defined in testPolicy() function.
- This file makes calls to indicators.py for getting indicator info & compute_portvals() from marketsimcode for evaluating the trades_df dataframe generated from the Manual Strategy.
- InSample() and OutOfSample() functions generate the charts and print the metrics for Insample and OutofSample results. 

6. StrategyLearner.py
- This file contains the implementation of StrategyLearner class with add_evidence() and testPolicy() functions
- This file makes calls to indicators.py for getting indicator info, BagLearner.py and RTLearner.py for implementing the Strategylearner.

7. experiment1.py
- This file Compares Manual Strategy, benchmark strategy and Strategy Learner for in-sample trading JPM
- required calls are made to ManualStrategy.py, StrategyLearner.py and marketsimcode
- InSample() function generates all the relevant charts and prints the relevant data

8. experiment2.py
- This file conducts an experiment with StrategyLearner that shows how changing the value of impact should affect in-sample trading behavior 
- required calls are made to StrategyLearner.py and marketsimcode
- test_code() function generates all the relevant charts and prints the relevant data


9. testproject.py 

- This file contains all the necessary calls to 
	a. ManualStrategy.py for generating all the charts & data
	b. experiment1.py for generating all the charts & data
	c. experiment2.py for generating all the charts & data

with the appropriate parameters to run everything needed for the report in a single Python call.


To run the code- 

- We only need to call testproject.py and all the charts and stats will be generated via this file 

  PYTHONPATH=../:. python testproject.py