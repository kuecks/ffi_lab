from contextlib import contextmanager
from abc import ABC, abstractmethod
import typing as t
from database_lib import Database
import grpc
import database_pb2_grpc
from database_pb2 import GetEdgesRequest, TwoHopsRequest
from database_ffi import Database as RustDatabase


class Client(ABC):
    @abstractmethod
    def get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        pass

    @abstractmethod
    def two_hops(self, from_id: int, edge1_type: int, edge2_type: int) -> t.List[int]:
        pass


class InMemoryClient(Client):
    def __init__(self, db: Database) -> None:
        self.db = db

    def get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        return self.db.get_edges(from_id, edge_type)

    def two_hops(self, from_id: int, edge1_type: int, edge2_type: int) -> t.List[int]:
        return self.db.two_hops(from_id, edge1_type, edge2_type)


class RustClient(Client):
    def __init__(self, db: RustDatabase) -> None:
        self.db = db

    def get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        return self.db.get_edges(from_id, edge_type)

    def two_hops(self, from_id: int, edge1_type: int, edge2_type: int) -> t.List[int]:
        return self.db.two_hops(from_id, edge1_type, edge2_type)


class RemoteClient(Client):
    def __init__(self, client: database_pb2_grpc.DatabaseStub) -> None:
        self.client = client

    def get_edges(self, from_id: int, edge_type: int) -> t.List[int]:
        request = GetEdgesRequest(
            from_id=from_id,
            edge_type=edge_type,
        )
        return self.client.get_edges(request).ids

    def two_hops(self, from_id: int, edge1_type: int, edge2_type: int) -> t.List[int]:
        request = TwoHopsRequest(
            from_id=from_id,
            edge1_type=edge1_type,
            edge2_type=edge2_type,
        )
        return self.client.two_hops(request).ids


class ClientFactory(ABC):
    @abstractmethod
    @contextmanager
    def make(self) -> t.Generator[Client, None, None]:
        raise NotImplementedError()


class InMemoryClientFactory(ClientFactory):
    def __init__(self) -> None:
        self.db = Database()

    @contextmanager
    def make(self) -> t.Generator[Client, None, None]:
        yield InMemoryClient(self.db)


class RustClientFactory(ClientFactory):
    def __init__(self) -> None:
        self.db = RustDatabase()

    @contextmanager
    def make(self) -> t.Generator[Client, None, None]:
        yield RustClient(self.db)


class RemoteClientFactory(ClientFactory):
    def __init__(self, port: int) -> None:
        self.port = port

    @contextmanager
    def make(self) -> t.Generator[Client, None, None]:
        with grpc.insecure_channel(f"localhost:{self.port}") as channel:
            client = database_pb2_grpc.DatabaseStub(channel)
            yield RemoteClient(client)
