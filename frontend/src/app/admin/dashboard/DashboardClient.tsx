"use client";

import { useEffect, useMemo, useState } from "react";

import { getJson } from "@/lib/api";

type DashboardOut = {
  month: string;
  total_ngos_reporting: number;
  total_people_helped: number;
  total_events_conducted: number;
  total_funds_utilized: number;
};

function formatMoney(v: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
  }).format(v);
}

export function DashboardClient() {
  const defaultMonth = useMemo(() => {
    const d = new Date();
    const m = `${d.getMonth() + 1}`.padStart(2, "0");
    return `${d.getFullYear()}-${m}`;
  }, []);

  const [month, setMonth] = useState(defaultMonth);
  const [data, setData] = useState<DashboardOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const out = await getJson<DashboardOut>(`/dashboard?month=${month}`);
        if (!cancelled) setData(out);
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Failed to load");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    if (/^\d{4}-\d{2}$/.test(month)) load();
    return () => {
      cancelled = true;
    };
  }, [month]);

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <label style={{ display: "grid", gap: 6, maxWidth: 240 }}>
        Month
        <input type="month" value={month} onChange={(e) => setMonth(e.target.value)} />
      </label>

      {loading ? <div>Loading…</div> : null}
      {error ? <div style={{ color: "crimson" }}>{error}</div> : null}

      {data ? (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: 12,
          }}
        >
          <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
            <div style={{ opacity: 0.7 }}>Total NGOs reporting</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>{data.total_ngos_reporting}</div>
          </div>
          <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
            <div style={{ opacity: 0.7 }}>Total people helped</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>{data.total_people_helped}</div>
          </div>
          <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
            <div style={{ opacity: 0.7 }}>Total events conducted</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>{data.total_events_conducted}</div>
          </div>
          <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
            <div style={{ opacity: 0.7 }}>Total funds utilized</div>
            <div style={{ fontSize: 28, fontWeight: 700 }}>
              {formatMoney(data.total_funds_utilized)}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

