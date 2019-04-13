This a project repo for game chexers which introduced by course COMP30024 Semester 1

### prepare for part B

- Alpha go related paper
  - [AlphaGo Zero using residual CNN and implement on connect4](<https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188>)
  - [Building Our Own Version of AlphaGo Zero](<https://medium.com/rossum/building-our-own-version-of-alphago-zero-b918642bd2b5>)
  - [original paper for alphaGO](<https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ>)
- Monte Carlo Tree search
  - [550 line python MCTS for go](<https://github.com/pasky/michi>)
- Basic reinforcement learning
  - [Markov Decison Process and Q-learning](<https://itnext.io/reinforcement-learning-with-q-tables-5f11168862c8>)
  - 



### Some idea

- Use residual-CNN with MCST
  - Problems:
    - Need the offline game play engine
    - Need quite long computational power
    - Don't know how to update the hyper-parameters by using the reinforcement learning policy
      - Solution:
        - Not find yet
  - advantages
    - No need of human knowledge
    - Make decision very quick
    
- Min-max algorithms
  - What we learnt on the class
  - Problems
    - How to extend this to multi-agent
      - Using three tuples
        - But decision making process might become really long, so we need to make some cut down rules
    - slow decision making, since we only have 60s computational time overall.
- DQN
  - Haven't have a try yet
- Find Nash equilibrium