import React from "react";
import "./Footer.css";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="layout-footer">
      <div className="footer-grid">
        <div className="footer-brand">
          <span className="footer-logo">
            <span aria-hidden="true">🌱</span>
            <span>CropEye</span>
          </span>
          <p>Field-ready intelligence engineered for South Asian growers.</p>
        </div>
        <div className="footer-column">
          <h4>Field desk</h4>
          <a href="mailto:advice@cropeye.ai">advice@cropeye.ai</a>
          <a href="tel:+918000000000">+91 8000 000 000</a>
          <span className="footer-note">
            Live agronomists daily 06:00–21:00 IST
          </span>
        </div>
        <div className="footer-column">
          <h4>Data fabric</h4>
          <ul>
            <li>AgroMonitoring radar & forecast stack</li>
            <li>Copernicus Sentinel-2 NDVI composites</li>
            <li>IMD & GFS mesoscale weather layers</li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <span>
          © {currentYear} CropEye Labs · Built in India for regenerative
          agriculture.
        </span>
        <a
          href="https://www.agromonitoring.com/"
          target="_blank"
          rel="noreferrer"
        >
          Data partners & trust
        </a>
      </div>
    </footer>
  );
};

export default Footer;
