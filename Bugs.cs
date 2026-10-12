using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Threading.Tasks;

public class Bugs
{
    const string ConnString = "Server=localhost;Database=app;User Id=sa;Password=admin123;";
    static List<string> shared = new List<string>();      // shared mutable state

    public async void Save(string x)                       // async void: exceptions crash the process
    {
        await Task.Delay(10);
    }

    public string GetSync()
    {
        return GetAsync().Result;                          // sync-over-async deadlock
    }

    Task<string> GetAsync() => Task.FromResult("x");

    public int Count(string s)
    {
        return s.Length;                                   // NullReferenceException
    }

    public SqlDataReader Find(string name)
    {
        var conn = new SqlConnection(ConnString);          // never disposed
        conn.Open();
        var cmd = new SqlCommand("SELECT * FROM Users WHERE Name = '" + name + "'", conn);  // SQL injection
        return cmd.ExecuteReader();
    }

    public string Read(string path)
    {
        var sr = new StreamReader(path);                   // not in a using block
        return sr.ReadToEnd();
    }

    public void Remove(List<int> xs)
    {
        foreach (var x in xs)
            if (x < 0) xs.Remove(x);                       // modifies the collection while enumerating
    }

    public string Join(IEnumerable<string> parts)
    {
        var s = "";
        foreach (var p in parts) s += p;                   // quadratic string building
        return s;
    }

    public void Swallow()
    {
        try { Save("a"); }
        catch (Exception) { }                              // swallowed
    }

    public object Load(Stream s)
    {
        return new BinaryFormatter().Deserialize(s);       // unsafe deserialization
    }

    public int Token() => new Random().Next();             // not cryptographically secure

    public bool Expired(DateTime d) => d < DateTime.Now;   // local time instead of UTC

    public decimal Total(double a, double b) => (decimal)(a + b);   // double used for money

    readonly object gate = new object();
    public void Lock() { lock (this) { } }                 // locking on `this`
}
