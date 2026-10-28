import sys
import os

# Ensure current working directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main_menu():
    while True:
        print("\n==============================================")
        print(" 🤖 REINFORCEMENT LEARNING SNAKE AI RESEARCH ")
        print("==============================================")
        print("1. Train Q-Learning Agent (Train & Benchmark)")
        print("2. Run Interference Mode (Human Sabotage vs AI)")
        print("3. Run Battle Mode (1v1 Human vs AI Match)")
        print("4. Play Classic Snake Game (Human Only)")
        print("5. Exit")
        print("==============================================")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        try:
            if choice == '1':
                print("\n[INFO] Starting Training Script...")
                import train
                train.train_and_benchmark()
                
            elif choice == '2':
                print("\n[INFO] Starting Interference Mode...")
                from modes import interference_mode
                interference_mode.run_interference_experiment()
                
            elif choice == '3':
                print("\n[INFO] Starting Battle Arena...")
                from modes.battle_mode import BattleArena
                arena = BattleArena()
                arena.run_match()
                
            elif choice == '4':
                print("\n[INFO] Starting Classic Snake Game...")
                from modes import snake_game
                snake_game.run_game()
                
            elif choice == '5':
                print("Exiting... All the best for your presentation!")
                sys.exit(0)
            else:
                print("[ERROR] Invalid choice! Please select between 1 to 5.")
                
        except Exception as e:
            print(f"\n[ERROR] An error occurred while running the mode: {e}")
            input("Press Enter to return to the main menu...")

if __name__ == "__main__":
    main_menu()