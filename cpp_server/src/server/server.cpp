#include "../api/python_server.hpp"
#include "../utils/log.hpp"
#include "httplib.h"

using namespace httplib;

void run_server() {
  Server svr;

  svr.Get("/health", [](const httplib::Request &, httplib::Response &res) {
    res.set_content("ok", "text/plain");
  });

  svr.Get("/logs", [](const httplib::Request &, httplib::Response &res) {
    std::string logs = get_logs_string();
    res.set_content(logs, "text/plain");
  });

  svr.Get("/py/(.+)", [](const httplib::Request &req, httplib::Response &res) {
    std::string response;
    python_server_get("/" + req.matches[1].str(), &response);
    res.set_content(response, "text/plain");
  });

  svr.set_error_handler([](const auto &req, auto &res) {
    auto fmt = "<!doctype html><html lang=en><p>Error Status: <span "
               "style='color:red;'>%d</span></p>";
    char buf[BUFSIZ];
    snprintf(buf, sizeof(buf), fmt, res.status);
    res.set_content(buf, "text/html");
  });

  app_log("Starting server on port 8008...");
  svr.listen("0.0.0.0", 8008);
}