# ============================== STAGE 1 - BUILD ============================= #

FROM gcc:13 AS builder

RUN apt-get update && apt-get install -y cmake

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# build ---------------------------------------------------------------------- #

RUN cmake . 
RUN make

# =============================== STAGE 2 - RUN ============================== #

FROM debian:bookworm-slim

# Set working directory
WORKDIR /app

# Copy only the built binary from builder stage
COPY --from=builder /app/main .

# (Optional) Make sure it's executable
RUN chmod +x main

# Run the binary
CMD ["./main"]