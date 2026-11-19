import express from "express";
import { createOrder } from "./orders";
import { settleInvoice } from "./billing";

const app = express();
app.use(express.json());

app.post("/orders", async (req, res) => {
  const order = await createOrder(req.body);
  const invoice = await settleInvoice(order.id);
  res.json({ order, invoice });
});

app.listen(3000);
