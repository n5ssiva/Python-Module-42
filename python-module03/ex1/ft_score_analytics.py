import sys

if len(sys.argv) < 2:
    print("No scores provided. Usage: python3"
          "ft_score_analytics.py <score1> <score2> ..")
else:
    scores = []
    for arg in sys.argv[1:]:
        try:
            scores.append(int(arg))
        except ValueError:
            pass
    average = sum(scores) / len(scores)
    score_range = max(scores) - min(scores)
    print("=== Player Score Analytics ===")
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {sum(scores)}")
    print(f"Average score: {average}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {score_range}")
