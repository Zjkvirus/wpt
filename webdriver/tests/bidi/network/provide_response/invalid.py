import pytest
import webdriver.bidi.error as error

pytestmark = pytest.mark.asyncio

PAGE_EMPTY_TEXT = "/webdriver/tests/bidi/network/support/empty.txt"


@pytest.mark.parametrize("value", [None, False, 42, {}, []])
async def test_params_request_invalid_type(bidi_session, value):
    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.provide_response(request=value)


@pytest.mark.parametrize("value", ["", "foo"])
async def test_params_request_invalid_value(bidi_session, value):
    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.provide_response(request=value)


async def test_params_request_no_such_request(bidi_session, setup_network_test,
                                              wait_for_event, fetch, url):
    await setup_network_test(events=[
        "network.responseCompleted",
    ])
    on_response_completed = wait_for_event("network.responseCompleted")

    text_url = url(PAGE_EMPTY_TEXT)
    await fetch(text_url)

    response_completed_event = await on_response_completed
    request = response_completed_event["request"]["request"]

    with pytest.raises(error.NoSuchRequestException):
        await bidi_session.network.provide_response(request=request)


@pytest.mark.parametrize("value", [False, 42, {}, []])
async def test_params_reason_phrase_invalid_type(setup_blocked_request,
                                                 bidi_session,
                                                 value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.provide_response(request=request,
                                                    reason_phrase=value)


@pytest.mark.parametrize("value", [False, "s", {}, []])
async def test_params_status_code_invalid_type(setup_blocked_request, bidi_session,
                                               value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.provide_response(request=request,
                                                    status_code=value)


@pytest.mark.parametrize("value", [-1, 4.3])
async def test_params_status_code_invalid_value(setup_blocked_request, bidi_session, value):
    request = await setup_blocked_request("beforeRequestSent")

    with pytest.raises(error.InvalidArgumentException):
        await bidi_session.network.provide_response(request=request,
                                                    status_code=value)


# TODO: Add body.
# TODO: Add cookies.
# TODO: Add headers.
