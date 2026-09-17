import unittest

from regional_reachability import evaluate


def fixture():
    return {"status": "finished", "results": [{"probe": {"country": "DE"}, "result": {
        "status": "finished", "statusCode": 200, "tls": {"authorized": True}, "rawBody": "<title>Tons of Skills</title>"}}]}


class RegionalTests(unittest.TestCase):
    def test_malformed_nested_results_fail_closed(self):
        for value in [None, {}, [None], [{"probe": [], "result": []}],
                      [{"probe": {"country": []}, "result": {"tls": [], "rawBody": []}}]]:
            self.assertFalse(evaluate({"status": "finished", "results": value}, ["DE"])["ok"])

    def test_complete_success(self):
        self.assertTrue(evaluate(fixture(), ["DE"])["ok"])

    def test_missing_country_does_not_pass(self):
        self.assertFalse(evaluate(fixture(), ["DE", "IN"])["ok"])

    def test_failed_http_untrusted_tls_wrong_content_and_duplicate_fail(self):
        for change in [{"statusCode": 403}, {"tls": {"authorized": False}}, {"rawBody": "error page"}]:
            data = fixture()
            data["results"][0]["result"].update(change)
            self.assertFalse(evaluate(data, ["DE"])["ok"])
        data = fixture()
        data["results"] *= 2
        self.assertFalse(evaluate(data, ["DE"])["ok"])

    def test_incomplete_and_no_results_fail(self):
        for data in [None, {"status": "in-progress"}, {"status": "finished", "results": []}]:
            self.assertFalse(evaluate(data, ["DE"])["ok"])


if __name__ == "__main__":
    unittest.main()
