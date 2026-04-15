# ============================== STAGE 1 - BUILD ============================= #

FROM gcc:13-bookworm AS builder

RUN apt-get update && apt-get install -y cmake

# Set working directory
WORKDIR /app

# Copy source code
COPY . .
RUN rm -r build/* || true

# Build
RUN cmake -S . -B build
RUN cmake --build build

# =============================== STAGE 2 - RUN ============================== #

FROM node:25-bookworm

ARG OBSIDIAN_EMAIL=""

# install dependencies ------------------------------------------------------- #

RUN npm install -g obsidian-headless
# RUN ob login --email

# setup executable ----------------------------------------------------------- #

# Set working directory
WORKDIR /app

# Copy only the built binary from builder stage
COPY --from=builder /app/build/main .

# (Optional) Make sure it's executable
RUN chmod +x main

# Run the binary
CMD ["./main"]