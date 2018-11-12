import pytest
import store_image


@pytest.fixture()
def run_store_image():
    return store_image.main()