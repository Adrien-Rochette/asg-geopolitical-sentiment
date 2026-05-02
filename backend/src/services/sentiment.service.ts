import axios from "axios";

export type SentimentResult = {
  text: string;
  sentiment: "negative" | "neutral" | "positive";
  confidence: number;
};

export async function analyzeSentiment(text: string): Promise<SentimentResult> {
  const aiServiceUrl = process.env.AI_SERVICE_URL || "http://127.0.0.1:8000";

  const response = await axios.post(`${aiServiceUrl}/predict`, {
    text
  });

  return response.data;
}