import typing as t
import json


# TODO: Make this relative to the repo or an absolute path
DB_FILE = "../data.json"
# Edge id for "is friends with"
FRIEND = 0
# Edge id for "likes"
LIKE = 1


class RawEntry(t.TypedDict):
    bidir: str
    edges: t.List[t.List[int]]


class Database:
    def __init__(self) -> None:
        self.objects: t.Dict[int, DbObject] = {}
        with open(DB_FILE, "r") as f:
            raw_contents: t.Dict[int, RawEntry] = json.load(f)
        # JSON keys are strings
        for edge_type_str, entry in raw_contents.items():
            edge_type = int(edge_type_str)
            # Edges that are bidirectional. E.g. "is friends with"
            is_bidir = entry["bidir"] == "Bidir"
            for edge_from, edge_to in entry["edges"]:
                self.objects.setdefault(edge_from, DbObject()).add_edge(
                    edge_type, edge_to
                )
                if is_bidir:
                    # Add the reverse edge as welll
                    self.objects.setdefault(edge_to, DbObject()).add_edge(
                        edge_type, edge_from
                    )

    def get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        from_obj: t.Optional[DbObject] = self.objects.get(from_id)
        if not from_obj:
            return []
        return sorted(from_obj.edges.get(edge_type) or [])

    def two_hops(self, from_id: int, edge1_type: int, edge2_type: int) -> t.List[int]:
        first_hop: t.List[int] = self.get_edges(from_id, edge1_type)
        ids = set()
        for adj in first_hop:
            ids.update(self.get_edges(adj, edge2_type))
        return sorted(ids)


class DbObject:
    def __init__(self) -> None:
        self.edges: t.Dict[int, t.Set[int]] = {}

    def add_edge(self, edge_type: int, to: int):
        self.edges.setdefault(edge_type, set()).add(to)
