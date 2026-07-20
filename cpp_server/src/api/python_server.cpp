#include "../config/json_config_handler.hpp"
#include "../utils/log.hpp"
#include <curl/curl.h>
#include <iostream>
#include <string>

size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
  ((std::string *)userp)->append((char *)contents, size * nmemb);
  return size * nmemb;
}

void python_server_get(std::string path, std::string *response) {
  CURL *curl = curl_easy_init();

  if (!curl) {
    return;
  }

  const JsonConfig config = get_config();
  std::string full_url = config.python_server_url + path;

  curl_easy_setopt(curl, CURLOPT_URL, full_url.c_str());
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, response);

  const CURLcode res = curl_easy_perform(curl);

  if (res == CURLE_OK) {
    app_log("Successful GET request to \"" + full_url + "\"");
  } else {
    app_log("Failed GET request to \"" + full_url + "\": " + curl_easy_strerror(res));
    std::cerr << curl_easy_strerror(res) << '\n';
  }

  curl_easy_cleanup(curl);
}