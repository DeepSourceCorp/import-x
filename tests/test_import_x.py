import sys

import pytest

from import_x import ExtensionLoader


def extension_not_present():
    class DummyLoder(ExtensionLoader):
        pass


def handle_module_not_present():
    class DummyLoder(ExtensionLoader):
        extension = '.txt'


def handle_module_not_callable():
    class DummyLoder(ExtensionLoader):
        extension = '.txt'
        handle_module = ''


def handle_module_arguements_length():
    class DummyLoader(ExtensionLoader):
        extension = '.txt'

        def handle_module(self, module):
            pass


def handle_module_arguements_length_staticmethod():
    class DummyLoader(ExtensionLoader):
        extension = '.txt'

        @staticmethod
        def handle_module(module):
            pass


VALIDATION_PARAMETERS = [
    (
        extension_not_present,
        "Class variable 'extension' not present for class 'DummyLoder'"
    ),
    (
        handle_module_not_present,
        "Method 'handle_module' not present for class 'DummyLoder'"
    ),
    (
        handle_module_not_callable,
        "Method 'handle_module' not present for class 'DummyLoder'"
    ),
    (
        handle_module_arguements_length,
        "In class 'DummyLoader' method handle_module should take 2 "
        "arguements, but it is taking 1"
    ),
    (
        handle_module_arguements_length_staticmethod,
        "In class 'DummyLoader' method handle_module should take 2 "
        "arguements, but it is taking 1"
    ),
]


@pytest.mark.parametrize('func, error_message', VALIDATION_PARAMETERS)
def test_validation(func, error_message):
    with pytest.raises(AssertionError, match=error_message):
        func()


def test_auto_enable():
    def _auto_enable():
        class JavaLoader(ExtensionLoader):
            extension = '.java'
            auto_enable = True

            def handle_module(self, module, path):
                pass
    assert sys.meta_path[-1].__class__.__name__ != 'JavaLoader'
    _auto_enable()
    assert sys.meta_path[-1].__class__.__name__ == 'JavaLoader'
    # clean-up
    sys.meta_path.pop()


def test_auto_enable_false():
    def _auto_enable():
        class JavaLoader(ExtensionLoader):
            extension = '.java'
            auto_enable = False

            def handle_module(self, module, path):
                pass
        return JavaLoader()

    java_imports = _auto_enable()
    assert sys.meta_path[-1].__class__.__name__ != 'JavaLoader'

    with java_imports:
        assert sys.meta_path[-1].__class__.__name__ == 'JavaLoader'
    assert sys.meta_path[-1].__class__.__name__ != 'JavaLoader'
