import express from "express";
import { analyzeSentiment } from "./services/sentiment.service";
import { pool } from "./db";

const app = express();

app.use(express.json());

app.get("/health", (_req, res) => {
  res.json({
    status: "ok",
    service: "asg-backend"
  });
});

app.post("/analyze", async (req, res) => {
  try {
    const { text, source, region } = req.body;

    if (!text) {
      return res.status(400).json({
        error: "text is required"
      });
    }

    const prediction = await analyzeSentiment(text);

    const result = await pool.query(
      `
      INSERT INTO headlines
      (title, sentiment, confidence, source, region)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
      `,
      [
        text,
        prediction.sentiment,
        prediction.confidence,
        source || null,
        region || null
      ]
    );

    return res.status(201).json(result.rows[0]);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      error: "Failed to analyze and save sentiment"
    });
  }
});

app.get("/headlines", async (_req, res) => {
  try {
    const result = await pool.query(
      `
      SELECT *
      FROM headlines
      ORDER BY created_at DESC
      LIMIT 100
      `
    );

    return res.json(result.rows);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      error: "Failed to fetch headlines"
    });
  }
});

const port = Number(process.env.PORT || 3000);

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});