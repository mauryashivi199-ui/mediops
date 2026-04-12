import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://localhost:5000/api";

const statusColor = (s) =>
  s === "UP" ? "#22C55E" : s === "DOWN" ? "#EF4444" : "#F59E0B";

export default function Dashboard() {
  const [health, setHealth]     = useState({});
  const [metrics, setMetrics]   = useState({});
  const [prediction, setPred]   = useState({});
  const [alerts, setAlerts]     = useState([]);
  const [healing, setHealing]   = useState(null);

  const fetchAll = async () => {
    const [h, m, p, a] = await Promise.all([
      axios.get(`${API}/health`),
      axios.get(`${API}/metrics`),
      axios.get(`${API}/predict`),
      axios.get(`${API}/alerts`),
    ]);
    setHealth(h.data);
    setMetrics(m.data);
    setPred(p.data);
    setAlerts(a.data);
  };

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 15000); // Refresh every 15s
    return () => clearInterval(interval);
  }, []);

  const manualHeal = async (service) => {
    setHealing(service);
    await axios.post(`${API}/heal/${encodeURIComponent(service)}`);
    setTimeout(() => { setHealing(null); fetchAll(); }, 3000);
  };

  return (
    <div style={{ background: "#0A0F1E", minHeight: "100vh", padding: 24, color: "#fff", fontFamily: "sans-serif" }}>

      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 32 }}>
        <span style={{ fontSize: 28 }}>🏥</span>
        <h1 style={{ margin: 0, fontSize: 26, color: "#3B82F6" }}>MediOps Dashboard</h1>
        <span style={{ marginLeft: "auto", fontSize: 12, color: "#6B7280" }}>
          Live • updates every 15s
        </span>
      </div>

      {/* System Metrics Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 28 }}>
        {[
          { label: "CPU", value: metrics.cpu_percent, unit: "%" },
          { label: "RAM", value: metrics.ram_percent, unit: "%" },
          { label: "Disk", value: metrics.disk_percent, unit: "%" },
          { label: "Risk", value: metrics.risk_level, unit: "" },
        ].map((m) => (
          <div key={m.label} style={{ background: "#111827", borderRadius: 12, padding: 20, border: "1px solid #1F2937" }}>
            <div style={{ fontSize: 12, color: "#6B7280", marginBottom: 6 }}>{m.label}</div>
            <div style={{
              fontSize: 28, fontWeight: 700,
              color: m.label === "Risk"
                ? (m.value === "CRITICAL" ? "#EF4444" : m.value === "WARNING" ? "#F59E0B" : "#22C55E")
                : (m.value > 85 ? "#EF4444" : m.value > 70 ? "#F59E0B" : "#22C55E")
            }}>
              {m.value}{m.unit}
            </div>
          </div>
        ))}
      </div>

      {/* Services Health */}
      <h2 style={{ fontSize: 16, color: "#9CA3AF", marginBottom: 12 }}>Hospital Services</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 12, marginBottom: 28 }}>
        {Object.entries(health).map(([name, info]) => (
          <div key={name} style={{
            background: "#111827", borderRadius: 10, padding: 16,
            border: `1px solid ${info.status === "DOWN" ? "#EF4444" : "#1F2937"}`
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontWeight: 600 }}>{name}</span>
              <span style={{
                background: statusColor(info.status) + "22",
                color: statusColor(info.status),
                padding: "2px 10px", borderRadius: 20, fontSize: 12, fontWeight: 700
              }}>{info.status}</span>
            </div>
            {info.status === "DOWN" && (
              <button
                onClick={() => manualHeal(name)}
                disabled={healing === name}
                style={{
                  marginTop: 10, padding: "6px 14px", background: "#1D4ED8",
                  color: "#fff", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 12
                }}
              >
                {healing === name ? "⚡ Healing..." : "🔁 Auto-Heal Now"}
              </button>
            )}
          </div>
        ))}
      </div>

      {/* AI Prediction */}
      {prediction.risk_level && (
        <div style={{ background: "#111827", borderRadius: 12, padding: 20, marginBottom: 28, border: "1px solid #1F2937" }}>
          <h2 style={{ margin: "0 0 12px", fontSize: 16, color: "#9CA3AF" }}>🤖 AI Failure Prediction</h2>
          <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <div style={{
              fontSize: 36, fontWeight: 700,
              color: prediction.risk_level === "HIGH" ? "#EF4444" : prediction.risk_level === "MEDIUM" ? "#F59E0B" : "#22C55E"
            }}>
              {prediction.risk_score}/100
            </div>
            <div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>{prediction.risk_level} RISK</div>
              <div style={{ fontSize: 13, color: "#9CA3AF" }}>{prediction.recommendation}</div>
            </div>
          </div>
        </div>
      )}

      {/* Alert History */}
      <h2 style={{ fontSize: 16, color: "#9CA3AF", marginBottom: 12 }}>📲 Recent Alerts</h2>
      <div style={{ background: "#111827", borderRadius: 12, padding: 16, border: "1px solid #1F2937" }}>
        {alerts.length === 0 && <div style={{ color: "#6B7280", fontSize: 13 }}>No alerts yet — system is healthy ✅</div>}
        {alerts.slice(-5).reverse().map((a, i) => (
          <div key={i} style={{
            padding: "8px 0", borderBottom: i < alerts.length - 1 ? "1px solid #1F2937" : "none",
            fontSize: 13, color: "#D1D5DB"
          }}>
            <span style={{ color: a.success ? "#22C55E" : "#EF4444", marginRight: 8 }}>
              {a.success ? "✅" : "❌"}
            </span>
            {a.message} <span style={{ color: "#6B7280", fontSize: 11 }}>• {a.timestamp?.slice(11, 19)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
