#include "python_server.hpp"
#include "utils/log.hpp"
#include <cstdint>
#include <cstring>
#include <filesystem>
#include <iostream>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

int sock = -1;
bool is_open = false;

namespace {
bool open_socket() {
  sock = socket(AF_UNIX, SOCK_STREAM, 0);
  if (sock == -1) {
    perror("socket");
    app_log("Failed to create socket");

    return false;
  }

  std::filesystem::create_directories("/tmp/local_app");

  sockaddr_un addr{};
  addr.sun_family = AF_UNIX;
  std::strcpy(addr.sun_path, "/tmp/local_app/local_app.sock");

  if (connect(sock, (sockaddr *)&addr, sizeof(addr)) == -1) {
    perror("connect");
    app_log("Failed to connect to socket");

    close(sock);
    return false;
  }

  is_open = true;
  return true;
}
} // namespace

bool python_server_socket(std::string message) {
  if (!is_open && !open_socket()) {
    app_log("Failed to open socket");
    return false;
  }

  const uint32_t message_length = message.length();
  ssize_t bytes_sent = send(sock, &message_length, sizeof(message_length), 0);
  if (bytes_sent == -1) {
    app_log("Failed to send socket message length");
    return false;
  }

  bytes_sent = send(sock, message.c_str(), message.length(), 0);
  if (bytes_sent == -1) {
    app_log("Failed to send socket message");
    return false;
  }

  app_log("Socket message sent: " + message + " (length: " + std::to_string(message_length) + ")");
  return true;
}
