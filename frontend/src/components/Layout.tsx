import { ReactNode } from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-agriBg flex flex-col">
      <Navbar onLogout={() => {}} />
      <main className="flex-1 p-6">{children}</main>
      <Footer />
    </div>
  );
}
