package main

import (
    "io"
    "log"
    "net/http"
)

func main() {
    h := func(w http.ResponseWriter, _ *http.Request) {
        io.WriteString(w, "Hello from a HandleFunc!\n")
    }

    http.HandleFunc("/", h)
    log.Println("Listening on http://localhost:8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
