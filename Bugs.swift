import Foundation

class Owner {
    var child: Child?
    deinit { print("owner gone") }
}

class Child {
    var owner: Owner?                          // strong back-reference: retain cycle, never freed
}

func link() {
    let o = Owner(), c = Child()
    o.child = c
    c.owner = o
}

func name(_ user: [String: String]) -> String {
    return user["name"]!                       // crashes when missing
}

func load(_ path: String) -> Data {
    return try! Data(contentsOf: URL(fileURLWithPath: path))   // crashes on any error
}

func cast(_ x: Any) -> String {
    return x as! String                        // crashes on other types
}

func download() {
    let data = try? Data(contentsOf: URL(string: "http://example.com/a")!)   // blocks the main thread, plain HTTP, force unwrap
    print(data?.count ?? 0)
}

func handler(_ cb: @escaping () -> Void) {
    DispatchQueue.main.async { [self] in cb() }
}

let password = "admin123"                      // hardcoded credential
UserDefaults.standard.set(password, forKey: "pw")   // secret stored in plain-text defaults

func index(_ a: [Int]) -> Int {
    return a[a.count]                          // out of range
}
