"use client";

import { useMemo, useState } from "react";

import { postJson } from "@/lib/api";

type ReportIn = {
  ngo_id: string;
  month: string; // YYYY-MM
  people_helped: number;
  events_conducted: number;
  funds_utilized: number;
};

export function SubmitForm() {
  const [ngoId, setNgoId] = useState("");
  const [month, setMonth] = useState("");
  const [peopleHelped, setPeopleHelped] = useState<string>("");
  const [eventsConducted, setEventsConducted] = useState<string>("");
  const [fundsUtilized, setFundsUtilized] = useState<string>("");

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const canSubmit = useMemo(() => {
    if (!ngoId.trim()) return false;
    if (!/^\d{4}-\d{2}$/.test(month)) return false;
    if (peopleHelped === "" || Number.isNaN(Number(peopleHelped))) return false;
    if (eventsConducted === "" || Number.isNaN(Number(eventsConducted))) return false;
    if (fundsUtilized === "" || Number.isNaN(Number(fundsUtilized))) return false;
    if (Number(peopleHelped) < 0) return false;
    if (Number(eventsConducted) < 0) return false;
    if (Number(fundsUtilized) < 0) return false;
    return true;
  }, [ngoId, month, peopleHelped, eventsConducted, fundsUtilized]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    const payload: ReportIn = {
      ngo_id: ngoId.trim(),
      month,
      people_helped: Number(peopleHelped),
      events_conducted: Number(eventsConducted),
      funds_utilized: Number(fundsUtilized),
    };

    setSubmitting(true);
    try {
      await postJson("/report", payload);
      setSuccess("Report submitted successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={onSubmit}
      style={{
        display: "grid",
        gap: 12,
        maxWidth: 520,
      }}
    >
      <label style={{ display: "grid", gap: 6 }}>
        NGO ID
        <input
          value={ngoId}
          onChange={(e) => setNgoId(e.target.value)}
          placeholder="e.g. NGO-123"
          required
        />
      </label>

      <label style={{ display: "grid", gap: 6 }}>
        Month
        <input
          value={month}
          onChange={(e) => setMonth(e.target.value)}
          type="month"
          required
        />
      </label>

      <label style={{ display: "grid", gap: 6 }}>
        People Helped
        <input
          value={peopleHelped}
          onChange={(e) => setPeopleHelped(e.target.value)}
          type="number"
          min={0}
          required
        />
      </label>

      <label style={{ display: "grid", gap: 6 }}>
        Events Conducted
        <input
          value={eventsConducted}
          onChange={(e) => setEventsConducted(e.target.value)}
          type="number"
          min={0}
          required
        />
      </label>

      <label style={{ display: "grid", gap: 6 }}>
        Funds Utilized
        <input
          value={fundsUtilized}
          onChange={(e) => setFundsUtilized(e.target.value)}
          type="number"
          min={0}
          step="0.01"
          required
        />
      </label>

      <button disabled={!canSubmit || submitting} type="submit">
        {submitting ? "Submitting..." : "Submit report"}
      </button>

      {error ? (
        <div style={{ color: "crimson" }}>{error}</div>
      ) : success ? (
        <div style={{ color: "green" }}>{success}</div>
      ) : null}
    </form>
  );
}

