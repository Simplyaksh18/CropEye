import React from "react";
import { motion } from "framer-motion";

const PageSection = ({ title, subtitle, children, mediaUrl, badge, icon }) => (
  <motion.section
    className="page-section"
    initial={{ opacity: 0, y: 16 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.4, ease: "easeOut" }}
  >
    <div className="page-section__content">
      <div className="page-section__head">
        <div className="page-section__title">
          {badge && <span className="page-section__badge">{badge}</span>}
          <div className="page-section__title-row">
            {icon && <span className="page-section__icon">{icon}</span>}
            <h2>{title}</h2>
          </div>
          {subtitle && <p className="page-section__subtitle">{subtitle}</p>}
        </div>
      </div>
      <div className="page-section__body">{children}</div>
    </div>
    {mediaUrl && (
      <div className="page-section__media">
        <img src={mediaUrl} alt="Section visual" loading="lazy" />
      </div>
    )}
  </motion.section>
);

export default PageSection;
