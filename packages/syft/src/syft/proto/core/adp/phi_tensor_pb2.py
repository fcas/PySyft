# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/adp/phi_tensor.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.adp import (
    scalar_manager_pb2 as proto_dot_core_dot_adp_dot_scalar__manager__pb2,
)
from syft.proto.core.adp import entity_pb2 as proto_dot_core_dot_adp_dot_entity__pb2
from syft.proto.core.tensor import (
    share_tensor_pb2 as proto_dot_core_dot_tensor_dot_share__tensor__pb2,
)
from syft.proto.lib.numpy import array_pb2 as proto_dot_lib_dot_numpy_dot_array__pb2
from syft.proto.lib.python import none_pb2 as proto_dot_lib_dot_python_dot_none__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1fproto/core/adp/phi_tensor.proto\x12\rsyft.core.adp\x1a\x1bproto/core/adp/entity.proto\x1a\x1bproto/lib/numpy/array.proto\x1a#proto/core/adp/scalar_manager.proto\x1a$proto/core/tensor/share_tensor.proto\x1a\x1bproto/lib/python/none.proto"\xf5\x02\n\x15SingleEntityPhiTensor\x12/\n\x06tensor\x18\x01 \x01(\x0b\x32\x1d.syft.core.tensor.ShareTensorH\x00\x12+\n\x05\x61rray\x18\x02 \x01(\x0b\x32\x1a.syft.lib.numpy.NumpyProtoH\x00\x12\'\n\x04none\x18\x03 \x01(\x0b\x32\x17.syft.lib.python.SyNoneH\x00\x12,\n\x08min_vals\x18\x04 \x01(\x0b\x32\x1a.syft.lib.numpy.NumpyProto\x12,\n\x08max_vals\x18\x05 \x01(\x0b\x32\x1a.syft.lib.numpy.NumpyProto\x12%\n\x06\x65ntity\x18\x06 \x01(\x0b\x32\x15.syft.core.adp.Entity\x12I\n\x0escalar_manager\x18\x07 \x01(\x0b\x32\x31.syft.core.adp.VirtualMachinePrivateScalarManagerB\x07\n\x05\x63hild"\xb4\x02\n\x12RowEntityPhiTensor\x12\x19\n\x11serde_concurrency\x18\x01 \x01(\r\x12\x0c\n\x04rows\x18\x02 \x03(\x0c\x12.\n\x0funique_entities\x18\x03 \x03(\x0b\x32\x15.syft.core.adp.Entity\x12Q\n\x16unique_scalar_managers\x18\x04 \x03(\x0b\x32\x31.syft.core.adp.VirtualMachinePrivateScalarManager\x12\x34\n\x10row_entity_index\x18\x05 \x01(\x0b\x32\x1a.syft.lib.numpy.NumpyProto\x12<\n\x18row_scalar_manager_index\x18\x06 \x01(\x0b\x32\x1a.syft.lib.numpy.NumpyProtob\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.core.adp.phi_tensor_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SINGLEENTITYPHITENSOR._serialized_start = 213
    _SINGLEENTITYPHITENSOR._serialized_end = 586
    _ROWENTITYPHITENSOR._serialized_start = 589
    _ROWENTITYPHITENSOR._serialized_end = 897
# @@protoc_insertion_point(module_scope)
