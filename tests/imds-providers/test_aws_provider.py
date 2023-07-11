# -*- coding: utf-8 -*-
"""Providers main test module."""
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
    with_statement,
)

# Supports Python2 and Python3 test mocks
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from watchmaker.utils.imds.detect.providers.aws_provider import AWSProvider

# @patch.object(AWSProvider, '_AWSProvider__get_server_metadata')
#     provider_mock.return_value = (
#         '{"imageId": "ami-12312412", "instanceId": "i-ec12as"}' \
#          .encode("utf8")
#     )


# def test_metadata_data_server_call_fail():
#     """Test calling the real metadata server and failing."""
#     provider = AWSProvider()
#     assert provider.check_metadata_server() is False


@patch.object(
    AWSProvider,
    "_AWSProvider__call_urlopen_retry",
    return_value=(
        '{"imageId": "ami-12312412", \
                            "instanceId": "i-ec12as"}'.encode(
            "utf8"
        )
    ),
)
@patch.object(
    AWSProvider,
    "_AWSProvider__request_token",
    return_value=(None),
)
def test_aws_check_metadata_server_is_valid(mock_urlopen, mock_request_token):
    """Test valid server data response for aws provider identification."""
    provider = AWSProvider()
    assert provider.check_metadata_server() is True


@patch.object(
    AWSProvider,
    "_AWSProvider__call_urlopen_retry",
    return_value=(
        '{"imageId": "not-valid", \
                            "instanceId": "etc-ec12as"}'.encode(
            "utf8"
        )
    ),
)
@patch.object(
    AWSProvider,
    "_AWSProvider__request_token",
    return_value=(None),
)
def test_aws_check_metadata_server_is_invalid(
    mock_urlopen, mock_request_token
):
    """Test invalid server data response for aws provider identification."""
    provider = AWSProvider()
    assert provider.check_metadata_server() is False


@patch.object(
    AWSProvider,
    "_AWSProvider__call_urlopen_retry",
    return_value=("abcdefgh1234546"),
)
def test_aws_check_request_token(mock_urlopen):
    """Test token is saved to imds_token."""
    provider = AWSProvider()
    assert provider._AWSProvider__request_token() is None
    assert AWSProvider.imds_token == "abcdefgh1234546"


@patch.object(
    AWSProvider,
    "_AWSProvider__call_urlopen_retry",
    return_value=(None),
)
def test_aws_check_request_token_none(mock_urlopen):
    """Test token is not saved to imds_token."""
    provider = AWSProvider()
    assert provider._AWSProvider__request_token() is None
    assert AWSProvider.imds_token == None
