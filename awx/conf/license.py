# Copyright (c) 2016 Ansible, Inc.
# All Rights Reserved.

# Django
from django.utils.translation import ugettext_lazy as _

# Django REST Framework
from rest_framework.exceptions import APIException

# Tower
from awx.main.task_engine import TaskEnhancer

__all__ = ['LicenseForbids', 'get_license', 'get_licensed_features',
           'feature_enabled', 'feature_exists']


class LicenseForbids(APIException):
    status_code = 402
    default_detail = _('Your Tower license does not allow that.')


def _get_validated_license_data():
    return TaskEnhancer().validate_enhancements()


def get_license(show_key=False):
    """Return a dictionary representing the active license on this Tower instance."""
    license_data = _get_validated_license_data()
    if not show_key:
        license_data.pop('license_key', None)
    return license_data


def get_licensed_features():
    """Return a set of all features enabled by the active license."""
    features = set()
    for feature, enabled in _get_validated_license_data().get('features', {}).items():
        if enabled:
            features.add(feature)
    return features


def feature_enabled(name):
    """Return True if the requested feature is enabled, False otherwise."""
    return _get_validated_license_data().get('features', {}).get(name, False)


def feature_exists(name):
    """Return True if the requested feature name exists, False otherwise."""
    return bool(name in _get_validated_license_data().get('features', {}))
