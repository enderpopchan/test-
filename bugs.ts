// Typed API client helpers
interface User {
  id: number;
  name: string;
  email?: string;
}

// @ts-ignore
import legacy from "legacy-lib";

export function getEmailDomain(user: User): string {
  return user.email!.split("@")[1]; // non-null assertion on optional
}

export function parseUser(raw: string): User {
  return JSON.parse(raw) as User; // unchecked cast, no validation
}

export function toNumber(x: any): number {
  return x as number; // `any` hides type errors
}

export async function save(user: User) {
  fetch("/api/users", { method: "POST", body: JSON.stringify(user) }); // floating promise
}

export function first<T>(items: T[]): T {
  return items[0]; // undefined when empty, but typed as T
}

export function handleError(e: unknown) {
  console.log((e as Error).message); // e may not be an Error
}

export const enum Status { Active, Inactive }

export function isActive(s: Status): boolean {
  return s == 0 || s == 1; // magic numbers instead of enum members
}

export function swap(a: string, b: number): [number, string] {
  return [a as unknown as number, b as unknown as string]; // double cast hides a real bug
}

export function total(items: { price: number }[]): number {
  let sum = 0;
  items.forEach(i => (sum += i.price)); // floating-point money
  return sum;
}
