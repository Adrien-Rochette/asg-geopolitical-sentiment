import express from "express";
import { analyzeSentiment } from "./services/sentiment.service";

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
    const { text } = req.body;

    if (!text) {
      return res.status(400).json({
        error: "text is required"
      });
    }

    const result = await analyzeSentiment(text);

    return res.json(result);
  } catch (error) {
    console.error(error);

    return res.status(500).json({
      error: "Failed to analyze sentiment"
    });
  }
});

const port = Number(process.env.PORT || 3000);

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});