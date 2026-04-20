import Link from "next/link";

import { BulkUploadClient } from "./BulkUploadClient";

export default function BulkUploadPage() {
  return (
    <div style={{ padding: 24, display: "grid", gap: 16 }}>
      <header style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h1 style={{ margin: 0 }}>Bulk report upload</h1>
        <div style={{ marginLeft: "auto" }}>
          <Link href="/">Home</Link>
        </div>
      </header>

      <p style={{ margin: 0, opacity: 0.8 }}>
        CSV header: <code>ngo_id,month,people_helped,events_conducted,funds_utilized</code>
      </p>

      <BulkUploadClient />
    </div>
  );
}

