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
      *	*This involves actually trading in the market, which can be extremely expensive*
      *	*This can also be done in a backtesting environment, but would still need to happen in the live market in order to run the model as the backtest has ran it*
    *	Updating Q
  *	The success of Q-Learning depends on the exploration of actions, since at the end of one training loop the Q table is updated with the result.  Results should be weighted, giving more weight to recent rewards and less weight as time passes.
  *	**Determining S can be done via a massive array of inputs that I will elaborate on further, with some hypotheticals.**



## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_