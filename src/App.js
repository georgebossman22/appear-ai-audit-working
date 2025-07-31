import { useState } from "react";
import "./App.css";

function App() {
  const [business, setBusiness] = useState("");
  const [location, setLocation] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const runAudit = () => {
    setLoading(true);
    const simulatedResponse = {
      directories: ["Google Business", "Yelp", "Bing Places"],
      missing: ["Yelp"],
      aiMention: false,
      recommendations: [
        "Create a Yelp profile with full business details.",
        "Add structured FAQ to your website (schema.org markup).",
        "Get mentioned on local blogs or Reddit threads."
      ]
    };
    setTimeout(() => {
      setResults(simulatedResponse);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="App">
      <h1>AI Visibility Audit</h1>
      <input
        type="text"
        placeholder="Business Name"
        value={business}
        onChange={(e) => setBusiness(e.target.value)}
      />
      <input
        type="text"
        placeholder="Location (e.g. London)"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />
      <button onClick={runAudit} disabled={loading}>
        {loading ? "Running Audit..." : "Run Audit"}
      </button>

      {results && (
        <div className="results">
          <p><strong>Directories Found:</strong> {results.directories.join(", ")}</p>
          <p><strong>Missing:</strong> {results.missing.join(", ")}</p>
          <p><strong>AI Mentioned in Test Prompts:</strong> {results.aiMention ? "Yes" : "No"}</p>
          <ul>
            {results.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
