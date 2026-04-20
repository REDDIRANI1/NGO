export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function postJson<TResponse>(
  path: string,
  body: unknown,
): Promise<TResponse> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const data: unknown = await res.json();
      const maybeObj = typeof data === "object" && data !== null ? (data as Record<string, unknown>) : null;
      const maybeDetail = maybeObj?.detail;

      detail =
        typeof maybeDetail === "string"
          ? maybeDetail
          : Array.isArray(maybeDetail)
            ? maybeDetail
                .map((d) =>
                  typeof d === "object" && d !== null ? (d as Record<string, unknown>).msg : null,
                )
                .filter((m): m is string => typeof m === "string")
                .join(", ")
            : detail;
    } catch {
      // ignore parse errors
    }
    throw new Error(detail);
  }

  return (await res.json()) as TResponse;
}

export async function getJson<TResponse>(path: string): Promise<TResponse> {
  const res = await fetch(`${API_BASE_URL}${path}`, { method: "GET" });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return (await res.json()) as TResponse;
}

export async function postFile<TResponse>(
  path: string,
  fileFieldName: string,
  file: File,
): Promise<TResponse> {
  const form = new FormData();
  form.append(fileFieldName, file);
  const res = await fetch(`${API_BASE_URL}${path}`, { method: "POST", body: form });
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return (await res.json()) as TResponse;
}

