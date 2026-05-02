import express from "express";
import { analyzeSentiment } from "./services/sentiment.service";
import { pool } from "./db";
import path from "path";

const app = express();
const port = Number(process.env.PORT || 3000);

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});

app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));


app.get("/dashboard", (_req, res) => {
  res.sendFile(path.join(__dirname, "../public/dashboard.html"));
});

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

app.get("/stats", async (_req, res) => {
  try {
    const result = await pool.query(
      `
      SELECT
        COALESCE(region, 'Unknown') AS region,

        COUNT(*) AS total_headlines,

        SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_count,
        SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) AS neutral_count,
        SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_count,

        AVG(
          CASE
            WHEN sentiment = 'positive' THEN 1
            WHEN sentiment = 'neutral' THEN 0
            WHEN sentiment = 'negative' THEN -1
          END
        ) AS mood_score,

        AVG(confidence) AS average_confidence

      FROM headlines
      GROUP BY COALESCE(region, 'Unknown')
      ORDER BY region ASC
      `
    );

    return res.json(result.rows);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      error: "Failed to fetch statistics"
    });
  }
});

app.get("/dashboard-data", async (_req, res) => {
  try {
    const statsResult = await pool.query(
      `
      SELECT
        COALESCE(region, 'Unknown') AS region,
        COUNT(*) AS total_headlines,
        SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) AS positive_count,
        SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) AS neutral_count,
        SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) AS negative_count,
        AVG(
          CASE
            WHEN sentiment = 'positive' THEN 1
            WHEN sentiment = 'neutral' THEN 0
            WHEN sentiment = 'negative' THEN -1
          END
        ) AS mood_score,
        AVG(confidence) AS average_confidence
      FROM headlines
      GROUP BY COALESCE(region, 'Unknown')
      ORDER BY region ASC
      `
    );

    const headlinesResult = await pool.query(
      `
      SELECT
        id,
        title,
        sentiment,
        confidence,
        source,
        region,
        created_at
      FROM headlines
      ORDER BY created_at DESC
      LIMIT 10
      `
    );

    return res.json({
      regions: statsResult.rows,
      latest_headlines: headlinesResult.rows
    });
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      error: "Failed to fetch dashboard data"
    });
  }
}

);