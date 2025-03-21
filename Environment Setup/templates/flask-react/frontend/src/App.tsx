import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import axios from 'axios'

const queryClient = new QueryClient()

function App() {
  const [backendMessage, setBackendMessage] = useState('')

  useEffect(() => {
    axios.get('http://localhost:5000/api/test')
      .then(response => setBackendMessage(response.data.message))
      .catch(error => console.error('Error:', error))
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <header className="bg-white shadow">
            <div className="max-w-7xl mx-auto py-6 px-4">
              <h1 className="text-3xl font-bold text-gray-900">
                Flask + TypeScript App <span className="text-purple-600">by Scripty</span>
              </h1>
            </div>
          </header>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <p className="text-gray-600">Backend Message:</p>
                <p className="text-lg font-semibold mt-2">{backendMessage}</p>
              </div>
              <Routes>
                <Route path="/" element={<div>Welcome to your Flask + TypeScript app!</div>} />
              </Routes>
            </div>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App