# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFGraphRecordDecoder and utilities to save and load them."""

from __future__ import absolute_import
from __future__ import division
# Standard __future__ imports
from __future__ import print_function

import abc
from typing import Dict, List, Optional, Text, Union

import six
import tensorflow as tf

from tensorflow.python.framework import composite_tensor  # pylint: disable=g-direct-tensorflow-import


TensorAlike = Union[tf.Tensor, composite_tensor.CompositeTensor]


@six.add_metaclass(abc.ABCMeta)
class TFGraphRecordDecoder(tf.Module):
  """Base class for decoders that turns a list of bytes to (composite) tensors.

  Sub-classes must implemented `_decode_record_internal()` (see its docstring
  for requirements).

  Decoder instances can be saved as a SavedModel by `save_decoder()`.
  The SavedModel can be loaded back by `load_decoder()`. However, the loaded
  decoder will always be of the type `LoadedDecoder` and only have the public
  interfaces listed in this base class available.
  """

  def __init__(self, name: Text):
    """Initializer.

    Args:
      name: Must be a valid TF scope name. May be used to create TF namescopes.
        see https://www.tensorflow.org/api_docs/python/tf/Graph#name_scope.
    """
    super(TFGraphRecordDecoder, self).__init__(name=name)

  @tf.function(input_signature=[tf.TensorSpec(shape=(None,), dtype=tf.string)])
  def decode_record(self, records: List[bytes]) -> Dict[Text, TensorAlike]:
    """Decodes a list of bytes to a Dict of (composite) tensors."""
    return self._decode_record_internal(tf.convert_to_tensor(records))

  def output_type_specs(self) -> Dict[Text, tf.TypeSpec]:
    """Returns the tf.TypeSpecs of the decoded tensors.

    Returns:
      A dict whose keys are the same as keys of the dict returned by
      `decode_record()` and values are the tf.TypeSpec of the corresponding
      (composite) tensor.
    """
    return {
        k: v._type_spec for k, v in  # pylint: disable=protected-access
        self.decode_record.get_concrete_function().structured_outputs.items()
    }

  @abc.abstractmethod
  def _decode_record_internal(
      self, records: tf.Tensor) -> Dict[Text, TensorAlike]:
    """Sub-classes should implement this.

    Implementations must use TF ops to derive the result (composite) tensors, as
    this function will be traced and become a tf.function (thus a TF Graph).

    The returned tensors must be batch-aligned (i.e. they should be at least
    of rank 1, and their outer-most dimensions must be of the same size). They
    do not have to be batch-aligned with the input tensor, but if that's the
    case, an additional tensor must be provided among the results, to indicate
    which input record a "row" in the output batch comes from. See
    `record_index_tensor_name` for more details.

    Args:
      records: a 1-D string tensor that contains the records to be decoded.

    Returns:
      A dict of (composite) tensors.
    """

  # Add the return type annotation once we drop TF 1.15 support.
  @tf.function(input_signature=[])
  def _record_index_tensor_name_tensor(self):
    """tf.function to store record_index_tensor_name in SavedModel."""
    if self.record_index_tensor_name is not None:
      return tf.experimental.Optional.from_value(
          self.record_index_tensor_name.encode())
    return tf.experimental.Optional.empty(tf.TensorSpec(
        shape=(), dtype=tf.string))

  @property
  def record_index_tensor_name(self) -> Optional[Text]:
    """The name of the tensor indicating which record a slice is from.

    The decoded tensors are batch-aligned among themselves, but they don't
    necessarily have to be batch-aligned with the input records. If not,
    sub-classes should implement this method to tie the batch dimension
    with the input record.

    The record index tensor must be a SparseTensor or a RaggedTensor of integral
    type, and must be 2-D and must not contain "missing" values.

    A record index tensor like the following:
    [[0], [0], [2]]
    means that of 3 "rows" in the output "batch", the first two rows came
    from the first record, and the 3rd row came from the third record.

    Returns:
      The name of the record index tensor.
    """
    return None


class LoadedDecoder(TFGraphRecordDecoder):
  """A `TFGraphRecordDecoder` recovered from a SavedModel.

  This wrapper class is needed because `output_type_specs()` won't be part
  of the SavedModel.
  """

  def __init__(self, loaded_module):
    super(LoadedDecoder, self).__init__(name="LoadedDecoder")
    self._loaded_module = loaded_module

  def _decode_record_internal(self,
                              record: List[bytes]) -> Dict[Text, TensorAlike]:
    return self._loaded_module.decode_record(record)

  @property
  def record_index_tensor_name(self) -> Optional[Text]:
    optional_name = self._loaded_module._record_index_tensor_name_tensor()  # pylint: disable=protected-access
    if optional_name.has_value():
      return optional_name.get_value().numpy().decode()
    return None


def save_decoder(decoder: TFGraphRecordDecoder, path: Text) -> None:
  """Saves a TFGraphRecordDecoder to a SavedModel."""
  if decoder.record_index_tensor_name is not None:
    assert decoder.record_index_tensor_name in decoder.output_type_specs(), (
        "Invalid decoder: record_index_tensor_name: {} not in output "
        "tensors: {}".format(decoder.record_index_tensor_name,
                             decoder.output_type_specs().keys()))
  tf.saved_model.save(decoder, path)


def load_decoder(path: Text) -> LoadedDecoder:
  """Loads a TFGraphRecordDecoder from a SavedModel."""
  loaded_module = tf.saved_model.load(path)
  assert hasattr(loaded_module, "decode_record"), (
      "the SavedModel is not a TFGraphRecordDecoder")
  return LoadedDecoder(loaded_module)
