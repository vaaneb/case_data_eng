from uuid import uuid4


class TestCreateUser:
    def should_return_201_with_user_data_when_valid_payload(self, client, sample_user_data):
        # Act
        response = client.post("/api/v1/users/", json=sample_user_data)

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 201
        assert data["first_name"] == sample_user_data["first_name"]
        assert data["last_name"] == sample_user_data["last_name"]
        assert data["email"] == sample_user_data["email"]
        assert data["phone"] == sample_user_data["phone"]
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    def should_return_409_when_email_already_exists(self, client, created_user, sample_user_data):
        # Act
        sample_user_data["phone"] = "11888888888"
        response = client.post("/api/v1/users/", json=sample_user_data)

        # Assert
        assert response.status_code == 409

    def should_return_409_when_phone_already_exists(self, client, created_user, sample_user_data):
        # Act
        sample_user_data["email"] = "other@example.com"
        response = client.post("/api/v1/users/", json=sample_user_data)

        # Assert
        assert response.status_code == 409

    def should_return_422_when_email_is_invalid(self, client, sample_user_data):
        # Act
        sample_user_data["email"] = "not-an-email"
        response = client.post("/api/v1/users/", json=sample_user_data)

        # Assert
        assert response.status_code == 422

    def should_return_422_when_required_fields_are_missing(self, client):
        # Act
        response = client.post("/api/v1/users/", json={})

        # Assert
        assert response.status_code == 422


class TestGetUser:
    def should_return_user_when_id_exists(self, client, created_user):
        # Act
        user_id = created_user["id"]
        response = client.get(f"/api/v1/users/{user_id}")

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["id"] == user_id

    def should_return_404_when_id_does_not_exist(self, client):
        # Act
        response = client.get(f"/api/v1/users/{uuid4()}")

        # Assert
        assert response.status_code == 404


class TestListUsers:
    def should_return_empty_list_when_no_users_exist(self, client):
        # Act
        response = client.get("/api/v1/users/")

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data == []

    def should_return_all_users_when_no_search_filter(self, client, created_user):
        # Act
        response = client.get("/api/v1/users/")

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["id"] == created_user["id"]

    def should_return_matching_users_when_search_matches(self, client, created_user):
        # Act
        response = client.get("/api/v1/users/", params={"search": "John"})

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == 1

    def should_return_empty_list_when_search_has_no_match(self, client, created_user):
        # Act
        response = client.get("/api/v1/users/", params={"search": "zzzzz"})

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert len(data) == 0


class TestUpdateUser:
    def should_return_updated_user_when_valid_payload(self, client, created_user):
        # Act
        user_id = created_user["id"]
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"first_name": "Jane"},
        )

        # Result
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert data["first_name"] == "Jane"
        assert data["last_name"] == created_user["last_name"]

    def should_return_404_when_user_does_not_exist(self, client):
        # Act
        response = client.put(
            f"/api/v1/users/{uuid4()}",
            json={"first_name": "Jane"},
        )

        # Assert
        assert response.status_code == 404

    def should_return_409_when_email_belongs_to_another_user(self, client, created_user, sample_user_data):
        # Act
        second = client.post("/api/v1/users/", json={
            **sample_user_data,
            "email": "other@example.com",
            "phone": "11888888888",
        }).json()

        response = client.put(
            f"/api/v1/users/{second['id']}",
            json={"email": created_user["email"]},
        )

        # Assert
        assert response.status_code == 409

    def should_return_422_when_extra_field_is_sent(self, client, created_user):
        # Act
        response = client.put(
            f"/api/v1/users/{created_user['id']}",
            json={"unknown_field": "value"},
        )

        # Assert
        assert response.status_code == 422


class TestDeleteUser:
    def should_return_204_and_remove_user_when_id_exists(self, client, created_user):
        # Act
        user_id = created_user["id"]
        response = client.delete(f"/api/v1/users/{user_id}")

        # Assert
        assert response.status_code == 204

        # Act - verify user was removed
        response = client.get(f"/api/v1/users/{user_id}")

        # Assert
        assert response.status_code == 404

    def should_return_404_when_user_does_not_exist(self, client):
        # Act
        response = client.delete(f"/api/v1/users/{uuid4()}")

        # Assert
        assert response.status_code == 404
