// src/app/layout.tsx

import "./globals.css";

export const metadata = {
  title: "CreatorIQ",
  description: "AI Creator Analytics Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-white antialiased">
        {children}
      </body>
    </html>
  );
}