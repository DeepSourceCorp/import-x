from import_x.loaders import json_loader  # pylint: disable=unused-import


def test_handle_module():
    from .fixtures import payload
    assert payload.data == {"test": "import_x"}
