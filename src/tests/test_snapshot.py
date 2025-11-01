"""Tests for the humidifier platform."""

from contextlib import nullcontext
import logging
from unittest.mock import patch

import pytest
from pyvesync import VeSync
from syrupy.assertion import SnapshotAssertion


from .common import (
    ALL_DEVICE_NAMES,
    mock_devices_response,
)

from tests.test_util.aiohttp import AiohttpClientMocker

NoException = nullcontext()


@pytest.mark.parametrize("device_name", ALL_DEVICE_NAMES)
async def test_device_state(
    snapshot: SnapshotAssertion,
    vesync_manager: VeSync,
    aioclient_mock: AiohttpClientMocker,
    device_name: str,
) -> None:
    """Test the device objects match the snapshots."""

    # Configure the API devices call for device_name
    mock_devices_response(aioclient_mock, device_name)

    # setup platform - only including the named device
    await vesync_manager.get_devices()
    await vesync_manager.update_all_devices()

    # Check device
    devices = vesync_manager.get_device_by_name(device_name)
    assert devices == snapshot(name="device")