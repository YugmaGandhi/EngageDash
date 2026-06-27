export default function Home() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "0.75rem",
        fontFamily: "var(--font-geist-sans), system-ui, sans-serif",
        padding: "2rem",
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: "2rem", fontWeight: 700, margin: 0 }}>EngageDash</h1>
      <p style={{ color: "#666", margin: 0 }}>AI-powered Customer Success Insights Dashboard</p>
      <p style={{ color: "#999", fontSize: "0.875rem", margin: 0 }}>
        Frontend skeleton — UI is built out from Phase 7.
      </p>
    </main>
  );
}
