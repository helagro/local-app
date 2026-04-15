#include "../utils/log.hpp"
#include "httplib.h"

using namespace httplib;

void start_server() {
  Server svr;

  svr.Get("/health", [](const httplib::Request &, httplib::Response &res) {
    res.set_content("ok", "text/plain");
  });

  app_log("Starting server on port 8008...");
  svr.listen("0.0.0.0", 8008);
}