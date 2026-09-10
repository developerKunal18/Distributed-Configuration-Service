import app as m

def setup_function():
    m._configs.clear();m._history.clear()

def test_health():
    assert m.app.test_client().get("/health").status_code==200

def test_create():
    r=m.app.test_client().put("/api/config/payment",json={"environment":"production","config":{"timeout":30}})
    assert r.status_code==201 and r.json["version"]==1

def test_update_version():
    c=m.app.test_client()
    c.put("/api/config/payment",json={"environment":"production","config":{"timeout":30}})
    r=c.put("/api/config/payment",json={"environment":"production","config":{"timeout":60}})
    assert r.status_code==200 and r.json["version"]==2

def test_get():
    c=m.app.test_client()
    c.put("/api/config/payment",json={"environment":"production","config":{"retries":3}})
    r=c.get("/api/config/payment?environment=production")
    assert r.status_code==200 and r.json["config"]["retries"]==3

def test_history():
    c=m.app.test_client()
    for n in (10,20,30):
        c.put("/api/config/payment",json={"environment":"production","config":{"timeout":n}})
    r=c.get("/api/config/payment/history?environment=production")
    assert r.json["count"]==3 and r.json["versions"][-1]["version"]==3

def test_missing():
    assert m.app.test_client().get("/api/config/unknown").status_code==404

def test_invalid():
    r=m.app.test_client().put("/api/config/payment",json={"config":"bad"})
    assert r.status_code==400
