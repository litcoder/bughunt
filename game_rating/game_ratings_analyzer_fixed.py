import csv
import os

def normalize_path(path):
    return os.path.normpath(path)

def is_valid_rating(r):
    return isinstance(r, (int, float)) and 0 <= r <= 10

def is_tie(games):
    unique_scores = set(avg for _, avg in games)
    return len(unique_scores) == 1

def read_ratings(file_path):
    ratings = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "").strip()
                rating_str = row.get("rating", "").strip()
                if not title or not rating_str:
                    continue
                try:
                    rating = int(rating_str)
                except ValueError:
                    continue
                if not is_valid_rating(rating):
                    continue
                if title in ratings:
                    ratings[title].append(rating)
                else:
                    ratings[title] = [rating]
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    return ratings

def generate_report(ratings, top_n):
    if not ratings:
        print("평가 데이터가 없습니다.")
        return

    averages = {}
    for title, scores in ratings.items():
        if scores:
            averages[title] = sum(scores) / len(scores)

    sorted_games = sorted(averages.items(), key=lambda x: x[1], reverse=True)

    print("\nTop Rated Games:")
    for i, (title, avg) in enumerate(sorted_games[:top_n]):
        print(f"{i+1}. {title} - Avg Rating: {avg:.2f}")

    if is_tie(sorted_games):
        print("All games have the same average rating.")

def main():
    path = os.path.join("data", "game_ratings_bugs.csv")
    file_path = normalize_path(path)
    ratings = read_ratings(file_path)
    top_n = min(10, len(ratings))
    generate_report(ratings, top_n)

if __name__ == "__main__":
    main()
