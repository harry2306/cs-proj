# Reinforcement Learning Pool AI
### Goal: Train an agent to learn how to play pool by trial and error. 
Description: Using a pool engine contructed from scratch using the Pygame and Math module, a agent will learn to finish a solo game of pool by following a reinforcement learning procedure, enumerated below:

table state $\to$ agent chooses a shot $\to$ pool engine simulates the physics $\to$ reward $\to$ new table state

General Objective:
1. Pool Scenary
2. Implement the classes and internal structure
3. Implement an approximation of pool physics
4. Create a reinforcement learning enviroment
5. Train an agent to pocket balls
6. Experimentation and Evaluation

File System:
```text
pool-rl-agent/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── main.py
├── train.py
├── watch_agent.py
│
├── engine/
│   ├── __init__.py
│   ├── ball.py
│   ├── table.py
│   ├── collision.py
│   ├── physics.py
│   ├── pool_engine.py
│   └── renderer.py
│
├── rl/
│   ├── __init__.py
│   ├── pool_env.py
│   ├── rewards.py
│   ├── observations.py
│   └── actions.py
│
├── models/
│   └── .gitkeep
│
├── logs/
│   └── .gitkeep
│
└── tests/
    ├── test_engine.py
    └── test_env.py
```

## Implementation Techniques

### Reinforcement Learning with PPO

This project will use **Proximal Policy Optimization (PPO)** to train the learning agent. PPO is a reinforcement learning algorithm that is commonly used for environments with continuous action spaces, making it a good fit for this project because a pool shot can be represented by continuous values such as angle and power.

A good idea would be to begin will be to proceed evalulation with a single ball and see how it preforms on this simple case. 

### Packages
1. Stable_Baselines3
2. Gymanasium
   Gymnasium is the communication system between the engine software and an
reinforcement learning algorithm. 

|Learning Agent| -> |gymnasium| -> |engine| \\
  \uparrow                                   |
  |_  _  _  _   _    _   _   _   _   _|
            closed loop
There are several abilities that gymansium need to 
be able to do:
1. rest your enviroment
4. Numpy

### Task 1:
For a solo pool game the AI engine should be able to command a shot based on two parameters [angle,power]


