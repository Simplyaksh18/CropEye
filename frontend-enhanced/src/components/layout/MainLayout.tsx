// src/components/layout/MainLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";
import Header from "../layout/Header";
import Footer from "../layout/Footer";
import { ScrollFloat } from "../animations/ScrollFloat";

const MainLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">
      <Header />

      <ScrollFloat>
        <main className="container mx-auto px-4 py-8 min-h-[calc(100vh-200px)]">
          <Outlet />
        </main>
      </ScrollFloat>

      <Footer />
    </div>
  );
};

export default MainLayout;
