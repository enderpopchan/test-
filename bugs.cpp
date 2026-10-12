#include <iostream>
#include <map>
#include <string>
#include <thread>
#include <vector>

struct Base {
    ~Base() {}                       // not virtual, deleting a Derived through Base* leaks
    virtual void run() {}
};

struct Derived : Base {
    int *data = new int[100];        // raw owning pointer, no copy constructor
    ~Derived() { delete data; }      // delete vs delete[]
    void run() override {}
};

struct Config {
    int port;                        // never initialized
    bool debug;
};

const std::string &name() {
    std::string s = "temp";
    return s;                        // dangling reference
}

void invalidate(std::vector<int> &v) {
    for (auto it = v.begin(); it != v.end(); ++it) {
        if (*it == 0) v.erase(it);   // invalidates the iterator
    }
}

void slicing(Base b) { b.run(); }    // object sliced when passed by value

void catch_by_value() {
    try {
        throw std::runtime_error("x");
    } catch (std::exception e) {     // slices the exception
    }
}

int counter = 0;
void race() {
    std::thread t1([] { for (int i = 0; i < 1000; i++) counter++; });
    std::thread t2([] { for (int i = 0; i < 1000; i++) counter++; });
    t1.detach();                     // detached, no join, data race
    t2.detach();
}

struct Resource {
    ~Resource() { throw std::runtime_error("in dtor"); }   // terminates
};

int overflow(int x) {
    return x + 1;                    // signed overflow is undefined behavior
}

void moved() {
    std::string a = "hello";
    std::string b = std::move(a);
    std::cout << a.size();           // use after move
}

int lookup(std::map<std::string, int> &m) {
    return m["missing"];             // inserts a default entry as a side effect
}

int main() {
    Base *b = new Derived();
    delete b;
    Config c;
    std::cout << c.port << std::endl;
}
