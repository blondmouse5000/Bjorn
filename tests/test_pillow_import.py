def test_pillow_import():
    # Simple smoke test to ensure Pillow can be imported in CI
    import PIL
    from PIL import Image
    assert hasattr(PIL, '__version__')
    assert Image is not None
