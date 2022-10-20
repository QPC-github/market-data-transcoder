#
# Copyright 2022 Google LLC
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from transcoder.source.file.FileMessageSource import FileMessageSource


class LengthDelimitedFileMessageSource(FileMessageSource):
    @staticmethod
    def source_type_identifier():
        return 'length_delimited'

    def __init__(self, file_path: str, skip_bytes: int = 0, endian: str = 'big',
                 message_skip_bytes: int = 0, message_length_byte_length: int = 2):
        super().__init__(file_path)
        self.skip_bytes = skip_bytes
        self.endian = endian
        self.message_skip_bytes = message_skip_bytes
        self.message_length_byte_length = message_length_byte_length

    def open(self):
        self.file_size = os.path.getsize(self.path)
        self.file_handle = open(self.path, 'rb')
        if self.skip_bytes > 0:
            self.file_handle.read(self.skip_bytes)

    def get_message_iterator(self):
        while self.file_handle.tell() < self.file_size:
            if self.message_skip_bytes > 0:
                self.file_handle.read(self.message_skip_bytes)

            message_length = int.from_bytes(self.file_handle.read(self.message_length_byte_length), self.endian)
            self.increment_count()
            yield self.file_handle.read(message_length)
            self._log_percentage_read()