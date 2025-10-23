import React, { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import "./Auth.css";
import MagicBento from "../UI/MagicBento";
import Footer from "../Layout/Footer";

const SHOWCASE_CHIPS = [
  "Auto NDVI refresh",
  "Hyperlocal forecast",
  "Soil nutrient advisor",
  "Pest watch AI",
];

const HIGHLIGHT_METRICS = [
  {
    label: "NDVI • Avg field health",
    value: "0.81",
    trend: "+4.8%",
    positive: true,
  },
  { label: "24h rain outlook", value: "12 mm", trend: "-18%", positive: false },
  { label: "Soil moisture", value: "68%", trend: "+7.0%", positive: true },
  { label: "Pest pressure", value: "Low", trend: "Stable", positive: true },
];

const ROTATING_INSIGHTS = [
  {
    icon: "🌱",
    title: "Vegetation spike detected",
    subtitle: "Satellite sync • 12 minutes ago",
    description:
      "Last Sentinel-2 pass shows a 3.2% uptick in canopy vigor on the eastern plots. Stay on top of irrigation to sustain momentum.",
    progress: 76,
    trend: "+3.1% vs yesterday",
    focus: "Irrigation efficiency",
    positive: true,
  },
  {
    icon: "☔",
    title: "Rain window incoming",
    subtitle: "OpenWeather • 2 hour lead",
    description:
      "A narrow rainfall band is projected between 17:00-18:00. Prep your soil amendments to maximize nutrient uptake post-shower.",
    progress: 64,
    trend: "45 min advance notice",
    focus: "Weather sync",
    positive: true,
  },
  {
    icon: "🪲",
    title: "Pest pressure minimal",
    subtitle: "Regional scout • Updated just now",
    description:
      "Trap data indicates low aphid counts across 35 km radius. Hold off on spraying and log scouting notes to keep the streak.",
    progress: 38,
    trend: "Stable week-over-week",
    focus: "Pest surveillance",
    positive: true,
  },
];

const SHOWCASE_POINTS = [
  "95% anomaly detection accuracy",
  "Live weather + soil telemetry",
  "One-click PDF crop briefings",
];

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [activeInsight, setActiveInsight] = useState(0);

  const { login } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const ticker = setInterval(() => {
      setActiveInsight((prev) => (prev + 1) % ROTATING_INSIGHTS.length);
    }, 5000);
    return () => clearInterval(ticker);
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (!formData.email || !formData.password) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }

    const result = await login(formData.email, formData.password);

    if (result.success) {
      navigate("/dashboard");
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const currentInsight = ROTATING_INSIGHTS[activeInsight];

  return (
    <div className="auth-container advanced-auth">
      <div className="auth-layout">
        <aside className="auth-showcase">
          <div className="showcase-inner">
            <div className="showcase-header">
              <span className="showcase-badge">Crop intelligence hub</span>
              <h2 className="showcase-title">
                Monitor <span>every acre</span> with live satellite and sensor
                fusion.
              </h2>
              <p className="showcase-subtitle">
                CropEye distills NDVI, soil labs, pest traps and hyperlocal
                weather into one actionable cockpit, refreshed every few
                minutes.
              </p>
            </div>
            <Footer />

            <div className="showcase-chips">
              {SHOWCASE_CHIPS.map((chip) => (
                <span className="showcase-chip" key={chip}>
                  {chip}
                </span>
              ))}
            </div>

            <div className="showcase-metrics">
              {HIGHLIGHT_METRICS.map((metric) => (
                <div className="metric-card" key={metric.label}>
                  <div className="metric-label">{metric.label}</div>
                  <div className="metric-value">{metric.value}</div>
                  <div
                    className={`metric-trend ${
                      metric.positive ? "positive" : "negative"
                    }`}
                  >
                    {metric.trend}
                  </div>
                </div>
              ))}
            </div>

            <div className="insight-card">
              <div className="insight-top">
                <div className="insight-icon">{currentInsight.icon}</div>
                <div>
                  <div className="insight-title">{currentInsight.title}</div>
                  <div className="insight-timestamp">
                    {currentInsight.subtitle}
                  </div>
                </div>
              </div>
              <p className="insight-description">
                {currentInsight.description}
              </p>
              <div className="insight-progress">
                <div
                  className="progress-bar"
                  style={{ width: `${currentInsight.progress}%` }}
                />
              </div>
              <div className="insight-footer">
                <span>{currentInsight.focus}</span>
                <span
                  className={`metric-trend ${
                    currentInsight.positive ? "positive" : "negative"
                  }`}
                >
                  {currentInsight.trend}
                </span>
              </div>
            </div>

            <ul className="showcase-highlights">
              {SHOWCASE_POINTS.map((point) => (
                <li key={point}>
                  <span />
                  {point}
                </li>
              ))}
            </ul>
          </div>
        </aside>

        <MagicBento className="auth-card">
          <div className="auth-card">
            <h2 className="auth-title">Sign in to CropEye</h2>
            <p className="auth-subtitle">
              Access the live agronomic mission control
            </p>

            <form onSubmit={handleSubmit} className="auth-form">
              {error && <div className="error-message">{error}</div>}

              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@farm.co"
                  required
                />
              </div>

              <div className="form-group password-group">
                <label htmlFor="password">Password</label>
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  className="visibility-toggle"
                  onClick={togglePasswordVisibility}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>

              <div className="form-meta">
                <span>Secure by JWT & bcrypt hashing</span>
                <a
                  href="https://cropeye.dev/docs"
                  target="_blank"
                  rel="noreferrer"
                >
                  View docs
                </a>
              </div>

              <button type="submit" className="auth-button" disabled={loading}>
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>

            <p className="auth-link">
              Don't have an account?{" "}
              <Link to="/register">Create one in seconds</Link>
            </p>

            <div className="auth-divider">or explore instantly</div>
            <div className="demo-credentials">
              <h4>Demo mission control</h4>
              <div className="demo-row">
                <span className="demo-label">Email</span>
                <span className="demo-value">demo@cropeye.dev</span>
              </div>
              <div className="demo-row">
                <span className="demo-label">Password</span>
                <span className="demo-value">DemoPass123!</span>
              </div>
            </div>
          </div>
        </MagicBento>
      </div>
    </div>
  );
};

export default Login;
