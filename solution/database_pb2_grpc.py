# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import database_pb2 as database__pb2


class DatabaseStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_edges = channel.unary_unary(
                '/database.Database/get_edges',
                request_serializer=database__pb2.GetEdgesRequest.SerializeToString,
                response_deserializer=database__pb2.GetEdgesResponse.FromString,
                )
        self.two_hops = channel.unary_unary(
                '/database.Database/two_hops',
                request_serializer=database__pb2.TwoHopsRequest.SerializeToString,
                response_deserializer=database__pb2.GetEdgesResponse.FromString,
                )


class DatabaseServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_edges(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def two_hops(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DatabaseServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_edges': grpc.unary_unary_rpc_method_handler(
                    servicer.get_edges,
                    request_deserializer=database__pb2.GetEdgesRequest.FromString,
                    response_serializer=database__pb2.GetEdgesResponse.SerializeToString,
            ),
            'two_hops': grpc.unary_unary_rpc_method_handler(
                    servicer.two_hops,
                    request_deserializer=database__pb2.TwoHopsRequest.FromString,
                    response_serializer=database__pb2.GetEdgesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'database.Database', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Database(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_edges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.Database/get_edges',
            database__pb2.GetEdgesRequest.SerializeToString,
            database__pb2.GetEdgesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def two_hops(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/database.Database/two_hops',
            database__pb2.TwoHopsRequest.SerializeToString,
            database__pb2.GetEdgesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
