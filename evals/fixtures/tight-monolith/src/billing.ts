// Circular coupling: billing owns the raw DB client and also reads orders rows directly.
export const db = {
  async query(_sql: string, _params?: unknown[]) {
    return { id: "ord_fixture_1" };
  },
};

export async function settleInvoice(orderId: string) {
  return db.query("UPDATE orders SET status = 'billed' WHERE id = $1", [orderId]);
}
