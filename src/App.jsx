import { useState, useMemo } from 'react';
import { Search, Car, Info, Hash, AlertCircle } from 'lucide-react';
import vmoData from './data/vmos.json';
import metroLogo from './assets/metro-logo.png';

function App() {
  const [query, setQuery] = useState('');

  // Helper to split searchable text into words
  const itemToWords = (item) => {
    // Combine description, model, makeName
    // Handle potential non-string values gracefully (though validation confirmed strings)
    const desc = item.description || '';
    const model = item.model || '';
    const name = item.makeName || '';
    const text = `${desc} ${model} ${name}`;
    return text.toLowerCase().split(/[\s-]+/).filter(Boolean);
  };

  const results = useMemo(() => {
    if (!query) return [];

    // Normalize query: uppercase for consistency with codes, but we handle case-insensitivity below
    const lowerQuery = query.toLowerCase().trim();
    if (!lowerQuery) return [];

    return vmoData.filter(item => {
      // 1. Code match (starts with)
      const isCodeMatch = item.code.toLowerCase().startsWith(lowerQuery);

      // 2. Name match (includes)
      const isNameMatch = item.searchTerms.toLowerCase().includes(lowerQuery);

      return isCodeMatch || isNameMatch;
    }).sort((a, b) => {
      const aCode = a.code.toLowerCase();
      const bCode = b.code.toLowerCase();

      // --- PRIORITY 1: EXACT CODE MATCH ---
      // If one is an exact code match and the other isn't, the exact match wins.
      const aExact = aCode === lowerQuery;
      const bExact = bCode === lowerQuery;
      if (aExact && !bExact) return -1;
      if (!aExact && bExact) return 1;

      // If both are exact matches, prioritize MAKES over MODELS
      if (aExact && bExact) {
        if (a.type === 'make' && b.type !== 'make') return -1;
        if (a.type !== 'make' && b.type === 'make') return 1;
      }

      // --- PRIORITY 2: STARTS WITH CODE ---
      // If one code actually starts with the query and the other doesn't (it's just a name match)
      const aCodeStart = aCode.startsWith(lowerQuery);
      const bCodeStart = bCode.startsWith(lowerQuery);
      if (aCodeStart && !bCodeStart) return -1;
      if (!aCodeStart && bCodeStart) return 1;

      // --- PRIORITY 3: WORD START (e.g. "ECO" -> "ECONOLINE") ---
      // Check if any word in the description starts with the query
      // We look at 'makeName' and 'model' or 'description'
      const aTerms = itemToWords(a);
      const bTerms = itemToWords(b);

      const aWordStart = aTerms.some(w => w.startsWith(lowerQuery));
      const bWordStart = bTerms.some(w => w.startsWith(lowerQuery));

      if (aWordStart && !bWordStart) return -1;
      if (!aWordStart && bWordStart) return 1;

      // --- PRIORITY 4: SHORTER CODE WINS (e.g. "F" search -> "F" vs "F150") ---
      if (aCode.length !== bCode.length) return aCode.length - bCode.length;

      // --- FALLBACK: ALPHABETICAL ---
      return a.description.localeCompare(b.description);
    }).slice(0, 75); // Increased limit slightly
  }, [query]);



  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-4 sm:p-12 font-sans selection:bg-red-900 selection:text-white">
      <div className="max-w-4xl mx-auto space-y-8 sm:space-y-10">

        {/* Header */}
        <header className="text-center space-y-6 pt-4 sm:pt-0 relative z-20">
          <div className="flex justify-center">
            <img
              src={metroLogo}
              alt="Metro 911 Logo"
              className="h-40 sm:h-52 w-auto drop-shadow-2xl"
            />
          </div>
          <div className="space-y-4">
            <h1 className="text-4xl sm:text-6xl font-black tracking-tighter text-white uppercase drop-shadow-lg scale-y-105">
              <span className="text-red-600">VMO</span> Lookup
            </h1>
            <p className="text-neutral-600 text-xs font-mono uppercase tracking-widest pt-2">
              v2026.01.15.1540
            </p>
          </div>
        </header>

        {/* Search Input */}
        <div className="relative group z-10 sticky top-4 sm:static">
          <div className="absolute -inset-1 bg-gradient-to-r from-red-600 to-red-900 rounded-lg blur opacity-40 group-focus-within:opacity-80 transition duration-500"></div>
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="ENTER CODE (0AKL) OR NAME..."
              className="w-full bg-neutral-900/95 backdrop-blur-xl text-xl sm:text-3xl p-5 sm:p-7 pl-14 sm:pl-20 rounded-md border border-neutral-700 shadow-2xl placeholder:text-neutral-600 focus:outline-none focus:border-red-500 text-white font-black uppercase tracking-wider transition-all"
              autoFocus
            />
            <Search className="absolute left-6 sm:left-8 top-1/2 -translate-y-1/2 text-neutral-500 w-7 h-7 sm:w-8 sm:h-8 group-focus-within:text-red-500 transition-colors" />
            {query && (
              <div className="absolute right-4 sm:right-6 top-1/2 -translate-y-1/2">
                <span className="text-[10px] sm:text-xs font-black bg-red-600/20 px-3 py-1.5 rounded-sm text-red-500 border border-red-600/30 uppercase tracking-widest">
                  {results.length} Results
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Results List */}
        <div className="space-y-4">
          {results.map((item) => (
            <div
              key={item.id}
              className="group relative bg-neutral-900 hover:bg-neutral-800 border-l-4 border-l-transparent hover:border-l-red-600 border-y border-r border-neutral-800 p-4 sm:p-6 rounded-r-md transition-all duration-200 ease-out shadow-lg hover:shadow-red-900/10"
            >
              <div className="flex flex-col sm:flex-row items-center sm:items-start gap-5 sm:gap-6 text-center sm:text-left">
                {/* Code Badge */}
                <div className="flex-shrink-0">
                  <div className={`w-24 h-24 rounded-md flex items-center justify-center border-2 shadow-inner ${item.code.toLowerCase() === query.toLowerCase()
                    ? 'bg-red-600 border-red-500 text-white shadow-red-900/50'
                    : 'bg-neutral-800 border-neutral-700 text-neutral-300'
                    }`}>
                    <span className="font-mono font-black text-3xl tracking-tighter">
                      {item.code}
                    </span>
                  </div>
                </div>

                {/* Content */}
                <div className="flex-grow min-w-0 w-full mb-1">
                  <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-2">
                    <h2 className="text-2xl sm:text-3xl font-black text-white break-words leading-none uppercase tracking-tight">
                      {item.type === 'make' ? item.makeName : (item.description || item.model)}
                    </h2>

                    {/* Exact Match Indicator */}
                    {item.code.toLowerCase() === query.toLowerCase() && (
                      <span className="inline-block mx-auto sm:mx-0 text-[10px] font-black uppercase tracking-widest bg-red-600 text-white px-2 py-1 rounded-sm w-fit shadow-md shadow-red-900/20">
                        Exact Match
                      </span>
                    )}
                  </div>

                  {/* Simplified Sub-info */}
                  <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3 mt-2">
                    {/* Display Make Name for Models, or 'Manufacturer' for Makes */}
                    {item.type === 'model' ? (
                      <span className="text-neutral-400 font-bold uppercase tracking-wide text-lg">
                        {item.makeName}
                      </span>
                    ) : (
                      <span className="text-neutral-500 text-sm uppercase font-bold tracking-wide">
                        Vehicle Manufacturer
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Empty States */}
          {query && results.length === 0 && (
            <div className="text-center py-20 rounded-md bg-neutral-900 border border-neutral-800 border-dashed">
              <div className="inline-flex p-4 rounded-full bg-neutral-800 mb-4">
                <AlertCircle className="w-10 h-10 text-red-600" />
              </div>
              <p className="text-neutral-400 text-xl font-bold uppercase">No matches found</p>
              <p className="text-neutral-600 text-sm mt-2 uppercase tracking-wide">Query: <span className="text-red-500">{query}</span></p>
            </div>
          )}

          {!query && (
            <div className="text-center py-32 opacity-20">
              <div className="inline-flex justify-center items-center w-24 h-24 rounded-full border-4 border-neutral-800 mb-6">
                <Search className="w-10 h-10 text-neutral-700" />
              </div>
              <p className="text-2xl font-black text-neutral-700 uppercase tracking-widest">System Ready</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
