# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import io
import sys

import pytest
from PIL import Image
from pixelmatch import pixelmatch
from pixelmatch.contrib.PIL import from_PIL_to_raw_data

from playwright._impl._path_utils import get_file_dirname

from .server import test_server

_dirname = get_file_dirname()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def assetdir():
    return _dirname / "assets"


@pytest.fixture
def server():
    yield test_server.server


@pytest.fixture
def https_server():
    yield test_server.https_server


@pytest.fixture
def ws_server():
    yield test_server.ws_server


@pytest.fixture(autouse=True, scope="session")
async def start_server():
    test_server.start()
    yield
    test_server.stop()


@pytest.fixture(autouse=True)
def after_each_hook():
    yield
    test_server.reset()


@pytest.fixture(scope="session")
def is_win():
    return sys.platform == "win32"


@pytest.fixture(scope="session")
def is_linux():
    return sys.platform == "linux"


@pytest.fixture(scope="session")
def is_mac():
    return sys.platform == "darwin"


def _get_skiplist(request, values, value_name):
    skipped_values = []
    # Allowlist
    only_marker = request.node.get_closest_marker(f"only_{value_name}")
    if only_marker:
        skipped_values = values
        skipped_values.remove(only_marker.args[0])

    # Denylist
    skip_marker = request.node.get_closest_marker(f"skip_{value_name}")
    if skip_marker:
        skipped_values.append(skip_marker.args[0])

    return skipped_values


@pytest.fixture(autouse=True)
def skip_by_platform(request):
    skip_platform_names = _get_skiplist(
        request, ["win32", "linux", "darwin"], "platform"
    )

    if sys.platform in skip_platform_names:
        pytest.skip(f"skipped on this platform: {sys.platform}")


@pytest.fixture(scope="session")
def assert_to_be_golden(browser_name: str):
    def compare(received_raw: bytes, golden_name: str):
        golden_file = (_dirname / f"golden-{browser_name}" / golden_name).read_bytes()
        received_image = Image.open(io.BytesIO(received_raw))
        golden_image = Image.open(io.BytesIO(golden_file))

        if golden_image.size != received_image.size:
            pytest.fail("Image size differs to golden image")
            return
        diff_pixels = pixelmatch(
            from_PIL_to_raw_data(received_image),
            from_PIL_to_raw_data(golden_image),
            golden_image.size[0],
            golden_image.size[1],
            threshold=0.2,
        )
        assert diff_pixels == 0

    return compare
