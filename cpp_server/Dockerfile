# ============================== STAGE 1 - BUILD ============================= #

FROM gcc:16-trixie AS builder

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

FROM node:26-trixie
ENV TZ=Europe/Stockholm

# install dependencies ------------------------------------------------------- #

RUN npm install -g obsidian-headless

# setup executable ----------------------------------------------------------- #

# Set working directory
WORKDIR /app

# Copy only the built binary from builder stage
COPY --from=builder /app/build/main .
COPY --from=builder /app/scripts/ ./scripts

# (Optional) Make sure it's executable
RUN chmod +x main

# Run the binary
CMD ["./scripts/start.sh"]