import Link from "next/link";

import { DashboardClient } from "./DashboardClient";

export default function DashboardPage() {
  return (
    <div style={{ padding: 24, display: "grid", gap: 16 }}>
      <header style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h1 style={{ margin: 0 }}>Admin dashboard</h1>
        <div style={{ marginLeft: "auto" }}>
          <Link href="/">Home</Link>
        </div>
      </header>

      <DashboardClient />
    </div>
  );
}

