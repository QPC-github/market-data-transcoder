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

from struct import unpack_from

from third_party.sbedecoder import SBEMessageFactory
from transcoder.message.factory.exception import TemplateSchemaNotDefinedError


class MemxMessageFactory(SBEMessageFactory):
    def __init__(self, schema):
        super(MemxMessageFactory, self).__init__(schema)

    def build(self, msg_buffer, offset):
        template_id = unpack_from('>B', msg_buffer, 2)[0]
        message_type = self.schema.get_message_type(template_id)

        if message_type is None:
            raise TemplateSchemaNotDefinedError(f'Schema not found for template_id: {template_id}')

        message = message_type()
        message.wrap(msg_buffer, 0)
        return message, len(msg_buffer)