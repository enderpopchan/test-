package main

import (
	"crypto/md5"
	"database/sql"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"os"
	"sync"
	"time"
)

var counter int
var users map[string]int // nil map

func inc() {
	counter++ // data race
}

func writeUser(name string) {
	users[name] = 1 // panic: assignment to nil map
}

func readAll(path string) []byte {
	f, _ := os.Open(path) // ignored error, never closed
	data, _ := ioutil.ReadAll(f)
	return data
}

func fetch(url string) string {
	resp, err := http.Get(url) // no timeout
	if err != nil {
		fmt.Println(err)
	}
	body, _ := ioutil.ReadAll(resp.Body) // nil deref if err != nil, body never closed
	return string(body)
}

func loopCapture() {
	for i := 0; i < 3; i++ {
		go func() { fmt.Println(i) }() // captures loop variable, no WaitGroup
	}
}

func deferInLoop(paths []string) {
	for _, p := range paths {
		f, _ := os.Open(p)
		defer f.Close() // all closes run at function exit
	}
}

func deadlock() {
	ch := make(chan int)
	ch <- 1 // unbuffered, no receiver
	fmt.Println(<-ch)
}

func leak() {
	ch := make(chan int)
	go func() { ch <- 1 }() // goroutine blocks forever if nobody reads
}

func query(db *sql.DB, name string) {
	db.Query("SELECT * FROM users WHERE name = '" + name + "'") // SQL injection, result ignored
}

func hash(p string) []byte {
	h := md5.Sum([]byte(p)) // weak hash
	return h[:]
}

func token() int {
	return rand.Int() // math/rand is predictable and unseeded
}

func shadow() error {
	err := fmt.Errorf("first")
	if true {
		_, err := os.Open("x") // shadows err, outer error lost
		_ = err
	}
	return err
}

func assert(v interface{}) string {
	return v.(string) // panics on other types
}

func copyLock(m sync.Mutex) { // copies the lock
	m.Lock()
}

func sliceAlias() {
	a := []int{1, 2, 3, 4}
	b := a[:2]
	b = append(b, 99) // overwrites a[2]
	fmt.Println(a, b)
}

func timeout() {
	for {
		select {
		case <-time.After(time.Second): // new timer every iteration
		}
	}
}

func main() {
	http.ListenAndServe(":8080", nil) // error ignored
}
