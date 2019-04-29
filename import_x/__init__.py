import contextlib
import json
import os
import pathlib
import sys
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
from inspect import getfullargspec


class ExtensionLoader(MetaPathFinder, Loader):
    """
    Base class to be extended by loaders to handle module.

    Acts as a finder and a loader.
    """

    extension: str

    def __enter__(self):
        sys.meta_path.append(self)

    def __exit__(self, *_):
        sys.meta_path.remove(self)

    @staticmethod
    def _get_file_path(dir_path, file_name, extension):
        path = pathlib.Path(dir_path).joinpath(file_name + extension)
        if path.exists():
            return path.resolve().as_posix()
        return ""

    @classmethod
    def find_spec(cls, fullname, path, *_, **__):
        """Return the spec of the module."""

        if path is None:
            path = [os.getcwd()]

        if '.' in fullname:
            name = fullname.split(sep='.')[-1]
        else:
            name = fullname

        for dir_name in path:
            path = cls._get_file_path(dir_name, name, cls.extension)
            if path:
                return spec_from_file_location(name=fullname, location=path, loader=cls())

        # could't import this one.
        return None

    def exec_module(self, module):
        """Call the respective handler for this module."""
        # pylint: disable=no-member
        self.handle_module(module, module.__spec__.origin)

    def __init_subclass__(cls):
        """
        Validate and append it to sys.meta_path if auto_enable is True
        """

        # Start validation.
        assert hasattr(cls, 'extension'), (
            f"Class variable 'extension' not present for class '{cls.__name__}'"
        )
        assert hasattr(cls, 'handle_module') and callable(cls.handle_module), (
            f"Method 'handle_module' not present for class '{cls.__name__}'"
        )
        args = set(getfullargspec(cls.handle_module).args)
        args.discard('self')
        assert len(args) == 2, (
            f"In class '{cls.__name__}' method handle_module should take 2 "
            f"arguements, but it is taking {len(args)}"
        )

        if getattr(cls, 'auto_enable', False) is True:
            sys.meta_path.append(cls())

    def module_repr(self, module):
        return (
            f"<module '{module.__name__}'> from '{module.__spec__.origin}'>"
        )
