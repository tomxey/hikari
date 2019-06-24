#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asynctest
import pytest


@pytest.fixture()
def http_client(event_loop):
    from hikari_tests.test_net.test_http import ClientMock

    return ClientMock(token="foobarsecret", loop=event_loop)


@pytest.mark.asyncio
async def test_create_reaction(http_client):
    http_client.request = asynctest.CoroutineMock()
    await http_client.create_reaction("696969", "12", "\N{OK HAND SIGN}")
    http_client.request.assert_awaited_once_with(
        "put",
        "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
        channel_id="696969",
        message_id="12",
        emoji="\N{OK HAND SIGN}",
    )