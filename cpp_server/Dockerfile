# -------- Stage 1: Build --------
FROM gcc:13 AS builder

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Build the project
RUN make

# -------- Stage 2: Runtime --------
FROM debian:bookworm-slim

# Set working directory
WORKDIR /app

# Copy only the built binary from builder stage
COPY --from=builder /app/my_app .

# (Optional) Make sure it's executable
RUN chmod +x my_app

# Run the binary
CMD ["./my_app"]