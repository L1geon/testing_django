import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_cource(client, course_factory):
    # Arrange
    courses = course_factory()
    print(courses.id, courses.name)

    # Act
    response = client.get(f'/api/v1/courses/{courses.id}/')
    print(response)
    # Assert
    data = response.json()
    assert response.status_code == 200
    assert courses.name == data['name']


@pytest.mark.django_db
def test_get_cources(client, course_factory):
    # Arrange
    quant = 999
    courses = course_factory(_quantity=quant)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == quant
    for i, course in enumerate(data):
        assert courses[i].name == course['name']


@pytest.mark.django_db
def test_get_filter_cources_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=9)
    i = 6

    # Act
    response = client.get('/api/v1/courses/', {'id': courses[i].id, 'name': courses[i].name}, )
    print(response.json())
    # Assert

    assert response.status_code == 200
    assert courses[i].id == response.json()[0]['id']


@pytest.mark.django_db
def test_get_filter_cources_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=20)
    i = 6

    # Act
    response = client.get('/api/v1/courses/', {'id': courses[i].id, 'name': courses[i].name}, )
    print(response.json())
    # Assert

    assert response.status_code == 200
    assert courses[i].name == response.json()[0]['name']


@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    count = Course.objects.count()
    name = 'Python from zero'
    # Act
    response1 = client.post('/api/v1/courses/', data={'name': name})
    response2 = client.get(f'/api/v1/courses/?name={name}')
    response3 = client.get(f'/api/v1/courses/{response1.json()["id"]}/')
    # Assert
    assert response1.status_code == 201
    assert Course.objects.count() == count + 1
    assert response2.status_code == 200
    assert name == response3.json()['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=2)
    # Act
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'Python from zero'})
    # Assert
    assert response.status_code == 200
    assert response.json()['name'] == 'Python from zero'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=2)
    # Act
    response = client.delete(f'/api/v1/courses/{courses[1].id}/')
    # Assert
    assert response.status_code == 204
