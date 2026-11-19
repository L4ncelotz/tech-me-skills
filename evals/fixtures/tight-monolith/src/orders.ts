import { db } from "./billing";

export async function createOrder(input: { customerId: string; totalCents: number }) {
  // Directly writes to shared orders + billing_ledger tables in one coupled transaction.
  return db.query("INSERT INTO orders (customer_id, total_cents) VALUES ($1, $2)", [
    input.customerId,
    input.totalCents,
  ]);
}
