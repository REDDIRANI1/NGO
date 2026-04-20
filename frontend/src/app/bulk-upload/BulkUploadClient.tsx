"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import { getJson, postFile } from "@/lib/api";

type UploadResponse = { job_id: string };

type JobItemFailure = { row_number: number; error: string };

type JobStatusOut = {
  job_id: string;
  status: string;
  total_rows: number;
  processed_rows: number;
  succeeded_rows: number;
  failed_rows: number;
  failures: JobItemFailure[];
};

const DONE_STATUSES = new Set(["completed", "completed_with_errors", "failed"]);

export function BulkUploadClient() {
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<JobStatusOut | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const pollingRef = useRef<number | null>(null);

  const progressLabel = useMemo(() => {
    if (!status) return null;
    if (status.total_rows > 0) {
      return `Processed ${status.processed_rows} of ${status.total_rows} rows`;
    }
    return `Processed ${status.processed_rows} rows`;
  }, [status]);

  async function startUpload() {
    if (!file) return;
    setError(null);
    setStatus(null);
    setJobId(null);
    setUploading(true);
    try {
      const res = await postFile<UploadResponse>("/reports/upload", "file", file);
      setJobId(res.job_id);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  useEffect(() => {
    async function tick(id: string) {
      try {
        const s = await getJson<JobStatusOut>(`/job-status/${id}`);
        setStatus(s);
        if (DONE_STATUSES.has(s.status)) {
          if (pollingRef.current) window.clearInterval(pollingRef.current);
          pollingRef.current = null;
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : "Polling failed");
      }
    }

    if (!jobId) return;
    tick(jobId);
    pollingRef.current = window.setInterval(() => tick(jobId), 2000);
    return () => {
      if (pollingRef.current) window.clearInterval(pollingRef.current);
      pollingRef.current = null;
    };
  }, [jobId]);

  return (
    <div style={{ display: "grid", gap: 12, maxWidth: 720 }}>
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontWeight: 600 }}>Upload CSV</div>
        <input
          type="file"
          accept=".csv,text/csv"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button disabled={!file || uploading} onClick={startUpload}>
          {uploading ? "Uploading…" : "Start processing"}
        </button>
      </div>

      {error ? <div style={{ color: "crimson" }}>{error}</div> : null}
      {jobId ? (
        <div style={{ display: "grid", gap: 6 }}>
          <div>
            <span style={{ opacity: 0.7 }}>Job ID:</span> <code>{jobId}</code>
          </div>
        </div>
      ) : null}

      {status ? (
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            <div>
              <span style={{ opacity: 0.7 }}>Status:</span> {status.status}
            </div>
            <div>
              <span style={{ opacity: 0.7 }}>Succeeded:</span> {status.succeeded_rows}
            </div>
            <div>
              <span style={{ opacity: 0.7 }}>Failed:</span> {status.failed_rows}
            </div>
          </div>

          {progressLabel ? <div>{progressLabel}</div> : null}

          {status.failures?.length ? (
            <div style={{ display: "grid", gap: 6 }}>
              <div style={{ fontWeight: 600 }}>Failed rows (sample)</div>
              <ul style={{ margin: 0, paddingLeft: 18 }}>
                {status.failures.map((f) => (
                  <li key={`${f.row_number}-${f.error}`}>
                    Row {f.row_number}: {f.error}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

