import pytest
from rest_framework.test import APIClient
from app.models import Course
from model_bakery import baker
import random
import uuid



url = "http://127.0.0.1:8000/api/v1/courses/"


@pytest.fixture(scope='function')
def client():
    return APIClient()


@pytest.fixture(scope='function')
def fabric_model():
    def factory(*args, **kwargs):
        return baker.make(*args, **kwargs)
    return factory


@pytest.mark.django_db
@pytest.mark.parametrize('request_, status', [
    ('client.delete("%s1/")' % url, 204),
    ('client.get("%s")' % url, 200),
    ('client.get("%s?id=1")' % url, 400),
    ('client.post("%s", data={"name": "name"})' % url, 201),
    ('client.delete("%s2/")' % url, 404),
    ('client.patch("%s?id=5")' % url, 405),
    ('client.patch("%s5/")' % url, 404),
    ('client.put("%s?id=5")' % url, 405),
])
def test_status_courses_view_set(fabric_model, client, request_, status):
    fabric_model(Course, _quantity=1)
    response = eval(request_)
    assert response.status_code == status


@pytest.mark.django_db
def test_courses_get_one_object(client, fabric_model):
    courses = fabric_model(_model=Course, _quantity=3)

    response: APIClient() = client.get(
        path=url,
        query_params={'id': courses[0].id},
    )

    course = Course.objects.get(id=response.json()[0]['id'])
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert course == Course.objects.first()


@pytest.mark.django_db
def test_courses_get_all_objects(client, fabric_model):
    count = random.randint(100, 200)
    fabric_model(_model=Course, _quantity=count)

    response: APIClient() = client.get(
        path=url,
    )
    assert response.status_code == 200
    assert len(response.json()) == count


@pytest.mark.django_db
def test_post_courses_view_set(client):
    count = 100
    for i in range(count):
        response: APIClient() = client.post(
            path=url,
            data={'name': str(i)},
        )
        assert response.status_code == 201

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == count


@pytest.mark.django_db
def test_delete_and_filters_courses_view_set(client, fabric_model):
    fabric_model(Course, _quantity=3)
    course_id = Course.objects.first().id

    response_get1 = client.get(url, query_params={'id': course_id})
    response_del1 = client.delete(url + '{}/'.format(course_id))
    response_get2 = client.get(url, query_params={'id': course_id})
    response_del2 = client.delete(url + '{}/'.format(course_id))

    assert response_get1.status_code == 200
    assert response_get2.status_code == 400

    assert response_del1.status_code == 204
    assert response_del2.status_code == 404


@pytest.mark.django_db
def test_filter_name_course(client, fabric_model):
    fabric_model(Course, _quantity=100)
    courses = random.choice(Course.objects.all())

    response_true = client.get(url, query_params={'name': courses.name})
    response_false = client.get(url, query_params={'name': uuid.uuid4()})

    assert response_true.status_code == 200
    assert response_false.status_code == 200

    assert len(response_true.json()) == 1
    assert not len(response_false.json()) == 1
