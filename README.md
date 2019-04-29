<p align="center">
  <img src="https://deepsource.io/images/logo-wordmark-dark.svg" />
</p>

<p align="center">
  <a href="https://deepsource.io/docs">Documentation</a> |
  <a href="https://deepsource.io/signup">Get Started</a> |
  <a href="https://gitter.im/deepsourcelabs/lobby?utm_source=share-link&utm_medium=link&utm_campaign=share-link">Developer Chat</a>
</p>

<p align="center">
  DeepSource helps you ship good quality code.
</p>

</p>

---

# import-x

An ext-tensible loader to import anything like it is a python module.

Supports Python **3.6+**.

## Installation

```
pip install import-x
```

## Usage

Example json file in your path ``foo.json``:

```json
    {
        "why": "not",
    }
```

```python
   # Extend the ExtensionLoader and implement 'handle_module' method
   # where you will get a module object and the path to that module.

   >>> from import_x import ExtensionLoader

   >>> class JsonLoader(ExtensionLoader):
        extension = '.json'

        auto_enable = False

        @staticmethod
        def handle_module(module, path):
            """
            Load the json file and set as `data` attribute of the module.
            """
            json_file = Path(path)
            content = json_file.read_text()
            try:
                data = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                data = {}
            module.data = data

    >>> json_imports = JsonLoader()
    >>> with json_imports:
            import foo
    >>> foo.data
    >>> {"why": "not"}
```

If you want to enable imports automatically without the context_manager then just
do ``auto_enable = True`` in your loader.

This Example ``JsonLoader`` can be used directly by importing

```python
    from import_x.loaders.json_loader import JsonLoader
```

and you are ready to import all the json files.
