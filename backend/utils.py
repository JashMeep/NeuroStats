def calculate_recall(card):
    """
    Simple exponential decay model for recall probability
    """
    base = card.confidence
    decay_rate = 0.1
    recall_probability = base * (0.9 ** card.time_since_review)
    return round(recall_probability, 2)

def classify_mistake(card):
    """
    Classify mistake type based on correctness and confidence
    """
    if card.is_correct:
        return "none"
    if card.confidence > 0.7:
        return "conceptual"
    return "memory"