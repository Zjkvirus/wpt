# mypy: allow-untyped-defs

from ..schema import WebFeaturesFile, FeatureEntry, SpecialFileEnum, FeatureFile

import pytest
import re

@pytest.mark.parametrize(
    "input,expected_result,expected_exception_type,exception_message",
    [
        (
            {
                "features": [
                    {
                        "name": "feature1",
                        "files": ["file1", "file2"],
                    }
                ]
            },
            WebFeaturesFile(features=[
                FeatureEntry(name="feature1",
                             files=[FeatureFile("file1"), FeatureFile("file2")])]),
            None,
            None
        ),
        (
            {},
            None,
            ValueError,
            "Object missing required keys: ['features']"
        ),
        (
            {
                "features": [
                    {}
                ]
            },
            None,
            ValueError,
            "Object missing required keys: ['files', 'name']"
        ),
    ])
def test_from_dict(input, expected_result, expected_exception_type, exception_message):
    if expected_exception_type:
        with pytest.raises(expected_exception_type, match=re.escape(exception_message)):
            WebFeaturesFile.from_dict(input)
    else:
        assert expected_result == WebFeaturesFile.from_dict(input)

@pytest.mark.parametrize(
    "input,expected_result",
    [
        (
            FeatureEntry(name="test1", files=[FeatureFile("file1")]),
            False
        ),
        (
            FeatureEntry(name="test2", files=SpecialFileEnum.RECURSIVE),
            True
        ),
    ])
def test_does_feature_apply_recursively(input, expected_result):
    assert input.does_feature_apply_recursively() == expected_result

@pytest.mark.parametrize(
    "input_feature,input_file,expected_result",
    [
        (
            FeatureFile("test.html"),
            "test.html",
            True
        ),
        (
            FeatureFile("test*.html"),
            "test2.html",
            True
        ),
        (
            FeatureFile("test-*.html"),
            "test2.html",
            False
        ),
    ])
def test_feature_file_match(input_feature, input_file, expected_result):
    assert input_feature.match(input_file) == expected_result
