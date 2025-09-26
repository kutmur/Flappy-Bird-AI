# Flappy Bird AI 

## Overview  
This project is an **AI-powered Flappy Bird** game where you can **play manually** or let an AI agent **learn and play** using **Reinforcement Learning (Deep Q-Learning / PPO).** The AI continuously improves its gameplay through training.  

## Features  
-  **Play Manually** – Control the bird using the spacebar 
-  **AI Mode** – The AI learns & plays Flappy Bird automatically 
-  **Scoreboard** – Displays current and best scores 
-  **Main Menu** – Choose to play manually, watch AI, or quit  
-  **Reinforcement Learning** – AI trains using **Stable-Baselines3 (PPO)**  

## AI Training  
- The AI is trained using **PPO (Proximal Policy Optimization)** with a custom Flappy Bird environment.  
- The training process **rewards survival** and **penalizes crashing.**  
- After **training for thousands of timesteps**, the AI learns to navigate through pipes.  

## Project Structure  
```
Flappy-Bird-AI/
│── assets/          # Game assets (bird, pipes, background)
│── models/         # Trained AI models
│── src/             # Main source code
│   │── main.py      # Game logic + AI integration
│   │── flappy_env.py # Custom Flappy Bird Gym environment
│   │── train_ai.py  # AI Training script
│── README.md       # Project documentation
│── requirements.txt # Dependencies
```

## Installation  
Clone the repository and install dependencies:  
```bash
git clone https://github.com/EXPERT2007/Flappy-Bird-AI.git
cd Flappy-Bird-AI
pip install -r requirements.txt
```

## How to Play  
Run the main game file:  
```bash
python src/main.py
```
### Controls:  
- **Press 1** → Play manually (spacebar to jump)  
- **Press 2** → Let the AI play  
- **Press Q** → Quit  

## Train AI  
If you want to train the AI from scratch, run:  
```bash
python src/train_ai.py
```
This will generate a trained model in the `models/` folder.  

## AI Performance  
- AI learns through **Deep Reinforcement Learning**  
- The model improves as training continues  
- You can train longer for a smarter AI  

## ⚡ Future Improvements  
- 🚀 Enhancing AI intelligence  
- 📊 Adding difficulty levels  
- 🎨 Improving visuals  
- 🎵 Adding sound effects  

## 🤝 Contributions  
Feel free to fork this repo, improve the AI, and submit pull requests!  

## 🐟 License  
This project is **MIT licensed.**

