        /* ═══════════════════════════════════════════
           STAGE 1 START: INPUT SCREEN
           ═══════════════════════════════════════════ */
        const Screen1Input = ({ appState, updateState, navigateForward }) => {
            const [dragOver, setDragOver] = useState(false);
            const [isDrafting, setIsDrafting] = useState(false);
            const [showSettings, setShowSettings] = useState(false);
            const [validationError, setValidationError] = useState('');

            const handleFile = async (file) => {
                if (!file) return;
                const ext = file.name.split('.').pop().toLowerCase();
                
                updateState({ 
                    fileInfo: { name: file.name, size: (file.size / 1024).toFixed(1) + ' KB', type: ext.toUpperCase() } 
                });

                if (ext === 'pdf') {
                    // Extract text using pdf.js
                    const reader = new FileReader();
                    reader.onload = async function() {
                        const typedarray = new Uint8Array(this.result);
                        try {
                            const pdf = await pdfjsLib.getDocument(typedarray).promise;
                            let fullText = '';
                            for (let i = 1; i <= pdf.numPages; i++) {
                                const page = await pdf.getPage(i);
                                const textContent = await page.getTextContent();
                                const pageText = textContent.items.map(item => item.str).join(' ');
                                fullText += pageText + '\n\n';
                            }
                            updateState({ pastedText: fullText });
                        } catch(e) { alert("Failed to read PDF text."); }
                    };
                    reader.readAsArrayBuffer(file);
                } else if (ext === 'txt' || ext === 'md' || ext === 'html') {
                    const reader = new FileReader();
                    reader.onload = (e) => updateState({ pastedText: e.target.result });
                    reader.readAsText(file);
                } else {
                    alert("Only text-based files (PDF, TXT, MD, HTML) are supported in V1.");
                }
            };

            const handleAIDraft = async () => {
                if (!appState.topic.trim()) return;
                setIsDrafting(true);
                try {
                    const prompt = `Write comprehensive study material about: ${appState.topic}.
                        Sub-topics to cover: ${appState.subTopics.filter(Boolean).join(', ')}.
                        ${appState.focus ? `Focus: ${appState.focus}` : ''}
                        Write in a clear, educational style suitable for exam preparation. Include definitions, examples, and key facts.
                        Length: around 600 words.`;
                    
                    // CALLING NATIVE AI FUNCTION HERE
                    const drafted = await window.geminiGenerateText(prompt);
                    updateState({ pastedText: drafted });
                } catch (e) {
                    alert('AI Drafting Failed: ' + e.message);
                } finally {
                    setIsDrafting(false);
                }
            };

            const handleContinue = () => {
                if (!appState.pastedText.trim() && !appState.topic.trim()) {
                    setValidationError('Please upload a file, type a topic, or paste text to continue.');
                    return;
                }
                setValidationError('');
                navigateForward(2);
            };

            return (
                <div className="max-w-4xl mx-auto py-8 px-4 fade-in">
                    <div className="text-center mb-8">
                        <h1 className="text-3xl font-bold text-gray-900 mb-2">Transform any material into structured notes</h1>
                        <p className="text-gray-500">Provide your source material via upload, AI generation, or manual paste.</p>
                    </div>

                    <div className="space-y-6">
                        {/* Section A: Upload */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                                <span className="bg-blue-100 text-blue-600 w-6 h-6 rounded-full flex items-center justify-center text-sm">A</span>
                                Upload File
                            </h2>
                            <div 
                                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                                onDragLeave={() => setDragOver(false)}
                                onDrop={(e) => { e.preventDefault(); setDragOver(false); handleFile(e.dataTransfer.files[0]); }}
                                onClick={() => document.getElementById('file-upload').click()}
                                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
                                    ${dragOver ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-blue-50'}`}
                            >
                                <input type="file" id="file-upload" className="hidden" accept=".pdf,.txt,.md,.html" onChange={(e) => handleFile(e.target.files[0])} />
                                {appState.fileInfo ? (
                                    <div className="text-blue-700 font-medium">📄 {appState.fileInfo.name} loaded successfully! Text extracted below.</div>
                                ) : (
                                    <div>
                                        <span className="text-3xl mb-2 block">📁</span>
                                        <p className="font-medium text-gray-700">Drop PDF or text file here</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="h-px bg-gray-200 flex-1"></div><span className="text-gray-400 text-sm font-medium">OR</span><div className="h-px bg-gray-200 flex-1"></div>
                        </div>

                        {/* Section B: Topic & AI Draft */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                                <span className="bg-blue-100 text-blue-600 w-6 h-6 rounded-full flex items-center justify-center text-sm">B</span>
                                Type Topic & Generate
                            </h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Main Topic</label>
                                    <input type="text" value={appState.topic} onChange={(e) => updateState({topic: e.target.value})} placeholder="e.g. Plate Tectonics" className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none" />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Sub-topics (comma separated)</label>
                                        <input type="text" value={appState.subTopics.join(',')} onChange={(e) => updateState({subTopics: e.target.value.split(',')})} placeholder="e.g. Divergent, Convergent" className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none" />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">Specific Focus</label>
                                        <input type="text" value={appState.focus} onChange={(e) => updateState({focus: e.target.value})} placeholder="e.g. Focus on Indian Plate" className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none" />
                                    </div>
                                </div>
                                {appState.topic.trim() && (
                                    <button onClick={handleAIDraft} disabled={isDrafting} className="w-full bg-purple-100 text-purple-700 hover:bg-purple-200 py-2 rounded-md font-semibold transition-colors disabled:opacity-50">
                                        {isDrafting ? '✨ AI is Drafting Material...' : '✨ Auto-Draft Material using AI'}
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Section C: Paste Text */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                                <span className="bg-blue-100 text-blue-600 w-6 h-6 rounded-full flex items-center justify-center text-sm">C</span>
                                Review / Paste Text
                            </h2>
                            <textarea rows="8" value={appState.pastedText} onChange={(e) => updateState({pastedText: e.target.value})} placeholder="Source text will appear here. You can also manually paste notes here." className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"></textarea>
                            <div className="text-right text-xs text-gray-500 mt-1">{appState.pastedText.length.toLocaleString()} / 50,000 chars</div>
                        </div>

                        {/* Optional Settings */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                            <button onClick={() => setShowSettings(!showSettings)} className="w-full bg-gray-50 px-6 py-3 flex justify-between items-center text-gray-700 font-semibold">
                                <span>⚙️ Optional Generation Settings</span>
                                <span>{showSettings ? '▲' : '▼'}</span>
                            </button>
                            {showSettings && (
                                <div className="p-6 grid grid-cols-2 gap-4 bg-white border-t border-gray-200">
                                    <div>
                                        <label className="block text-xs font-medium text-gray-600 mb-1">Exam Type</label>
                                        <select value={appState.settings.exam} onChange={(e) => updateState({settings: {...appState.settings, exam: e.target.value}})} className="w-full border border-gray-300 rounded-md p-2 text-sm">
                                            <option>General Learning</option><option>UPSC</option><option>State PSC</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-xs font-medium text-gray-600 mb-1">State Focus</label>
                                        <input type="text" value={appState.settings.state} onChange={(e) => updateState({settings: {...appState.settings, state: e.target.value}})} placeholder="e.g. MP" className="w-full border border-gray-300 rounded-md p-2 text-sm" />
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Continue Button */}
                        {validationError && <div className="text-red-600 text-sm font-semibold text-center">{validationError}</div>}
                        <button onClick={handleContinue} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl shadow-md text-lg transition-colors">
                            Continue to Reading ➔
                        </button>
                    </div>
                </div>
            );
        };
        /* ═══════════════════════════════════════════
           STAGE 1 END
           ═══════════════════════════════════════════ */
