import pytest

from quiz.build import Field, FieldChain, NestedObject, Error
from quiz.build import field_chain as _


class TestFieldChain:

    def test_empty(self):
        assert _ == FieldChain([])

    # def test_hash(self):
    #     assert hash(FieldChain([])) == hash(FieldChain([]))

    def test_getattr(self):
        assert _.foo_field.bla == FieldChain([
            Field('foo_field', {}),
            Field('bla', {}),
        ])

    def test_iter(self):
        items = [
            Field('foo', {}),
            Field('bar', {}),
        ]
        assert list(FieldChain(items)) == items
        assert len(FieldChain(items)) == 2

    def test_getitem(self):
        assert _.foo.bar.blabla[
            _
            .foobar
            .bing
        ] == FieldChain([
            Field('foo', {}),
            Field('bar', {}),
            NestedObject(
                Field('blabla', {}),
                FieldChain([
                    Field('foobar', {}),
                    Field('bing', {}),
                ])
            )
        ])

    def test_getitem_empty(self):
        with pytest.raises(Error):
            _['bla']

    def test_getitem_nested(self):
        assert _.foo[
            _
            .bar
            .bing[
                _
                .blabla
            ]
        ] == FieldChain([
            NestedObject(
                Field('foo', {}),
                FieldChain([
                    Field('bar', {}),
                    NestedObject(
                        Field('bing', {}),
                        FieldChain([
                            Field('blabla', {})
                        ])
                    )
                ])
            )
        ])

    def test_call(self):
        assert _.foo(bla=4, bar=None) == FieldChain([
            Field('foo', {'bla': 4, 'bar': None})
        ])

    def test_call_empty(self):
        assert _.foo() == FieldChain([
            Field('foo', {})
        ])

    def test_invalid_call(self):
        with pytest.raises(Error):
            _()

    def test_combination(self):
        assert _.foo.bar[
            _
            .bing(param1=4.1)
            .baz
            .foo_bar_bla(p2=None, r='')[
                _
                .height(unit='cm')
            ]
            .oof
            .qux()
        ] == FieldChain([
            Field('foo', {}),
            NestedObject(
                Field('bar', {}),
                FieldChain([
                    Field('bing', {'param1': 4.1}),
                    Field('baz', {}),
                    NestedObject(
                        Field('foo_bar_bla', {'p2': None, 'r': ''}),
                        FieldChain([
                            Field('height', {'unit': 'cm'})
                        ])
                    ),
                    Field('oof', {}),
                    Field('qux', {}),
                ])
            )
        ])