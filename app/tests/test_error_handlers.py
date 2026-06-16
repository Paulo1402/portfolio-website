from django.test import RequestFactory, TestCase

from app.views import handler_404, handler_500


class ErrorHandlerTests(TestCase):
    def test_handler_404_logs_request_path(self):
        request = RequestFactory().get("/missing-page/")

        with self.assertLogs("app.views", level="WARNING") as logs:
            response = handler_404(request, Exception("not found"))

        self.assertEqual(response.status_code, 404)
        self.assertIn("/missing-page/", logs.output[0])

    def test_handler_500_logs_request_path(self):
        request = RequestFactory().get("/broken-page/")

        with self.assertLogs("app.views", level="ERROR") as logs:
            try:
                raise RuntimeError("broken")
            except RuntimeError:
                response = handler_500(request)

        self.assertEqual(response.status_code, 500)
        self.assertIn("/broken-page/", logs.output[0])
