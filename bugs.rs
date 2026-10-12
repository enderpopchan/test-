use std::cell::RefCell;
use std::rc::Rc;
use std::sync::Mutex;

struct Node {
    next: Option<Rc<RefCell<Node>>>,
}

fn first(v: &Vec<i32>) -> i32 {
    v[0] // panics on empty
}

fn parse(s: &str) -> i32 {
    s.parse().unwrap() // panics on bad input
}

fn truncate(x: i64) -> i32 {
    x as i32 // silent truncation
}

fn add(a: u8, b: u8) -> u8 {
    a + b // overflow panics in debug, wraps in release
}

fn deref_raw() -> i32 {
    let p: *const i32 = std::ptr::null();
    unsafe { *p } // null pointer dereference
}

fn cycle() {
    let a = Rc::new(RefCell::new(Node { next: None }));
    let b = Rc::new(RefCell::new(Node { next: Some(a.clone()) }));
    a.borrow_mut().next = Some(b); // reference cycle, never freed
}

fn leak(s: String) {
    std::mem::forget(s); // leaks on purpose
}

fn ignore() {
    let _ = std::fs::remove_file("important.txt"); // error discarded
}

fn lock_twice(m: &Mutex<i32>) {
    let _a = m.lock().unwrap();
    let _b = m.lock().unwrap(); // deadlock
}

fn clone_in_loop(v: &Vec<String>) -> usize {
    let mut n = 0;
    for s in v {
        n += s.clone().len(); // needless allocation
    }
    n
}

fn transmute_it(x: u32) -> f32 {
    unsafe { std::mem::transmute::<u32, f32>(x) } // use f32::from_bits
}

fn slice(s: &str) -> &str {
    &s[0..3] // panics on a non-char boundary or short string
}

fn main() {
    let v = vec![];
    println!("{}", first(&v));
}
