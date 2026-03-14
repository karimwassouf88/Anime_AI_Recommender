import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Miyabi AI",
  description: "Your personal anime recommendation companion",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
