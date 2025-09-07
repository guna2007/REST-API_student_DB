# uvicorn app.main:app -> then append /docs
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.json()["working"] == "Good"

def test_post_student():
    resp = client.post("/students",json={"name" : "GUna","age" : 18,"grade" : 9})
    assert resp.status_code == 201
    newstudent = resp.json()
    assert "id" in newstudent and newstudent["name"] == "Guna" and newstudent["age"] == 18 and newstudent["grade"] == 9

def test_search_students():
    #no filters
    client.post("/students", json={"name": "Guna", "age": 18, "grade": 9})
    client.post("/students", json={"name": "sai", "age": 15, "grade": 8})
    client.post("/students", json={"name": "teja", "age": 17, "grade": 7})

    resp1 = client.get("/students")
    assert resp1.status_code == 200
    assert len(resp1.json()) >= 3

    #with filters
    resp2 = client.get("/students?min_age=17")
    assert resp2.status_code == 200
    assert all(s["age"] >= 17 for s in resp2.json())

    resp3 = client.get("/students?grade=8")
    assert resp3.status_code == 200
    assert all(s["grade"] == 8 for s in resp3.json())

    resp4 = client.get("/students?search=a")
    assert resp4.status_code == 200
    assert all("a" in s["name"].lower() for s in resp4.json())

    #with 2 filters
    resp5 = client.get("/students?min_age=15&grade=9")
    assert resp5.status_code == 200
    assert all(s["age"] >= 15 and s["grade"] == 9 for s in resp5.json())

    #for 404error
    resp5 = client.get("/students/?min_age=50")
    assert resp5.status_code == 404
    assert resp5.json()["detail"] == "Data not Found"

def test_get_byID():
    resp = client.post("/students",json={"name" : "CHaran","age" : 19,"grade" : 6})
    testcase = resp.json()
    test_ID = testcase["id"]
    # checks id
    resp1 = client.get(f"/student/{test_ID}")
    assert resp1.status_code == 200
    assert resp1.json()["id"] == test_ID
    # for 404 error
    resp2 = client.get(f"/student/40")
    assert resp2.status_code == 404
    assert resp2.json()["detail"] == "Data not Found 40"
    # for invalid id
    resp3 = client.get(f"/student/-2")
    assert resp3.status_code == 422

def test_delete_byID():
    resp = client.post("/students",json={"name" : "Surya","age" : 19,"grade" : 10})
    testcase = resp.json()
    test_ID = testcase["id"]
    # delete success
    resp1 = client.delete(f"/student/{test_ID}")
    assert resp1.status_code == 200
    assert resp1.json()[f"{test_ID}"] == "deleted"
    # check del id
    resp2 = client.get(f"/student/{test_ID}")
    assert resp2.json()["detail"] == f"Data not Found {test_ID}"
    # invalid id
    resp3 = client.delete("/student/99")
    assert resp3.status_code == 404
    assert resp3.json()["detail"] == "ID not found"

def test_update_byID():
    resp = client.post("/students",json={"name" : "Madhab","age" : 20,"grade" : 6})
    testcase = resp.json()
    test_ID = testcase["id"]
    # update success
    resp1 = client.put(f"/student/{test_ID}?name=MaDhaN&age=21&grade=8")
    assert resp1.status_code == 200
    updatedcase = resp1.json()
    assert updatedcase["name"] == "Madhan"
    assert updatedcase["age"] == 21
    assert updatedcase["grade"] == 8
    assert updatedcase["id"] == test_ID
    # invalid id
    resp2 = client.put("/student/400")
    assert resp2.status_code == 404
    assert resp2.json()["detail"] == "ID not Found"
    # invalid params
    resp3 = client.put(f"/student/{test_ID}?name=123&age=-2&grade=1")
    assert resp3.status_code == 422
    # no update
    resp4 = client.put(f"/student/{test_ID}")
    assert resp4.status_code == 200
    unchanged = resp4.json()
    assert unchanged == updatedcase

#pythonpath=. pytest