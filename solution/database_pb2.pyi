from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetEdgesRequest(_message.Message):
    __slots__ = ["from_id", "edge_type"]
    FROM_ID_FIELD_NUMBER: _ClassVar[int]
    EDGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    from_id: int
    edge_type: int
    def __init__(self, from_id: _Optional[int] = ..., edge_type: _Optional[int] = ...) -> None: ...

class TwoHopsRequest(_message.Message):
    __slots__ = ["from_id", "edge1_type", "edge2_type"]
    FROM_ID_FIELD_NUMBER: _ClassVar[int]
    EDGE1_TYPE_FIELD_NUMBER: _ClassVar[int]
    EDGE2_TYPE_FIELD_NUMBER: _ClassVar[int]
    from_id: int
    edge1_type: int
    edge2_type: int
    def __init__(self, from_id: _Optional[int] = ..., edge1_type: _Optional[int] = ..., edge2_type: _Optional[int] = ...) -> None: ...

class GetEdgesResponse(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ids: _Optional[_Iterable[int]] = ...) -> None: ...
