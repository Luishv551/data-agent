import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'CloudWalk Data Agent',
  description: 'Natural language interface for CloudWalk transaction data analysis',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
