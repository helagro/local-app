#include "../utils/log.hpp"
#include "httplib.h"

using namespace httplib;

void start_server() {
  Server svr;

  svr.Get("/health", [](const httplib::Request &, httplib::Response &res) {
    res.set_content("ok", "text/plain");
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