def test_get_assignments_teacher_1(client, h_teacher_1):
    """
    List assignments for teacher_1
    """
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data != []
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] == 'SUBMITTED'

def test_get_assignments_teacher_2(client, h_teacher_2):
    """
    List assignments for teacher_2
    """
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data != []
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] == 'SUBMITTED'


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )
    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'This assignment belongs to some other teacher'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should not allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    error_response = response.json
    assert error_response["message"] == ['Invalid grade input']

def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment exists else throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

def test_grade_assignment_empty_id(client, h_teacher_1):
    """
    failure case: If an assignment exists else throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": '',
            "grade": "A"
        }
    )

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'ValidationError'
    assert error_response["message"] == {'id': ['Not a valid integer.']}


def test_grade_assignment_draft_assignment(client, h_teacher_1, h_student_2):
    """
    failure case: only a submitted assignment can be graded
    """

    content = 'ONLY DRAFT'

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json = {
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": data['id'],
            "grade": "A"
        }
    )

    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a SUBMITTED assignment can be graded'

def test_grade_assignment_graded(client, h_teacher_2):
    """
        correct grade should be assiged and marked GRADED
    """

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 3,
            "grade": "B"
        }
    )
    data = response.json['data']
    assert response.status_code == 200
    assert data['state'] == "GRADED"
    assert data['grade'] == "B"
    assert data['teacher_id'] == 2