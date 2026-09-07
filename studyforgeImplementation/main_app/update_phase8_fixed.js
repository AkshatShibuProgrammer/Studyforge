const fs = require('fs');
let html = fs.readFileSync('studyforge_main.html', 'utf8');

// The string we are looking to replace
const promptCenterStartStr = `const PromptCenter = ({ prompts, promptHistory = [], onUpdate, onClose }) => {`;

let startIdx = html.indexOf(promptCenterStartStr);
if (startIdx === -1) {
    startIdx = html.indexOf('const PromptCenter =');
}
if (startIdx === -1) {
    console.error("PromptCenter not found!");
} else {
    // Find the end of PromptCenter by counting braces
    let braceCount = 0;
    let endIdx = -1;
    let started = false;
    for (let i = startIdx; i < html.length; i++) {
        if (html[i] === '{') {
            braceCount++;
            started = true;
        } else if (html[i] === '}') {
            braceCount--;
        }
        
        if (started && braceCount === 0) {
            // Found the matching closing brace
            // We know PromptCenter ends with `        };`
            endIdx = html.indexOf(';', i);
            break;
        }
    }
    
    if (endIdx !== -1) {
        const newPromptCenter = `const PromptCenter = ({ prompts, promptHistory = [], onUpdate, onClose }) => {
            const [tab, setTab] = useState('templates');
            const [showSystem, setShowSystem] = useState(false); // Option C: Toggle System Prompts
            const promptKeys = Object.keys(prompts || {});
            
            return (
                <Modal title="🔧 Prompt Center" onClose={onClose} wide>
                    <div className="flex gap-4 border-b border-gray-200 dark:border-gray-700 mb-4 pb-2 items-center">
                        <button onClick={() => setTab('templates')} className={\`font-medium \${tab === 'templates' ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400' : 'text-gray-500 dark:text-gray-400'}\`}>Templates</button>
                        <button onClick={() => setTab('history')} className={\`font-medium \${tab === 'history' ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400' : 'text-gray-500 dark:text-gray-400'}\`}>Execution History</button>
                        {tab === 'history' && (
                            <label className="text-xs flex items-center gap-1 ml-auto text-gray-700 dark:text-gray-300 cursor-pointer">
                                <input type="checkbox" checked={showSystem} onChange={e => setShowSystem(e.target.checked)} className="rounded" />
                                Show System Context
                            </label>
                        )}
                    </div>
                    
                    {tab === 'templates' && (
                        <>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">View and edit canonical templates.</p>
                            <div className="space-y-4 max-h-[60vh] overflow-y-auto custom-scrollbar">
                                {promptKeys.map(key => (
                                    <details key={key} className="border border-gray-200 dark:border-gray-700 rounded-lg group">
                                        <summary className="px-4 py-2 bg-gray-50 dark:bg-gray-800 cursor-pointer font-medium text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex justify-between text-gray-800 dark:text-gray-200">
                                            <span>{key}</span>
                                            <span className="text-gray-400 group-open:rotate-180 transition-transform">▼</span>
                                        </summary>
                                        <div className="p-4 bg-white dark:bg-gray-900">
                                            <textarea rows={8}
                                                value={prompts[key] || ''}
                                                onChange={(e) => onUpdate(key, e.target.value)}
                                                className="w-full text-xs font-mono p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100" />
                                            <div className="flex gap-2 mt-2">
                                                <button onClick={() => navigator.clipboard.writeText(prompts[key])} className="text-xs text-blue-600 dark:text-blue-400 font-medium">📋 Copy</button>
                                                <button onClick={() => onUpdate(key, DEFAULT_PROMPTS[key])} className="text-xs text-gray-500 dark:text-gray-400 ml-4">Reset</button>
                                            </div>
                                        </div>
                                    </details>
                                ))}
                            </div>
                        </>
                    )}

                    {tab === 'history' && (
                        <>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Recent finalized prompts sent to AI.</p>
                            <div className="space-y-4 max-h-[60vh] overflow-y-auto custom-scrollbar pr-2">
                                {promptHistory.length === 0 ? <p className="text-sm text-gray-400 italic">No history yet.</p> : null}
                                {promptHistory.slice().reverse().map((h, i) => (
                                    <div key={i} className="border border-gray-200 dark:border-gray-700 rounded-lg p-3 text-sm bg-white dark:bg-gray-800">
                                        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mb-2">
                                            <span className="font-bold">{h.type}</span>
                                            <span>{new Date(h.timestamp).toLocaleTimeString()}</span>
                                        </div>
                                        {h.system && showSystem && (
                                            <div className="mb-2">
                                                <span className="font-semibold text-xs text-gray-600 dark:text-gray-400 block mb-1">System Instruction (Context):</span>
                                                <div className="bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 p-2 text-xs font-mono rounded max-h-24 overflow-y-auto text-gray-800 dark:text-gray-300">{h.system}</div>
                                            </div>
                                        )}
                                        <span className="font-semibold text-xs text-gray-600 dark:text-gray-400 block mb-1">{showSystem ? 'Final Merged User Prompt:' : 'User Prompt:'}</span>
                                        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800/50 p-2 text-xs font-mono rounded max-h-40 overflow-y-auto whitespace-pre-wrap text-gray-800 dark:text-gray-300">{h.prompt}</div>
                                        <button onClick={() => navigator.clipboard.writeText(h.prompt)} className="mt-2 text-xs text-blue-600 dark:text-blue-400 hover:underline">📋 Copy Final</button>
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
                </Modal>
            );
        }`;
        
        html = html.substring(0, startIdx) + newPromptCenter + html.substring(endIdx + 1);
        console.log("Successfully replaced PromptCenter using AST-like brace counting.");
    }
}

