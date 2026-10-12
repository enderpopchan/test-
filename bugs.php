<?php
// Account pages
error_reporting(E_ALL);
ini_set("display_errors", 1);                              // leaks internals

$db = new mysqli("localhost", "root", "admin123", "app");  // hardcoded credentials

$id = $_GET["id"];
$res = $db->query("SELECT * FROM users WHERE id = $id");   // SQL injection
$row = $res->fetch_assoc();

echo "Hello " . $_GET["name"];                             // reflected XSS
echo "<a href='" . $_SERVER["REQUEST_URI"] . "'>self</a>"; // XSS via URI

include($_GET["page"] . ".php");                           // local/remote file inclusion

eval($_POST["code"]);                                      // code execution

$obj = unserialize($_COOKIE["data"]);                      // object injection

extract($_POST);                                           // overwrites any variable ($is_admin, ...)

if ($_POST["token"] == "0e12345") {                        // loose comparison: "0e..." hash collisions
    grant_access();
}

if (md5($_POST["password"]) == $row["hash"]) {             // md5 plus loose comparison
    $_SESSION["user"] = $row["id"];                        // no session_regenerate_id
}

if (in_array($_GET["role"], ["admin", 0])) {               // loose in_array
    echo "welcome";
}

shell_exec("ping -c 1 " . $_GET["host"]);                  // command injection

move_uploaded_file($_FILES["f"]["tmp_name"], "uploads/" . $_FILES["f"]["name"]);  // no validation, path traversal

mail($_POST["to"], "Hi", "Body", "From: " . $_POST["from"]);   // header injection

$cfg = @file_get_contents("config.json");                  // error suppression
setcookie("auth", $row["id"]);                             // no httponly/secure flags
header("Location: " . $_GET["next"]);                      // open redirect
