"use client";

import { useState } from "react";

export default function HomePage() {
  const [status, setStatus] = useState<string | null>(null);

  async function checkHealth() {
    try {
      const res = await fetch("http://127.0.0.1:8000/health");
      const data = await res.json();
      setStatus(data.status);
    } catch (err) {
      setStatus("error");
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <h1 className="text-3xl font-bold mb-6">MedExplain Frontend</h1>
      <button
        onClick={checkHealth}
        className="px-6 py-3 rounded-lg bg-blue-600 text-white hover:bg-blue-700 shadow-md"
      >
        Check Backend Health
      </button>
      {status && (
        <p className="mt-4 text-lg">
          Backend status:{" "}
          <span
            className={
              status === "ok"
                ? "text-green-600 font-semibold"
                : "text-red-600 font-semibold"
            }
          >
            {status}
          </span>
        </p>
      )}
    </main>
  );
}
