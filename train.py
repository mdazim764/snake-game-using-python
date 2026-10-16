import numpy as np
import pygame
from snake_env import SnakeEnv
from q_agent import QLearningAgent

def train_and_benchmark():
    episodes = 1000
    # Step 1: Fast Training ke liye render_mode=False rakha hai
    env = SnakeEnv(render_mode=False)
    agent = QLearningAgent(
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_decay=0.992,
        epsilon_min=0.01
    )

    scores = []
    max_score = 0

    print("==========================================")
    print("🚀 Starting Q-Learning Training (1000 Episodes)...")
    print("==========================================")

    for ep in range(1, episodes + 1):
        state = env.reset()
        done = False

        while not done:
            action = agent.get_action(state, train_mode=True)
            next_state, reward, done, score = env.step(action)
            agent.learn(state, action, reward, next_state, done)
            state = next_state

        agent.decay_epsilon()
        scores.append(score)
        if score > max_score:
            max_score = score

        # Har 100 episodes par progress print karo
        if ep % 100 == 0:
            avg_score = np.mean(scores[-100:])
            print(f"Episode {ep:4d}/{episodes} | Avg Score (Last 100): {avg_score:5.2f} | Max Score: {max_score:2d} | Epsilon: {agent.epsilon:.3f}")

    # Save trained Q-table for Task 4 & Task 5
    agent.save_model("q_table.pkl")

    # Optional: Save training graph if matplotlib is installed
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 4))
        plt.plot(scores, color='lightgreen', alpha=0.4, label='Episode Score')
        moving_avg = np.convolve(scores, np.ones(50)/50, mode='valid')
        plt.plot(range(49, len(scores)), moving_avg, color='green', linewidth=2, label='50-Episode Moving Avg')
        plt.title("Q-Learning Snake Agent - Training Progress")
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig("training_curve.png")
        print("[SUCCESS] Training graph saved as 'training_curve.png' (Presentation ke kaam aayega!)")
    except ImportError:
        print("[INFO] matplotlib installed nahi hai, graph skip kiya gaya.")

    # Step 2: Live Visual Benchmark of Trained Agent
    print("\n🎮 Launching Live Visual Demo of Trained Agent (3 Episodes)...")
    demo_env = SnakeEnv(render_mode=True)
    for demo_ep in range(1, 4):
        state = demo_env.reset()
        done = False
        while not done:
            # train_mode=False ka matlab 100% pure Q-table dimaag use karega
            action = agent.get_action(state, train_mode=False)
            state, _, done, score = demo_env.step(action, fps=25)
        print(f"🔥 Trained AI Demo Episode {demo_ep} | Final Score: {score}")

    pygame.quit()

if __name__ == "__main__":
    train_and_benchmark()