# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages_robocup_ssl_geometry_legacy.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

from proto import messages_robocup_ssl_geometry_pb2

DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages_robocup_ssl_geometry_legacy.proto',
  package='RoboCup2014Legacy.Geometry',
  serialized_pb=_b('\n*messages_robocup_ssl_geometry_legacy.proto\x12\x1aRoboCup2014Legacy.Geometry\x1a#messages_robocup_ssl_geometry.proto\"\x8a\x03\n\x15SSL_GeometryFieldSize\x12\x12\n\nline_width\x18\x01 \x02(\x05\x12\x14\n\x0c\x66ield_length\x18\x02 \x02(\x05\x12\x13\n\x0b\x66ield_width\x18\x03 \x02(\x05\x12\x16\n\x0e\x62oundary_width\x18\x04 \x02(\x05\x12\x15\n\rreferee_width\x18\x05 \x02(\x05\x12\x12\n\ngoal_width\x18\x06 \x02(\x05\x12\x12\n\ngoal_depth\x18\x07 \x02(\x05\x12\x17\n\x0fgoal_wall_width\x18\x08 \x02(\x05\x12\x1c\n\x14\x63\x65nter_circle_radius\x18\t \x02(\x05\x12\x16\n\x0e\x64\x65\x66\x65nse_radius\x18\n \x02(\x05\x12\x17\n\x0f\x64\x65\x66\x65nse_stretch\x18\x0b \x02(\x05\x12#\n\x1b\x66ree_kick_from_defense_dist\x18\x0c \x02(\x05\x12)\n!penalty_spot_from_field_line_dist\x18\r \x02(\x05\x12#\n\x1bpenalty_line_from_spot_dist\x18\x0e \x02(\x05\"\x83\x01\n\x10SSL_GeometryData\x12@\n\x05\x66ield\x18\x01 \x02(\x0b\x32\x31.RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize\x12-\n\x05\x63\x61lib\x18\x02 \x03(\x0b\x32\x1e.SSL_GeometryCameraCalibration')
  ,
  dependencies=[messages_robocup_ssl_geometry_pb2.DESCRIPTOR, ])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SSL_GEOMETRYFIELDSIZE = _descriptor.Descriptor(
  name='SSL_GeometryFieldSize',
  full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='line_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.line_width', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='field_length', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.field_length', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='field_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.field_width', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='boundary_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.boundary_width', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='referee_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.referee_width', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goal_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.goal_width', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goal_depth', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.goal_depth', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='goal_wall_width', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.goal_wall_width', index=7,
      number=8, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='center_circle_radius', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.center_circle_radius', index=8,
      number=9, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='defense_radius', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.defense_radius', index=9,
      number=10, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='defense_stretch', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.defense_stretch', index=10,
      number=11, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='free_kick_from_defense_dist', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.free_kick_from_defense_dist', index=11,
      number=12, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='penalty_spot_from_field_line_dist', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.penalty_spot_from_field_line_dist', index=12,
      number=13, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='penalty_line_from_spot_dist', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize.penalty_line_from_spot_dist', index=13,
      number=14, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=112,
  serialized_end=506,
)


_SSL_GEOMETRYDATA = _descriptor.Descriptor(
  name='SSL_GeometryData',
  full_name='RoboCup2014Legacy.Geometry.SSL_GeometryData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='field', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryData.field', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='calib', full_name='RoboCup2014Legacy.Geometry.SSL_GeometryData.calib', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=509,
  serialized_end=640,
)

_SSL_GEOMETRYDATA.fields_by_name['field'].message_type = _SSL_GEOMETRYFIELDSIZE
_SSL_GEOMETRYDATA.fields_by_name['calib'].message_type = messages_robocup_ssl_geometry_pb2._SSL_GEOMETRYCAMERACALIBRATION
DESCRIPTOR.message_types_by_name['SSL_GeometryFieldSize'] = _SSL_GEOMETRYFIELDSIZE
DESCRIPTOR.message_types_by_name['SSL_GeometryData'] = _SSL_GEOMETRYDATA

SSL_GeometryFieldSize = _reflection.GeneratedProtocolMessageType('SSL_GeometryFieldSize', (_message.Message,), dict(
  DESCRIPTOR = _SSL_GEOMETRYFIELDSIZE,
  __module__ = 'messages_robocup_ssl_geometry_legacy_pb2'
  # @@protoc_insertion_point(class_scope:RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize)
  ))
_sym_db.RegisterMessage(SSL_GeometryFieldSize)

SSL_GeometryData = _reflection.GeneratedProtocolMessageType('SSL_GeometryData', (_message.Message,), dict(
  DESCRIPTOR = _SSL_GEOMETRYDATA,
  __module__ = 'messages_robocup_ssl_geometry_legacy_pb2'
  # @@protoc_insertion_point(class_scope:RoboCup2014Legacy.Geometry.SSL_GeometryData)
  ))
_sym_db.RegisterMessage(SSL_GeometryData)


# @@protoc_insertion_point(module_scope)
