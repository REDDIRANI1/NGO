import Link from "next/link";

import { SubmitForm } from "./SubmitForm";

export default function SubmitPage() {
  return (
    <div style={{ padding: 24, display: "grid", gap: 16 }}>
      <header style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h1 style={{ margin: 0 }}>Report submission</h1>
        <div style={{ marginLeft: "auto" }}>
          <Link href="/">Home</Link>
        </div>
      </header>

      <SubmitForm />
    </div>
  );
}

