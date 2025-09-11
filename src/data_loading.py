import pandas as pd

def load_clean_data():
    human_moves = pd.read_csv("../data/human_moves.csv", header=None).values
    ai_moves = pd.read_csv("../data/ai_moves.csv", header=None).values
    return human_moves, ai_moves

def prepare_training_data(human_moves, ai_moves, indices):
    training_data = []
    for idx in indices:  # Use specific indices
        human_game = human_moves[idx].tolist()
        ai_game = ai_moves[idx].tolist()
        training_data.append((human_game, ai_game))
    return training_data

def load_indices():
    """Load existing train/test split"""
    with open("../data/test_indices.txt", "r") as f:
        test_indices = [int(line.strip()) for line in f]
    
    with open("../data/train_indices.txt", "r") as f:
        train_indices = [int(line.strip()) for line in f]
    
    print(f"Loaded splits: {len(train_indices)} train, {len(test_indices)} test")
    return train_indices, test_indices