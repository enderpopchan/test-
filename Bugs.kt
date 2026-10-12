import java.io.File

class Session {
    lateinit var token: String                 // crashes if read before assignment
    var user: String? = null
}

fun length(s: String?): Int {
    return s!!.length                          // NullPointerException
}

fun firstLine(path: String): String {
    val r = File(path).bufferedReader()        // never closed
    return r.readLine()                        // may be null at runtime
}

fun parse(s: String): Int {
    return s.toInt()                           // NumberFormatException
}

fun cast(x: Any): String {
    return x as String                         // ClassCastException
}

fun query(name: String): String {
    return "SELECT * FROM users WHERE name = '$name'"   // SQL injection
}

fun remove(xs: MutableList<Int>) {
    for (x in xs) if (x < 0) xs.remove(x)      // ConcurrentModificationException
}

fun risky() {
    try {
        parse("x")
    } catch (e: Exception) {                   // swallowed
    }
}

fun launch() {
    GlobalScope.launch { delay(1000) }         // unstructured coroutine, leaks past its owner
}

fun main() {
    println(Session().token)
}
