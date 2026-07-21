// @ts-ignore
import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "EduLens — The Intelligent Study-Streamer",
  description: "Turn long videos and PDFs into interactive, searchable study material.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-white/5">
          <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
            <Link href="/" className="flex items-center gap-2 font-semibold text-lg">
              <span className="w-7 h-7 rounded-lg bg-brand-500 grid place-items-center text-sm">EL</span>
              EduLens
            </Link>
            <div className="flex items-center gap-6 text-sm text-slate-300">
              <Link href="/upload" className="hover:text-white transition-colors">Upload</Link>
              <Link href="/dashboard" className="hover:text-white transition-colors">Library</Link>
            </div>
          </nav>
        </header>
        <main className="max-w-6xl mx-auto px-6 py-10">{children}</main>
      </body>
    </html>
  );
}