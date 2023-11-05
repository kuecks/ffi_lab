import argparse
import grpc
from concurrent import futures
import database_pb2_grpc
from database_pb2 import GetEdgesRequest, TwoHopsRequest, GetEdgesResponse
from database_lib import Database, DbObject
import typing as t


class DatabaseServicer(database_pb2_grpc.DatabaseServicer):
    def __init__(self):
        self.db = Database()

    def _get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        from_obj: t.Optional[DbObject] = self.db.objects.get(from_id)
        if not from_obj:
            return []
        return sorted(from_obj.edges.get(edge_type) or [])

    def get_edges(self, request: GetEdgesRequest, context) -> GetEdgesResponse:
        ids = self._get_edges(request.from_id, request.edge_type)
        return GetEdgesResponse(ids=ids)

    def two_hops(self, request: TwoHopsRequest, context) -> GetEdgesResponse:
        first_hop: t.List[int] = self._get_edges(request.from_id, request.edge1_type)
        ids = set()
        for adj in first_hop:
            ids.update(self._get_edges(adj, request.edge2_type))
        return GetEdgesResponse(ids=sorted(ids))


def serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServicer_to_server(DatabaseServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Serving on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=50051)
    args = parser.parse_args()
    serve(args.port)
