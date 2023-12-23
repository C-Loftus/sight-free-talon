package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"path/filepath"
    "runtime"
	"encoding/json"
)

type LogLines struct {
    LastIOLine      string `json:"last_io_line"`
    LastDebugLine   string `json:"last_debug_line"`
    LastWarningLine string `json:"last_warning_line"`
    FirstErrorLine  string `json:"first_error_line"`
    LastErrorLine   string `json:"last_error_line"`
}


func main() {
	// Open the log file
    var path string
    if runtime.GOOS == "windows" {
        path = filepath.Join(os.Getenv("APPDATA"), "Talon", "talon.log")
    } else {
        path = filepath.Join(os.Getenv("HOME"), ".talon", "talon.log")
    }

    file, err := os.Open(path)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

	// Create regular expressions for each log category
	ioRegex := regexp.MustCompile(`.*\s+IO\s+(.*)`)
	debugRegex := regexp.MustCompile(`.*\s+DEBUG\s+(.*)`)
	warningRegex := regexp.MustCompile(`.*\s+WARNING\s+(.*)`)
	errorRegex := regexp.MustCompile(`.*\s+ERROR\s+(.*)`)

	// Initialize variables to store the last lines for each category
	var lastIOLine, lastDebugLine, lastWarningLine, firstErrorLine, lastErrorLine string

	// Read the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		// Check the category of the log line
		if ioRegex.MatchString(line) {
			// Extract the content after "IO"
			match := ioRegex.FindStringSubmatch(line)
			if len(match) > 1 {
				lastIOLine = match[1]
			}
		} else if debugRegex.MatchString(line) {
			// Extract the content after "DEBUG"
			match := debugRegex.FindStringSubmatch(line)
			if len(match) > 1 {
				lastDebugLine = match[1]
			}
		} else if warningRegex.MatchString(line) {
			// Extract the content after "WARNING"
			match := warningRegex.FindStringSubmatch(line)
			if len(match) > 1 {
				lastWarningLine = match[1]
			}
		} else if errorRegex.MatchString(line) {
			// Extract the first and last line of the ERROR block
			firstErrorLine = line
			lastErrorLine = line

			// Read the lines until another log type is encountered
			for scanner.Scan() {
				nextLine := scanner.Text()
				if ioRegex.MatchString(nextLine) || debugRegex.MatchString(nextLine) || warningRegex.MatchString(nextLine) || errorRegex.MatchString(nextLine) {
					// Found a line matching another category, stop capturing the ERROR block
					break
				}
				lastErrorLine = nextLine
			}
		}
	}

    lines := LogLines{
        LastIOLine:      lastIOLine,
        LastDebugLine:   lastDebugLine,
        LastWarningLine: lastWarningLine,
        FirstErrorLine:  firstErrorLine,
        LastErrorLine:   lastErrorLine,
    }

    jsonData, err := json.Marshal(lines)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Println(string(jsonData))
}
