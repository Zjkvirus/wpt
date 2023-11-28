from enum import Enum
from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Any, Sequence, Union

from ..schema import SchemaValue, validate_dict

"""
YAML filename for meta files
"""
WEB_FEATURES_YML_FILENAME = "WEB_FEATURES.yml"


class SpecialFileEnum(Enum):
    """All files recursively"""
    RECURSIVE = "**"


class FeatureFile(str):
    def match(self, input_base_filename: str) -> bool:
        return fnmatchcase(input_base_filename, self)

@dataclass
class FeatureEntry:
    files: Union[Sequence[FeatureFile], SpecialFileEnum]
    """The web feature key"""
    name: str

    _required_keys = {"files", "name"}

    @staticmethod
    def from_dict(obj: Any) -> 'FeatureEntry':
        """
        Converts the provided dictionary to an instance of FeatureEntry
        :param obj: The object that will be converted to a FeatureEntry.
        :return: An instance of FeatureEntry
        :raises ValueError: If there unexpected keys or missing required keys.
        """
        assert isinstance(obj, dict)
        validate_dict(obj, FeatureEntry._required_keys)
        files = SchemaValue.from_union([
            lambda x: SchemaValue.from_list(SchemaValue.from_class(FeatureFile), x),
            SpecialFileEnum], obj.get("files"))
        name = SchemaValue.from_str(obj.get("name"))
        return FeatureEntry(files, name)


    def does_feature_apply_recursively(self) -> bool:
        if isinstance(self.files, SpecialFileEnum) and self.files == SpecialFileEnum.RECURSIVE:
            return True
        return False


@dataclass
class WebFeaturesFile:
    """List of features"""
    features: Sequence[FeatureEntry]

    _required_keys = {"features"}

    @staticmethod
    def from_dict(obj: Any) -> 'WebFeaturesFile':
        """
        Converts the provided dictionary to an instance of WebFeaturesFile
        :param obj: The object that will be converted to a WebFeaturesFile.
        :return: An instance of WebFeaturesFile
        :raises ValueError: If there unexpected keys or missing required keys.
        """
        assert isinstance(obj, dict)
        validate_dict(obj, WebFeaturesFile._required_keys)
        features = SchemaValue.from_list(FeatureEntry.from_dict, obj.get("features"))
        return WebFeaturesFile(features)
