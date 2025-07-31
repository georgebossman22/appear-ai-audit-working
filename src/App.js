import { useState } from "react";
import "./App.css";

function App() {
  const [contactName, setContactName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [business, setBusiness] = useState("");
  const [location, setLocation] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const runAudit = async () => {
    setLoading(true);

    try {
      await fetch("https://hook.eu2.make.com/oro7fxpewgxa31b8ke1aofxol60129xo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: contactName,
          phone,
          email,
          business,
          location,
        }),
      });

      console.log("Audit submitted:", {
        contactName,
        phone,
        email,
        business,
        location,
      });

      // Simulated response for frontend display
      const simulatedResponse = {
        directories: ["Google Business", "Yelp", "Bing Places"],
        missing: ["Yelp"],
        aiMention: false,
        recommendations: [
          "Create a Yelp profile with full business details.",
          "Add structured FAQ to your website (schema.org markup).",
          "Get mentioned on local blogs or Reddit threads.",
        ],
      };

      setResults(simulatedResponse);
    } catch (error) {
      console.error("Error submitting to webhook:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>AI Visibility Audit</h1>
      <p>Find out if your business shows up in AI tools like ChatGPT, Bing, and Google.</p>

      <input
        type="text"
        placeholder="Your Full Name"
        value={contactName}
        onChange={(e) => setContactName(e.target.value)}
      />

      <input
        type="tel"
        placeholder="Phone Number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="text"
        placeholder="Business Name (e.g. Elena’s Café)"
        value={business}
        onChange={(e) => setBusiness(e.target.value)}
      />

      <input
        type="text"
        placeholder="Location (e.g. London, SW7)"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />

      <button onClick={runAudit} disabled={loading}>
        {loading ? "Running Audit..." : "Run Free AI Audit"}
      </button>

      {results && (
        <div className="results">
          <h2>Audit Results</h2>
          <p><strong>Directories Found:</strong> {results.directories.join(", ")}</p>
          <p><strong>Missing Listings:</strong> {results.missing.join(", ")}</p>
          <p><strong>AI Mentions Detected:</strong> {results.aiMention ? "Yes" : "No"}</p>
          <ul>
            {results.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
