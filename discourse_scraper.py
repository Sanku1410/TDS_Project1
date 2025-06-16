import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCOURSE_API_KEY = os.getenv("DISCOURSE_API_KEY")
DISCOURSE_API_USER = os.getenv("DISCOURSE_API_USER")
DISCOURSE_BASE_URL = os.getenv("DISCOURSE_BASE_URL")

def get_posts(from_date, to_date):
    page = 0
    all_posts = []

    while True:
        url = f"{DISCOURSE_BASE_URL}/posts.json?page={page}"
        headers = {
            "Api-Key": DISCOURSE_API_KEY,
            "Api-Username": DISCOURSE_API_USER
        }

        res = requests.get(url, headers=headers)
        if res.status_code != 200 or not res.json():
            break

        posts = res.json()
        for post in posts:
            created = post.get("created_at", "")
            if created:
                post_date = datetime.strptime(created[:10], "%Y-%m-%d").date()
                if from_date <= post_date <= to_date:
                    all_posts.append(post["cooked"])
                elif post_date > to_date:
                    return all_posts

        page += 1

    return all_posts

if __name__ == "__main__":
    from_date = datetime.strptime("2025-01-01", "%Y-%m-%d").date()
    to_date = datetime.strptime("2025-04-14", "%Y-%m-%d").date()
    posts = get_posts(from_date, to_date)

    with open("data/raw/forum_scraped.txt", "w", encoding="utf-8") as f:
        for post in posts:
            f.write(post + "\n\n")

    print(f"Saved {len(posts)} posts.")
