const { sum, parse, sortIds } = require("./bugs");

describe("helpers", () => {
  test("sum", () => {
    expect(sum([1, 2, 3])).toBeDefined();          // weak assertion, hides the NaN
  });

  test("parse", () => {
    parse("10");                                   // no assertion
  });

  test.skip("sortIds", () => {                     // skipped, hides the lexicographic sort
    expect(sortIds([10, 9, 1])).toEqual([1, 9, 10]);
  });

  test("timing", async () => {
    await new Promise(r => setTimeout(r, 3000));   // slow, sleeps instead of mocking time
    expect(Math.random()).toBeLessThan(2);         // always true
  });

  it("flaky", () => {
    expect(Date.now() % 2).toBe(0);                // depends on the clock
  });
});
