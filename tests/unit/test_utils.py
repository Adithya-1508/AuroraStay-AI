from shared.utils import generate_uuid


def test_generate_uuid_without_prefix() -> None:
    val = generate_uuid()
    assert val is not None
    assert len(val) > 0


def test_generate_uuid_with_prefix() -> None:
    prefix = "tst"
    val = generate_uuid(prefix)
    assert val.startswith("tst_")
