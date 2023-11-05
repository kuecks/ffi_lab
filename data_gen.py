import argparse
import json
import random
from solution.database_lib import LIKE, FRIEND, DB_FILE


def main(num_people: int, num_objects: int, num_friends: int, num_likes: int) -> None:
    people = list(range(num_people))
    objects = list(range(num_people, num_people + num_objects))
    friends = set()
    likes = set()
    for _ in range(num_friends):
        pair = sorted(random.sample(people, 2))
        friends.add(tuple(pair))
    for _ in range(num_likes):
        person = random.choice(people)
        object = random.choice(objects)
        likes.add((person, object))
    data = {
        FRIEND: {
            "bidir": "Bidir",
            "edges": [list(edge) for edge in sorted(friends)],
        },
        LIKE: {
            "bidir": "Single",
            "edges": [list(edge) for edge in sorted(likes)]
        }
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="The seed for the rng", default=0)
    parser.add_argument("--num-people", type=int, help="The number of people objects", default=100)
    parser.add_argument("--num-objects", type=int, help="The objects to like", default=50)
    parser.add_argument("--num-friends", type=int, help="The number of random friend edges (may have repeats)", default=1000)
    parser.add_argument("--num-likes", type=int, help="The number of random likes (may have repeats)", default=1000)
    args = parser.parse_args()
    random.seed(args.seed)
    main(args.num_people, args.num_objects, args.num_friends, args.num_likes)