// Add dark mode toggle to TopBar
const topBarRegex = /const TopBar = \(\{ currentScreen, maxReachedScreen, navigateBack,\n\s*onPromptCenter, onHelp, onReset, saveStatus \}\) => \(/;
const newTopBarDef = `const TopBar = ({ currentScreen, maxReachedScreen, navigateBack,
                  onPromptCenter, onHelp, onReset, saveStatus, darkMode, setDarkMode }) => (`

html = html.replace(topBarRegex, newTopBarDef);

const navBarRightSide = `<button onClick={onPromptCenter} className="text-gray-500 hover:text-gray-700 p-1 rounded hover:bg-gray-100" title="Prompt Center">🔧</button>`;
const newNavBarRightSide = `<button onClick={() => setDarkMode(!darkMode)} className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700" title="Toggle Dark Mode">
        {darkMode ? '☀️' : '🌙'}
      </button>
      <button onClick={onPromptCenter} className="text-gray-500 hover:text-gray-700 p-1 rounded hover:bg-gray-100" title="Prompt Center">🔧</button>`;

html = html.replace(navBarRightSide, newNavBarRightSide);

// Need to pass darkMode to TopBar inside App
const appTopBarRender = `<TopBar
            currentScreen={appState.currentScreen}
            maxReachedScreen={appState.maxReachedScreen}
            navigateBack={navigateBack}
            onPromptCenter={() => setShowPrompts(true)}
            onHelp={() => setShowHelp(true)}
            onReset={resetApp}
            saveStatus={saveStatus}
          />`;
const newAppTopBarRender = `<TopBar
            currentScreen={appState.currentScreen}
            maxReachedScreen={appState.maxReachedScreen}
            navigateBack={navigateBack}
            onPromptCenter={() => setShowPrompts(true)}
            onHelp={() => setShowHelp(true)}
            onReset={resetApp}
            saveStatus={saveStatus}
            darkMode={darkMode}
            setDarkMode={setDarkMode}
          />`;

html = html.replace(appTopBarRender, newAppTopBarRender);

fs.writeFileSync('studyforge_main.html', html, 'utf8');
console.log('Update complete');
