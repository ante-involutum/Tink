import pytest


@pytest.mark.usefixtures('init')
class TestController():

    def test_create_job(self):
        payload = {
            "name": "jmx",
            "jmx": "/jmx/example.jmx"
        }
        resp = self.bs.post('/tink/job', json=payload)
        assert resp.status_code == 200

    def test_get_jobs(self):
        resp = self.bs.get('/tink/jobs')
        assert resp.status_code == 200

    def test_get_job(self):
        resp = self.bs.get(f'/tink/job/jmx')
        assert resp.status_code == 200

    def test_updata_job(self):
        resp = self.bs.patch(f'/tink/job/jmx')
        assert resp.status_code == 200

    def test_delete_job(self):
        resp = self.bs.delete(f'/tink/job/jmx')
        assert resp.status_code == 200
