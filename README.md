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
