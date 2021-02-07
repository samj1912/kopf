import copy

import pytest

import kopf

strict_mode = pytest.mark.parametrize('strictness', [
    pytest.param(dict(strict=True), id='strictTrue'),
])
non_strict_mode = pytest.mark.parametrize('strictness', [
    pytest.param(dict(strict=False), id='strictFalse'),
    pytest.param(dict(), id='strictAbsent'),
])
any_strict_mode = pytest.mark.parametrize('strictness', [
    pytest.param(dict(strict=True), id='strictTrue'),
    pytest.param(dict(strict=False), id='strictFalse'),
    pytest.param(dict(), id='strictAbsent'),
])

obj1_with_names = pytest.mark.parametrize('obj1', [
    pytest.param({'metadata': {'name': 'a'}}, id='regularname'),
    pytest.param({'metadata': {'generateName': 'b'}}, id='generatename'),
    pytest.param({'metadata': {'name': 'c', 'generateName': 'd'}}, id='bothnames'),
])
obj2_with_names = pytest.mark.parametrize('obj2', [
    pytest.param({'metadata': {'name': 'a'}}, id='regularname'),
    pytest.param({'metadata': {'generateName': 'b'}}, id='generatename'),
    pytest.param({'metadata': {'name': 'c', 'generateName': 'd'}}, id='bothnames'),
])
obj1_without_names = pytest.mark.parametrize('obj1', [
    pytest.param({}, id='withoutmeta'),
    pytest.param({'metadata': {}}, id='withmeta'),
])
obj2_without_names = pytest.mark.parametrize('obj2', [
    pytest.param({}, id='withoutmeta'),
    pytest.param({'metadata': {}}, id='withmeta'),
])


# The EXISTING names are preserved.
# The strictness is not involved due to this (no new names added).
@obj1_with_names
@any_strict_mode
def test_preserved_name_of_dict(strictness, obj1):
    obj1 = copy.deepcopy(obj1)
    kopf.harmonize_naming(obj1, name='provided-name', **strictness)
    assert obj1['metadata'].get('name') != 'provided-name'
    assert obj1['metadata'].get('generateName') != 'provided-name'


@obj2_with_names
@obj1_with_names
@any_strict_mode
def test_preserved_names_of_dicts(strictness, multicls, obj1, obj2):
    obj1, obj2 = copy.deepcopy(obj1), copy.deepcopy(obj2)
    objs = multicls([obj1, obj2])
    kopf.harmonize_naming(objs, name='provided-name', **strictness)
    assert obj1['metadata'].get('name') != 'provided-name'
    assert obj2['metadata'].get('name') != 'provided-name'
    assert obj1['metadata'].get('generateName') != 'provided-name'
    assert obj2['metadata'].get('generateName') != 'provided-name'


# When names are ABSENT, they are added.
# The only varying part is which name is added: regular or generated.
@obj1_without_names
@strict_mode
def test_assignment_of_strict_name_of_dict(strictness, obj1):
    obj1 = copy.deepcopy(obj1)
    kopf.harmonize_naming(obj1, name='provided-name', **strictness)
    assert 'name' in obj1['metadata']
    assert 'generateName' not in obj1['metadata']
    assert obj1['metadata']['name'] == 'provided-name'


@obj2_without_names
@obj1_without_names
@strict_mode
def test_assignment_of_strict_names_of_dicts(strictness, multicls, obj1, obj2):
    obj1, obj2 = copy.deepcopy(obj1), copy.deepcopy(obj2)
    objs = multicls([obj1, obj2])
    kopf.harmonize_naming(objs, name='provided-name', **strictness)
    assert 'name' in obj1['metadata']
    assert 'name' in obj2['metadata']
    assert 'generateName' not in obj1['metadata']
    assert 'generateName' not in obj2['metadata']
    assert obj1['metadata']['name'] == 'provided-name'
    assert obj2['metadata']['name'] == 'provided-name'


@obj1_without_names
@non_strict_mode
def test_assignment_of_nonstrict_name_of_dict(strictness, obj1):
    obj1 = copy.deepcopy(obj1)
    kopf.harmonize_naming(obj1, name='provided-name', **strictness)
    assert 'name' not in obj1['metadata']
    assert 'generateName' in obj1['metadata']
    assert obj1['metadata']['generateName'] == 'provided-name-'


@obj2_without_names
@obj1_without_names
@non_strict_mode
def test_assignment_of_nonstrict_names_of_dicts(strictness, multicls, obj1, obj2):
    obj1, obj2 = copy.deepcopy(obj1), copy.deepcopy(obj2)
    objs = multicls([obj1, obj2])
    kopf.harmonize_naming(objs, name='provided-name', **strictness)
    assert 'name' not in obj1['metadata']
    assert 'name' not in obj2['metadata']
    assert 'generateName' in obj1['metadata']
    assert 'generateName' in obj2['metadata']
    assert obj1['metadata']['generateName'] == 'provided-name-'
    assert obj2['metadata']['generateName'] == 'provided-name-'
