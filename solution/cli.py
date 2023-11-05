import argparse
from collections import Counter
from database_client import (
    InMemoryClientFactory,
    RemoteClientFactory,
    Client,
    ClientFactory,
    RustClientFactory,
)
from database_lib import FRIEND, LIKE
import typing as t


def pymk(id: int, client: Client) -> None:
    """
    Get "people you may know"
    Get all friends of friends that you are not already friends with, then sort them
    by number of mutual friends
    """
    pymk: Counter[int] = Counter()
    friends = set(client.get_edges(id, FRIEND))
    for friend in friends:
        pymk.update(set(client.get_edges(friend, FRIEND)) - {id} - friends)
    print(f"You may know {pymk.most_common()}")


def tyme(id: int, client: Client) -> None:
    """
    Get "things you may enjoy"
    Get all the things that your friends like, then sort by how many of your friends like enjoy them
    """
    tyme: Counter[int] = Counter()
    likes = set(client.get_edges(id, LIKE))
    friends = client.get_edges(id, FRIEND)
    for friend in friends:
        friend_likes = set(client.get_edges(friend, LIKE)) - likes
        tyme.update(friend_likes)
    print(f"You may enjoy {tyme.most_common()}")


def main(args: argparse.Namespace):
    factory: ClientFactory
    if args.remote_port:
        factory = RemoteClientFactory(port=args.remote_port)
    elif args.rust:
        factory = RustClientFactory()
    else:
        factory = InMemoryClientFactory()
    with factory.make() as client:
        if args.command == "pymk":
            print("Calling pymk")
            pymk(args.id, client)
        elif args.command == "tyme":
            tyme(args.id, client)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    client_group = parser.add_mutually_exclusive_group(required=True)
    client_group.add_argument(
        "--in-memory",
        action="store_true",
        help="Use an in memory client with this json file as the db",
    )
    client_group.add_argument(
        "--remote-port", type=int, help="Use a client to a remote db on this port"
    )
    client_group.add_argument(
        "--rust",
        action="store_true",
        help="Use a client to a rust db over ffi with this json file as the db",
    )
    commands = parser.add_subparsers(required=True, dest="command")
    pymk_parser = commands.add_parser("pymk", help="Find people you may know")
    pymk_parser.add_argument(
        "id", type=int, help="The id of the person to find potential friends for"
    )
    tyme_parser = commands.add_parser("tyme", help="Find things you may enjoy")
    tyme_parser.add_argument(
        "id", type=int, help="The id of the person to find things they may enjoy"
    )
    args = parser.parse_args()
    main(args)
