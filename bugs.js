// Dashboard helpers
const express = require("express");
const crypto = require("crypto");
const { exec } = require("child_process");

const app = express();
const JWT_SECRET = "secret";
const cache = {};

function sum(arr) {
  let total = 0;
  for (let i = 0; i <= arr.length; i++) total += arr[i]; // off-by-one, NaN
  return total;
}

function parse(s) {
  return parseInt(s); // no radix, no NaN check
}

function isDone(a, b) {
  return a == b || a == null; // loose equality
}

function sortIds(ids) {
  return ids.sort(); // lexicographic: [10, 9, 1] -> [1, 10, 9]
}

function makeHandlers() {
  var handlers = [];
  for (var i = 0; i < 3; i++) {
    handlers.push(function () { return i; }); // always returns 3
  }
  return handlers;
}

async function loadUser(id) {
  const res = fetch("/api/users/" + id); // missing await
  return res.json();
}

async function loadAll(ids) {
  ids.forEach(async (id) => { await loadUser(id); }); // not awaited, errors lost
}

function merge(target, src) {
  for (const k in src) {
    if (typeof src[k] === "object") merge(target[k] = target[k] || {}, src[k]); // prototype pollution
    else target[k] = src[k];
  }
  return target;
}

function render(el, name) {
  el.innerHTML = "<b>" + name + "</b>"; // XSS
}

function validEmail(s) {
  return /^([a-zA-Z0-9]+)+@example\.com$/.test(s); // catastrophic backtracking
}

function token() {
  return Math.random().toString(36).slice(2); // predictable
}

function readConfig(text) {
  return JSON.parse(text); // throws on bad input, unguarded
}

class Counter {
  constructor() { this.n = 0; }
  inc() { this.n++; }
}
const c = new Counter();
setTimeout(c.inc, 10); // `this` lost

function removeItem(arr, i) {
  delete arr[i]; // leaves a hole, length unchanged
  return arr;
}

function isNumber(x) {
  return typeof x === "number" || x === NaN; // NaN never equals itself
}

app.get("/run", (req, res) => {
  exec("ls " + req.query.dir, (err, out) => res.send(out)); // command injection, XSS
});

app.get("/session", (req, res) => {
  res.cookie("sid", token()); // no httpOnly/secure/sameSite
  res.send(eval(req.query.code)); // code execution
});

app.get("/item/:id", (req, res) => {
  if (!cache[req.params.id]) cache[req.params.id] = Date.now(); // unbounded cache
  res.json(cache);
});

process.on("unhandledRejection", () => {}); // hides every rejected promise
app.listen(3000, "0.0.0.0");
