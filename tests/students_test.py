""" Adding test for student resource"""

def test_get_assignments_student_1(client, h_student_1):
    """
    List assignments for student_1
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data != []
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """
    List assignments for student_2 
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data != []
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_student_1(client, h_student_1):
    """
    Create assignment for student_1
    """

    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json = {
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']

    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_edit_and_repost_bad_id(client, h_student_1):
    """
    Create assignment for student_1
    """

    content = 'ABCD TESTPOST_UPDATED'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json = {
            'content': content,
            'id': 1000
        })

    assert response.status_code == 404
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'No assignment with this id was found'

def test_edit_and_repost_assignment_student_1(client, h_student_1):
    """
    Create assignment for student_1
    """

    content = 'ABCD TESTPOST_UPDATED'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json = {
            'content': content,
            'id': 6
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """
    Submit assignment for student_1 to teacher 2
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assingment_resubmitt_error(client, h_student_1):
    """
    failure case: Submit assignment for student_1 to teacher 2 again
    """

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    assert response.status_code == 400    
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'

def test_post_assignment_with_empty_content(client, h_student_2):
    """
    failure case: Create and submit assignment with empty content
    """
    content = ''

    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json = {
            'content': content
        })

    assert response.status_code == 200
    data = response.json['data']

    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': data['id'],
            'teacher_id': 2
        })
    assert response.status_code == 400
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'assignment with empty content cannot be submitted'

def test_post_assignment_with_empty_principal(client):
    """
    failure case: Create and submit assignment with empty content
    """
    content = ''

    response = client.post(
        '/student/assignments',
        headers='',
        json = {
            'content': content
        })

    assert response.status_code == 401
    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'principal not found'

def test_post_assignment_student_2(client, h_student_2):
    """
    Create assignment for student_2
    """

    content = 'ABCD TESTPOST2'

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