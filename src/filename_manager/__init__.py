try:
    from importlib.metadata import version

    __version__ = version("filename-manager")
except ImportError:
    from importlib_metadata import version as version_old  # For Python < 3.8

    __version__ = version_old("filename-manager")
