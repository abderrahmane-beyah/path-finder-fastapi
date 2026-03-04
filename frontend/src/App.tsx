import { useState, useEffect, type FormEvent } from 'react'
import './App.css'

interface PathInfo {
  numero: number
  chemin: string[]
  route_str: string
  distance: number
  difference: number
  pourcentage: number
  est_optimal: boolean
}

interface RouteResponse {
  error: string | null
  image_data: string | null
  selected_start: string | null
  selected_end: string | null
  all_paths: PathInfo[]
}

function App() {
  const [cities, setCities] = useState<string[]>([])
  const [startCity, setStartCity] = useState('')
  const [endCity, setEndCity] = useState('')
  const [results, setResults] = useState<RouteResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/cities')
      .then((res) => res.json())
      .then((data) => setCities(data.cities))
      .catch(() => setError('Failed to load cities.'))
  }, [])

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setResults(null)

    if (!startCity || !endCity) {
      setError('Please select both start and end cities.')
      return
    }
    if (startCity === endCity) {
      setError('Start and end cities must be different.')
      return
    }

    setLoading(true)
    try {
      const response = await fetch('/api/routes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start_city: startCity, end_city: endCity }),
      })
      const data: RouteResponse = await response.json()

      if (data.error) {
        setError(data.error)
      } else if (data.all_paths.length > 0) {
        setResults(data)
      } else {
        setError('No routes found between these cities.')
      }
    } catch {
      setError('An error occurred while finding routes.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Route Finder in Mauritania</h1>
      <p>Select your starting and destination cities to find the shortest route.</p>

      {error && <div className="error">{error}</div>}

      {loading && (
        <div className="loading active">
          <div className="spinner" />
          <p>Finding routes...</p>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <label htmlFor="start_city">Starting City:</label>
        <select
          id="start_city"
          value={startCity}
          onChange={(e) => setStartCity(e.target.value)}
          required
        >
          <option value="" disabled>-- Select starting city --</option>
          {cities.map((city) => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>

        <label htmlFor="end_city">Destination City:</label>
        <select
          id="end_city"
          value={endCity}
          onChange={(e) => setEndCity(e.target.value)}
          required
        >
          <option value="" disabled>-- Select destination city --</option>
          {cities.map((city) => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>

        <button type="submit" disabled={loading}>Find Shortest Route</button>
      </form>

      {results && (
        <div className="result">
          <h3>Routes Found:</h3>
          {results.all_paths.map((path, index) => (
            <div key={path.numero} className={`path-card path-${index + 1}`}>
              <div className="path-header">
                <span className={`badge ${path.est_optimal ? 'optimal' : 'alternative'}`}>
                  {path.est_optimal ? 'Optimal' : `Alternative ${index}`}
                </span>
                <strong>Route {index + 1}</strong>
              </div>
              <div className="path-info">
                <p><strong>Route:</strong> {path.route_str}</p>
                <p>
                  <strong>Distance:</strong> {path.distance} km
                  {!path.est_optimal && (
                    <span className="difference">
                      {' '}(+{path.difference} km, +{path.pourcentage.toFixed(1)}%)
                    </span>
                  )}
                </p>
              </div>
            </div>
          ))}

          {results.image_data && (
            <>
              <hr />
              <h4>Route Visualization:</h4>
              <img
                src={`data:image/png;base64,${results.image_data}`}
                alt="Route graph"
                className="visualization"
              />
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default App
