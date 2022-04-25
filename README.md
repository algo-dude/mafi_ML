<h1 align="center">Welcome to UNCC MAFI Machine Learning Independent Study Spring 2022 👋</h1>
<p>
  <a href="https://twitter.com/algo\_seth" target="_blank">
    <img alt="Twitter: algo\_seth" src="https://img.shields.io/twitter/follow/algo\_seth.svg?style=social" />
  </a>
</p>

> Materials and findings from GA Tech's CS7646 course and varios other resources and papers

## Author

👤 **Seth Lingafeldt**

* Twitter: [@algo\_seth](https://twitter.com/algo_seth)
* Github: [@algo-dude](https://github.com/algo-dude)
* LinkedIn: [@sethlingafeldt](https://linkedin.com/in/sethlingafeldt)

## Takeaways from CS7646, not ordered:  

*	GA Tech’s CS7646 ML4T course had amazing YouTube lectures and tons of content that I will keep in my work related notebook.  My handwritten notes are in the PDF file on my GitHub.
https://lucylabs.gatech.edu/ml4t/
* They use stock data from 2000 – 2012.  In my experience, this can only be used to teach basic concepts and holds little value for system development, particularly with ML-based systems.  See below:
* I’m pasting in my notes here on technical analysis because I loved the material and how it was delivered.
![](/images/notes1.png)
* Technical analysis typically provides more value the shorter the time horizon gets.  A perfect example of this is the differences between Renaissance Technologies and Warren Buffet, whom, in the real world, have similar performance.
![](/images/notes1.png)

* With the addition of more market participants, old techniques do not work.  Larry Connors’s “RSI(2)” trading system no longer works, but was once heralded as a magic pill for TA traders.
  * https://www.qmatix.com/ConnorsRSI-Pullbacks-Guidebook.pdf
* TA indicators, such as the RSI, are typically weak today when used on its own.  Combinations of these indicators are much stronger, but still work better for shorter periods.
* The ease of use of any machine learning based system is inversely proportional to the extractable value, particularly when taking into account data ingestion.

## The Financial Markets as a Reinforcement Learning Environment  

* The three main choices before a model can be ran must be accounted for:
  * The data: How to sample, concatenate, process, and feed it to the DRL agent in order to determine the State.
  * The actions: What can the agent do at any point in time?  Simple examples = [buy, sell, hold].  Complicated actions = [rebalancing, pyramiding, hedging, changing stop loss or take profit targets, write an option, etc…].
  * The reward: Sharpe ratio or current balance are typical.

#### Q-Learning  

* Q-Learning, a type of reinforcement learning, is the typical “trade simulation” method.  
* I have been the most interested in Q-Learning, because it can be used in a backtest framework, although I have not had success with it on the data sources that I currently use and am familiar with.
  * It relies on creating a table: ∏(S) = Policy for state (S). 
  * ∏(S) maximizes the perceived outcome of state S by performing an action, A.
      * A is found by searching the “Q-Table” of possible actions.
  *	Training the Q-Table involves:
    *	Setting a start time and initiating Q
    *	Q = immediate reward + discounted reward
    *	Computing S (determine the current market state)
    *	Selecting A via consulting Q: Q represents the value of taking action A in state S
    *	Observing the experience (result) and the modified state after action A was taken
      *	*Note: This involves actually trading in the market, which can be extremely expensive*
      *	*Note: This can also be done in a backtesting environment, but would still need to happen in the live market in order to run the model as the backtest has ran it*
    *	Updating Q
  *	The success of Q-Learning depends on the exploration of actions, since at the end of one training loop the Q table is updated with the result.  Results should be weighted, giving more weight to recent rewards and less weight as time passes.
  *	**Determining S can be done via a massive array of inputs that I will elaborate on further, with some hypotheticals.**

#### Dyna-Q  

* Dyna-Q is a way to speed up Q-Leaning by “hallucinating experiences” between real events.  It is quite clever. 
  * After every iteration of Q-Learning, training Dyna-Q involves:
    *	Choosing a random state S and action A
    *	Inferring the result of the hallucinated state and action
    *	Updating Q
    *	Repeating 100x/200x between each iteration of standard Q-Learning
  *	This act of inference is commonly weighted less than actual market interaction.  
    * The value placed on this inference must be discounted in some way to differentiate it from the actual market, because it may or may not be “true”.
*	Dyna-Q is computationally expensive, but not monetarily.  If this is being deployed in continuous time (live), then it can be extremely costly.

## Market State

*	Ultimately, the State prediction, S, is where models win or lose when deployed.
*	Many other ML models use a state variable.
  *	S can be categorized by Close/MA, BB value, P/E ratio, simulation current holdings, return since entry, or many other simple numerical observations based on price or fundamental data.
    *	*Double dipping would include using other ML algorithms such as NLP or sentiment analysis to infer some additional information about the market that can then be discretized as some numerical value.*
    * **I suspect this is where the largest amount of edge is for any trading system which incorporates a ML based agent.**

## Portfolio Management

* Most of the public knowledge of active machine learning techniques being applied to the market are in regards to portfolio management and/or rebalancing.  
  *	This will typically be done with some kind of “uncertainty” variable that is associated with the estimated State.  Higher uncertainty can, for instance, lead to a smaller position size.
*	Sharpe, unsurprisingly, seems to be the most common risk reward measurement.

## Takeaways from varios papers

*	Multiple markets are not typically used – likely this is because it is out of the research scope when a project begins.  This makes me quite hesitant on usability of results unless there is a significant economic explainable reason behind it.  If someone argued “cryptocurrency ML trading systems won’t work on fixed income products because they are far less volatile and move much slower”, I would agree with said statement, but if something works in the FX markets, I would also want to see it on equity indexes, for example.
*	There is no consistency among the environments.  Some model with transaction costs and market friction, some ignore it.  Some allow short selling, others ignore it.
*	Everyone is using different datasets, so it is hard to compare between multiple papers.
*	**VERY FEW papers and projects have code available online.  Almost all of it is proprietary.  I can’t fault them for this.**

## Papers, but not inclusive

1.	Rundo, F. Deep LSTM with reinforcement learning layer for financial trend prediction in FX high frequency trading systems.  Appl. Sci. 2019, 9, 4460.
2.	Huotari, T.; Savolainen, J.; Collan, M. Deep reinforcement learning agent for S&P 500 stock selection. Axioms 2020, 9, 130.
3.	Tsantekidis, A.; Passalis, N.; Tefas, A. Diversity-driven knowledge distillation for financial trading using Deep Reinforcement Learning. Neural Netw. 2021, 140, 193–202.
4.	Wu, M.E.; Syu, J.H.; Lin, J.C.W.; Ho, J.M. Portfolio management system in equity market neutral using reinforcement learning.  Appl. Intell. 2021, 51, 8119–8131
5.	Millea, A. Deep Reinforcement Learning for Trading—A Critical Survey. Data 2021, 6, 119. 
6.	He, X.; Zhao, K.; Chu, X. AutoML: A Survey of the State-of-the-Art. Knowl.-Based Syst. 2021, 212, 106622.
7.	Jiang, Z.; Xu, D.; Liang, J. A deep reinforcement learning framework for the financial portfolio management problem. arXiv 2017, arXiv:1706.10059.
8.	Lucarelli, G.; Borrotti, M. A deep Q-learning portfolio management framework for the cryptocurrency market. Neural Comput. Appl. 2020, 32, 17229–17244.
9.	Mosavi, A.; Faghan, Y.; Ghamisi, P.; Duan, P.; Ardabili, S.F.; Salwana, E.; Band, S.S. Comprehensive review of deep reinforcement learning methods and applications in economics. Mathematics 2020, 8, 1640.

## CS7646 monthly folders:

1) Jan

  * Most of January was spent discovering that there was no good equity portfolio backtesting framework in the public domain written in python.  I still use RealTest for my equity research.

2) Feb

  * I  spent time working on the IAQF project where we implremented a HMM hidden state model to predict the market state.  It did fairly well.  Date on X axis is not included, but you can see the GFC in 2008 is where the states diverge.  We saw little value in the three state model, so we took two states to the production code  See image:
  * ![](/images/hmm.png)
  * In February I started the CS7646 course and began taking notes and working through some of the material.  I did not upload the practice code for some simpler ML learnign algorithms such as bag learner.

3) March

  * CS7646 lectures were completed.  See file: /March/GATECH-CS7646-ML4T.pdf
  * Lots and lots of Python practice.

4) April

  * A Q-learning robot that navigates a "maze":
      * ![](/images/qlearning_robot.gif)
  * Coding indicators without a TA library
      * ![](/images/Indicator2_BB.png)
  * Comparing a theoretically optiomal strategy
    



## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_