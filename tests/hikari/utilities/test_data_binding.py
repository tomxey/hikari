# -*- coding: utf-8 -*-
# Copyright (c) 2020 Nekokatt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import typing

import attr
import mock
import multidict
import pytest

from hikari import snowflakes
from hikari import undefined
from hikari.utilities import data_binding


@attr.s(slots=True)
class MyUnique(snowflakes.Unique):
    id: snowflakes.Snowflake = attr.ib(converter=snowflakes.Snowflake)


class TestStringMapBuilder:
    def test_is_mapping(self):
        assert isinstance(data_binding.StringMapBuilder(), typing.Mapping)

    def test_is_multidict(self):
        assert isinstance(data_binding.StringMapBuilder(), multidict.MultiDict)

    def test_starts_empty(self):
        mapping = data_binding.StringMapBuilder()
        assert mapping == {}

    def test_put_undefined(self):
        mapping = data_binding.StringMapBuilder()
        mapping.put("foo", undefined.UNDEFINED)
        assert dict(mapping) == {}

    def test_put_general_value_casts_to_str(self):
        m = mock.Mock()
        mapping = data_binding.StringMapBuilder()
        mapping.put("foo", m)
        assert dict(mapping) == {"foo": m.__str__()}

    def test_duplicate_puts_stores_values_as_sequence(self):
        m1 = mock.Mock()
        m2 = mock.Mock()
        mapping = data_binding.StringMapBuilder()
        mapping.put("foo", m1)
        mapping.put("foo", m2)
        assert mapping.getall("foo") == [m1.__str__(), m2.__str__()]
        assert list(mapping.keys()) == ["foo", "foo"]

    def test_put_Unique(self):
        mapping = data_binding.StringMapBuilder()

        mapping.put("myunique", MyUnique(123))
        assert dict(mapping) == {"myunique": "123"}

    def test_put_int(self):
        mapping = data_binding.StringMapBuilder()
        mapping.put("yeet", 420_69)
        assert dict(mapping) == {"yeet": "42069"}

    @pytest.mark.parametrize(
        ("name", "input_val", "expect"), [("a", True, "true"), ("b", False, "false"), ("c", None, "null")]
    )
    def test_put_py_singleton(self, name, input_val, expect):
        mapping = data_binding.StringMapBuilder()
        mapping.put(name, input_val)
        assert dict(mapping) == {name: expect}

    def test_put_with_conversion_uses_return_value(self):
        def convert(_):
            return "yeah, i got called"

        mapping = data_binding.StringMapBuilder()
        mapping.put("blep", "meow", conversion=convert)
        assert dict(mapping) == {"blep": "yeah, i got called"}

    def test_put_with_conversion_passes_raw_input_to_converter(self):
        mapping = data_binding.StringMapBuilder()
        convert = mock.Mock()

        expect = object()
        mapping.put("yaskjgakljglak", expect, conversion=convert)
        convert.assert_called_once_with(expect)

    def test_put_py_singleton_conversion_runs_before_check(self):
        def convert(_):
            return True

        mapping = data_binding.StringMapBuilder()
        mapping.put("im hungry", "yo", conversion=convert)
        assert dict(mapping) == {"im hungry": "true"}


