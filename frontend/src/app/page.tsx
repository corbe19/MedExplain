"use client";
import { useState } from "react";

type Pred = { label: string; score: number };

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [preds, setPreds] = useState<Pred[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  async function analyze() {
    if (!file) return;
    setLoading(true);
    setErr(null);
    setPreds(null);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/analyze/image", {
        method: "POST",
        body: fd,
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setPreds(data.result);
    } catch (e: any) {
      setErr(e.message ?? "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-3xl font-bold mb-4">MedExplain</h1>

      <div className="space-y-4">
        <input
          type="file"
          accept="image/png,image/jpeg"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          className="block w-full"
        />
        <button
          onClick={analyze}
          disabled={!file || loading}
          className="px-4 py-2 rounded-lg bg-blue-600 text-white disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze Image"}
        </button>

        {err && <p className="text-red-600">{err}</p>}

        {preds && (
          <div className="mt-4 rounded-lg border p-4">
            <h2 className="font-semibold mb-2">Predictions</h2>
            <ul className="space-y-1">
              {preds.map((p, i) => (
                <li key={i} className="flex items-center justify-between">
                  <span>{p.label}</span>
                  <span className="tabular-nums">
                    {(p.score * 100).toFixed(1)}%
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </main>
  );
}
