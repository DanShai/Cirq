# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Resolves ParameterValues to assigned values."""

from typing import Dict, Union
import sys

import sympy


class ParamResolver(object):
    """Resolves sympy.Symbols to actual values.

    A Symbol is a wrapped parameter name (str). A ParamResolver is an object
    that can be used to assign values for these keys.

    ParamResolvers are hashable.

    Attributes:
        param_dict: A dictionary from the ParameterValue key (str) to its
            assigned value.
    """

    def __init__(self, param_dict: Dict[str, float]) -> None:
        self.param_dict = param_dict
        self._param_hash = hash(frozenset(param_dict.items()))

    def value_of(
            self,
            value: Union[sympy.Basic, float, str]
    ) -> Union[sympy.Basic, float]:
        """Attempt to resolve a Symbol or name or float to its assigned value.

        If unable to resolve a sympy.Symbol, returns it unchanged.
        If unable to resolve a name, returns a sympy.Symbol with that name.

        Args:
            value: The sympy.Symbol or name or float to try to resolve into just
                a float.

        Returns:
            The value of the parameter as resolved by this resolver.
        """
        if isinstance(value, str):
            return self.param_dict.get(value, sympy.Symbol(value))
        if isinstance(value, sympy.Basic):
            if sys.version_info.major < 3:
                # coverage: ignore
                # HACK: workaround https://github.com/sympy/sympy/issues/16087
                d = {k.encode(): v for k, v in self.param_dict.items()}
                v = value.subs(d)
            else:
                v = value.subs(self.param_dict)
            return v if v.free_symbols else float(v)
        return value

    def __getitem__(self, key):
        return self.value_of(key)

    def __hash__(self):
        return self._param_hash

    def __eq__(self, other):
        if not isinstance(other, ParamResolver):
            return NotImplemented
        return self.param_dict == other.param_dict

    def __repr__(self):
        return 'cirq.ParamResolver({})'.format(repr(self.param_dict))
