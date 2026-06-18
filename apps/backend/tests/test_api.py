import pytest


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["app"] == "AI Marketing OS"


@pytest.mark.asyncio
async def test_register(client):
    payload = {
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User",
        "role": "viewer",
    }
    r = await client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate(client):
    payload = {
        "email": "dupe@example.com",
        "password": "TestPass123!",
        "full_name": "Duplicate",
    }
    r1 = await client.post("/api/v1/auth/register", json=payload)
    assert r1.status_code == 201
    r2 = await client.post("/api/v1/auth/register", json=payload)
    assert r2.status_code == 409


@pytest.mark.asyncio
async def test_login(client):
    email = "login@example.com"
    await client.post("/api/v1/auth/register", json={
        "email": email, "password": "TestPass123!", "full_name": "Login Test",
    })
    r = await client.post("/api/v1/auth/login", json={
        "email": email, "password": "TestPass123!",
    })
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client):
    r = await client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com", "password": "wrong",
    })
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client):
    email = "me@example.com"
    await client.post("/api/v1/auth/register", json={
        "email": email, "password": "TestPass123!", "full_name": "Me",
    })
    login_r = await client.post("/api/v1/auth/login", json={
        "email": email, "password": "TestPass123!",
    })
    token = login_r.json()["access_token"]
    r = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == email


@pytest.mark.asyncio
async def test_campaign_crud(client):
    email = "campaign@example.com"
    await client.post("/api/v1/auth/register", json={
        "email": email, "password": "TestPass123!", "full_name": "Campaign User",
    })
    login_r = await client.post("/api/v1/auth/login", json={
        "email": email, "password": "TestPass123!",
    })
    token = login_r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = await client.post("/api/v1/campaigns/", json={
        "name": "Test Campaign", "goal": "Increase awareness",
    }, headers=headers)
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    r = await client.get("/api/v1/campaigns/", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    r = await client.get(f"/api/v1/campaigns/{cid}", headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Test Campaign"

    r = await client.patch(f"/api/v1/campaigns/{cid}", json={
        "name": "Updated Campaign",
    }, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Updated Campaign"
