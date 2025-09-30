import './globals.css'

export const metadata = { title: 'Moodify' }

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  )
}
