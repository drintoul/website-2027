const express = require("express");
const cors = require("cors");
const multer = require("multer");

const app = express();
const PORT = process.env.PORT || 4000;

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 10 * 1024 * 1024 } });

app.use(cors());
app.use(express.json());

// Health check — used by the compose healthcheck and by cloudflared/uptime checks
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", service: "voyages-by-dave-backend" });
});

// Lead intake form submission
app.post("/api/plan", upload.single("document"), (req, res) => {
  const body = req.body || {};
  const file = req.file;

  const entry = {
    received: new Date().toISOString(),
    name: body.name,
    email: body.email,
    phone: body.phone,
    destination: body.destination,
    dates: body.dates,
    flexibility: body.flexibility,
    origin: body.origin,
    travellers: body.travellers,
    composition: body.composition,
    trip_type: body.trip_type,
    hardest: body.hardest,
    canada_only: body.canada_only,
    accessibility: body.accessibility,
    stage: body.stage,
    document: file ? { name: file.originalname, size: file.size, type: file.mimetype } : null,
  };

  // Log intake for now; replace with email/CRM notification when ready
  console.log("[lead intake]", JSON.stringify(entry, null, 2));

  res.json({ status: "ok", message: "Trip request received" });
});

app.listen(PORT, () => {
  console.log(`Voyages By Dave backend listening on port ${PORT}`);
});
