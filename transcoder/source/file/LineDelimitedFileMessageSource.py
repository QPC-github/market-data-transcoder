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

from transcoder.source.file import FileMessageSource


class LineDelimitedFileMessageSource(FileMessageSource):
    @staticmethod
    def source_type_identifier():
        return 'line_delimited'

    def __init__(self, file_path: str, skip_lines: int = 0):
        super().__init__(file_path)
        self.skip_lines = skip_lines

    def open(self):
        self.file_size = os.path.getsize(self.path)
        self.file_handle = open(self.path, 'rt')

    def get_message_iterator(self):
        if self.file_size == 0:
            return
        elif self.skip_lines > 0:
            for _ in range(self.skip_lines):
                self.file_handle.readline()
        while line := self.file_handle.readline():
            self.increment_count()
            yield line
            self._log_percentage_read()