class TestJSONObjectBuilder:
    def test_is_mapping(self):
        assert isinstance(data_binding.JSONObjectBuilder(), typing.Mapping)

    def test_starts_empty(self):
        assert data_binding.JSONObjectBuilder() == {}

    def test_put_undefined(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put("foo", undefined.UNDEFINED)
        assert builder == {}

    def test_put_defined(self):
        m = mock.Mock()
        builder = data_binding.JSONObjectBuilder()
        builder.put("bar", m)
        assert builder == {"bar": m}

    def test_put_with_conversion_uses_conversion_result(self):
        m = mock.Mock()
        convert = mock.Mock()
        builder = data_binding.JSONObjectBuilder()
        builder.put("rawr", m, conversion=convert)
        assert builder == {"rawr": convert()}

    def test_put_with_conversion_passes_raw_input_to_converter(self):
        m = mock.Mock()
        convert = mock.Mock()
        builder = data_binding.JSONObjectBuilder()
        builder.put("bar", m, conversion=convert)
        convert.assert_called_once_with(m)

    def test_put_array_undefined(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put_array("dd", undefined.UNDEFINED)
        assert builder == {}

    def test__put_array_defined(self):
        m1 = mock.Mock()
        m2 = mock.Mock()
        m3 = mock.Mock()
        builder = data_binding.JSONObjectBuilder()
        builder.put_array("ttt", [m1, m2, m3])
        assert builder == {"ttt": [m1, m2, m3]}

    def test_put_array_with_conversion_uses_conversion_result(self):
        r1 = mock.Mock()
        r2 = mock.Mock()
        r3 = mock.Mock()

        convert = mock.Mock(side_effect=[r1, r2, r3])
        builder = data_binding.JSONObjectBuilder()
        builder.put_array("www", [object(), object(), object()], conversion=convert)
        assert builder == {"www": [r1, r2, r3]}

    def test_put_array_with_conversion_passes_raw_input_to_converter(self):
        m1 = mock.Mock()
        m2 = mock.Mock()
        m3 = mock.Mock()

        convert = mock.Mock()
        builder = data_binding.JSONObjectBuilder()
        builder.put_array("xxx", [m1, m2, m3], conversion=convert)
        assert convert.call_args_list[0] == mock.call(m1)
        assert convert.call_args_list[1] == mock.call(m2)
        assert convert.call_args_list[2] == mock.call(m3)

    def test_put_snowflake_undefined(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake("nya!", undefined.UNDEFINED)
        assert builder == {}

    @pytest.mark.parametrize(
        ("input_value", "expected_str"),
        [
            (100123, "100123"),
            ("100124", "100124"),
            (MyUnique(100127), "100127"),
            (MyUnique("100129"), "100129"),
            (snowflakes.Snowflake(100125), "100125"),
            (snowflakes.Snowflake("100126"), "100126"),
        ],
    )
    def test_put_snowflake(self, input_value, expected_str):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake("WAWAWA!", input_value)
        assert builder == {"WAWAWA!": expected_str}

    def test_put_snowflake_none(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake("wawawa osuremono", None)
        assert builder == {"wawawa osuremono": None}

    @pytest.mark.parametrize(
        ("input_value", "expected_str"),
        [
            (100123, "100123"),
            ("100124", "100124"),
            (MyUnique(100127), "100127"),
            (MyUnique("100129"), "100129"),
            (snowflakes.Snowflake(100125), "100125"),
            (snowflakes.Snowflake("100126"), "100126"),
        ],
    )
    def test_put_snowflake_array_conversions(self, input_value, expected_str):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake_array("WAWAWAH!", [input_value] * 5)
        assert builder == {"WAWAWAH!": [expected_str] * 5}

    def test_put_snowflake_array(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake_array("DESU!", [123, 456, 987, 115])
        assert builder == {"DESU!": ["123", "456", "987", "115"]}

    def test_put_snowflake_array_undefined(self):
        builder = data_binding.JSONObjectBuilder()
        builder.put_snowflake_array("test", undefined.UNDEFINED)
        assert builder == {}


class TestCastJSONArray:
    def test_cast_is_invoked_with_each_item(self):
        cast = mock.Mock()
        arr = ["foo", "bar", "baz"]

        data_binding.cast_json_array(arr, cast)

        assert cast.call_args_list[0] == mock.call("foo")
        assert cast.call_args_list[1] == mock.call("bar")
        assert cast.call_args_list[2] == mock.call("baz")

    def test_cast_result_is_used_for_each_item(self):
        r1 = mock.Mock()
        r2 = mock.Mock()
        r3 = mock.Mock()
        cast = mock.Mock(side_effect=[r1, r2, r3])

        arr = ["foo", "bar", "baz"]

        assert data_binding.cast_json_array(arr, cast) == [r1, r2, r3]

    def test_passes_kwargs_for_every_cast(self):
        cast = mock.Mock()
        arr = ["foo", "bar", "baz"]

        data_binding.cast_json_array(arr, cast, foo=42, bar="OK")

        assert cast.call_args_list[0] == mock.call("foo", foo=42, bar="OK")
        assert cast.call_args_list[1] == mock.call("bar", foo=42, bar="OK")
        assert cast.call_args_list[2] == mock.call("baz", foo=42, bar="OK")