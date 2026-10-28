# 🐍 Agentic Snake

> A Pygame-powered Snake game and reinforcement-learning laboratory with
> classic gameplay, Q-learning, human-vs-AI battles, adversarial interference,
> and AI-versus-AI comparison modes.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00A86B?logo=python&logoColor=white)
![Reinforcement Learning](https://img.shields.io/badge/RL-Q--learning-8A2BE2)
![Platform](https://img.shields.io/badge/Platform-Desktop-lightgrey)

## ✨ What this project does

**Agentic Snake** combines a traditional grid-based Snake game with a small,
interpretable reinforcement-learning playground. The included Q-learning agent
learns a policy from a compact 11-value state representation and stores the
learned policy as a Python pickle file.

You can:

- play the traditional Snake game with keyboard controls;
- train and visually benchmark a Q-learning agent;
- play a timed human-versus-AI battle;
- override the AI with human “sabotage” inputs in Interference Mode; and
- compare a normal Q-table with an optimized Q-table in a best-of-three arena.

## 🎮 Modes

### Graphical launcher

Run `gui_main.py` to open the modern launcher:

1. **Train & Benchmark Agent** — trains for 1,000 episodes, saves
   `q_table.pkl`, and runs three visual demo episodes.
2. **Human vs AI Agent (Battle Mode)** — a 60-second match between the human
   snake and the trained AI.
3. **Human Interference (Adversarial Mode)** — the AI plays while arrow-key
   inputs can override its direction.
4. **Normal vs Optimized AI** — runs a three-match comparison using
   `q_table_normal.pkl` and `q_table.pkl`.
5. **Play Traditional Snake Game** — classic human-controlled Snake with
   music, images, score, and persistent high score.
6. **Exit**

```bash
python gui_main.py
```

### Terminal launcher

Run `main.py` for a text-based menu. It exposes training, Interference Mode,
Battle Mode, and classic Snake:

```bash
python main.py
```

### Direct training

Training can also be started without either launcher:

```bash
python train.py
```

Training runs without rendering for speed, writes the learned policy to
`q_table.pkl`, and attempts to save `training_curve.png` when Matplotlib is
installed. It then displays three visual benchmark episodes.

## 🧠 How the Q-learning agent works

The agent uses an epsilon-greedy policy and a dictionary-backed Q-table.

### State representation

Each state contains 11 binary values:

1. danger straight ahead;
2. danger to the right;
3. danger to the left;
4. current direction is up;
5. current direction is right;
6. current direction is down;
7. current direction is left;
8. food is above;
9. food is to the right;
10. food is below; and
11. food is to the left.

### Actions

The policy chooses one relative action per step:

| Action | Meaning |
| --- | --- |
| `0` | Continue straight |
| `1` | Turn right |
| `2` | Turn left |

### Rewards

The environment uses reward shaping to make learning easier:

- `+50` for eating food;
- `+1` for moving closer to food;
- `-1.5` for moving farther away; and
- `-100` for a collision or an episode timeout.

The default training configuration uses a learning rate of `0.1`, discount
factor of `0.9`, initial exploration of `1.0`, exploration decay of `0.992`,
and minimum exploration of `0.01`.

## 🕹️ Controls

### Classic Snake

| Key | Action |
| --- | --- |
| Arrow keys | Move the snake |
| `S` | Stop the snake |
| `Q` | Increase score by 2 (debug/cheat behavior) |
| `F` | Increase movement speed |
| `L` | Decrease movement speed |
| `Space` | Start from the welcome screen |
| `Enter` | Restart after game over |
| `E` / `End` | Exit the current game |

### Battle Mode

| Key | Action |
| --- | --- |
| Arrow keys | Control the human snake |
| Any arrow key at the opening screen | Start the match |

The arena lasts up to 60 seconds. The human snake is cyan and the AI snake is
green.

### Human Interference Mode

| Key | Action |
| --- | --- |
| Arrow keys | Override the AI's relative direction |
| `F` | Increase speed |
| `S` | Decrease speed |
| `R` | Reset the current episode |
| `Esc` | Leave the final game-over screen |

Opposite-direction overrides are ignored because they would immediately turn
the snake into its own neck.

## 🧰 Installation

This repository does not currently include a dependency manifest such as
`requirements.txt` or `pyproject.toml`. Create a virtual environment and
install the runtime dependencies manually:

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
# source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install pygame numpy
```

Matplotlib is optional and is only needed for the training curve:

```bash
python -m pip install matplotlib
```

> **Audio note:** Classic Snake initializes the Pygame mixer. If your system
> cannot initialize audio, use a configured desktop audio device or adjust the
> local Pygame/audio setup before launching that mode.

## 📁 Project structure

```text
.
├── gui_main.py              # Graphical launcher
├── main.py                  # Terminal launcher
├── train.py                 # Q-learning training and benchmark flow
├── src/
│   ├── q_agent.py           # QLearningAgent and Q-table persistence
│   └── snake_env.py         # Grid environment, state, rewards, rendering
├── modes/
│   ├── snake_game.py        # Traditional Snake implementation
│   ├── battle_mode.py       # Human vs trained AI
│   ├── interference_mode.py # Human override/adversarial experiment
│   └── compare_mode.py      # Normal vs optimized AI comparison
├── models/                  # Model-related workspace assets
├── img_music/               # Background images and sound effects
├── q_table.pkl              # Trained/optimized Q-table artifact
├── q_table_normal.pkl       # Q-table used by comparison mode
├── high_score.txt           # Persistent classic-game high score
├── snake.png, snake1.png   # Launcher artwork
└── *.spec                   # PyInstaller build specifications
```

The `build/`, `dist/`, and `output/` directories contain generated packaging
outputs and are not required when running from source. The root-level source
files and assets are the canonical implementation.

## 💾 Model and generated files

- `q_table.pkl` is loaded by Battle Mode and Interference Mode.
- `q_table_normal.pkl` is loaded by the comparison mode alongside
  `q_table.pkl`.
- Running training overwrites `q_table.pkl`.
- Training may generate `training_curve.png`.
- Classic Snake updates `high_score.txt`.
- Q-tables are Python pickle files; only load model files from trusted sources.

If a mode reports that a model is missing, run training first:

```bash
python train.py
```

The comparison mode additionally expects `q_table_normal.pkl` to be present.

## 🏗️ Packaging for Windows

PyInstaller specification files are included for the graphical launcher and
the original standalone game:

```bash
python -m pip install pyinstaller
pyinstaller gui_main.spec
```

The generated executable and bundled assets appear under `build/` and `dist/`.
Because the application loads images, audio, models, and score files using
relative paths, launch a packaged build from its distribution directory and
keep the required assets beside the executable.

## 🔍 Design notes and current limitations

- The learning environment uses a fixed grid with a default size of
  `700 × 500` and 20-pixel cells.
- The classic game uses a separate `700 × 500` implementation with 15-pixel
  movement.
- The agent is intentionally small and tabular rather than neural; this makes
  its behavior easy to inspect but limits generalization.
- Random food placement and training exploration mean scores can vary between
  runs.
- The project currently relies on working-directory-relative asset paths.
  Running commands from the repository root is the most reliable workflow.
- There is no automated test suite or dependency lockfile in the repository.

## 🤝 Contributing

1. Create a feature branch.
2. Make focused changes and preserve the existing mode behavior.
3. Run a syntax check before opening a pull request:

   ```bash
   python -m compileall src modes gui_main.py main.py train.py
   ```

4. Describe gameplay, training, or asset changes clearly in the pull request.

Useful contribution ideas include extracting shared grid logic, adding a
dependency manifest, replacing working-directory-relative paths with
project-relative asset resolution, and adding deterministic environment tests.

## 📜 License

No license file is currently included in this repository. Add a license before
redistributing the project or its bundled assets.

---

Made with Python, Pygame, and a little reinforcement learning. 🐍
