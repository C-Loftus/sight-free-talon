#!/bin/bash

# Define the Go source file
GO_SOURCE="log_parser.go"

# Define the output directory
OUTPUT_DIR="bin"

# Cross-compile for Windows
GOOS=windows GOARCH=amd64 go build -o "${OUTPUT_DIR}/log_parser_windows_amd64.exe" "${GO_SOURCE}"
GOOS=windows GOARCH=386 go build -o "${OUTPUT_DIR}/log_parser_windows_386.exe" "${GO_SOURCE}"

# Cross-compile for Linux
GOOS=linux GOARCH=amd64 go build -o "${OUTPUT_DIR}/log_parser_linux_amd64" "${GO_SOURCE}"
GOOS=linux GOARCH=386 go build -o "${OUTPUT_DIR}/log_parser_linux_386" "${GO_SOURCE}"

# Cross-compile for macOS
GOOS=darwin GOARCH=amd64 go build -o "${OUTPUT_DIR}/log_parser_macos_amd64" "${GO_SOURCE}"

echo "Compilation completed. Binaries are in the '${OUTPUT_DIR}' directory."
