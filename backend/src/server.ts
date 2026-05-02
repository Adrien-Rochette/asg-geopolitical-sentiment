import express from "express";

const app = express();

app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    service: "asg-backend"
  });
});

const port = Number(process.env.PORT || 3000);

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});