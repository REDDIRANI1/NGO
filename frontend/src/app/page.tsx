import Link from "next/link";

import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <div className={styles.intro}>
          <h1>NGO monthly reporting</h1>
          <p>Submit monthly NGO impact reports or upload them in bulk via CSV.</p>
        </div>
        <div className={styles.ctas}>
          <Link className={styles.primary} href="/submit">
            Submit a report
          </Link>
          <Link className={styles.secondary} href="/bulk-upload">
            Bulk upload (CSV)
          </Link>
          <Link className={styles.secondary} href="/admin/dashboard">
            Admin dashboard
          </Link>
        </div>
      </main>
    </div>
  );
}
