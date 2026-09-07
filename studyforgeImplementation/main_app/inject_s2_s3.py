import json
import re

ai_03c = """TASK: Evaluate only the routed StudyForge feature bundles using evidence from the source and structured analysis.

Detected subject signals:
{{SUBJECT_SIGNALS_JSON}}

Structured deep analysis:
{{DEEP_ANALYSIS_JSON}}

Routed bundle definitions. Evaluate only these bundle IDs and their listed features:
{{ROUTED_BUNDLES_JSON}}

Relevant source excerpts and page references:
{{RELEVANT_SOURCE_EXCERPTS_JSON}}

Requirements:
1. Evaluate only the routed bundles. Do not add unrelated bundles.
2. For each bundle and feature, assign exactly one state: "auto_on", "suggested", or "not_detected".
3. "auto_on" requires strong direct evidence and should be suitable as a default.
4. "suggested" means there is some meaningful evidence or learning value but user choice is appropriate.
5. "not_detected" means the source does not support it now. It remains available for user force-enable.
6. Give concise evidence and reason for every non-empty result.
7. Do not hallucinate formulas, maps, cases, current affairs, personalities, processes, or other features solely because a bundle exists.
8. This call plans/detects features only. It must not fetch deep external location/personality/current-affairs facts.

Return exactly this JSON object:
{
  "bundles": [
    {
      "bundle_id": "",
      "state": "auto_on|suggested|not_detected",
      "evidence": [],
      "features": [
        {"feature_id": "", "state": "auto_on|suggested|not_detected", "reason": "", "evidence": []}
      ]
    }
  ]
}"""

# Step 1: Inject AI_03C into DEFAULT_PROMPTS
with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

insert_str = f"      AI_03C: `{ai_03c.replace('`', '\\`')}`,\n"
pattern = r'const DEFAULT_PROMPTS = \{'
match = re.search(pattern, content)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + '\n' + insert_str + content[insert_pos:]

# Step 2: Inject Screen2 and Screen3 logic before const Step2
screen_logic = """
    const Screen2_Reading = {
      async init() {
        const streamBox = document.getElementById('screen2-content');
        streamBox.innerHTML = '<div class="font-mono text-xs text-sky-600 bg-sky-50 p-4 rounded-lg shadow-inner">[SYSTEM] Starting 3-Prompt Hybrid Extraction...</div>';
        
        try {
          // PROMPT 1: Subject/Signals
          streamBox.innerHTML += '<div class="font-mono text-xs text-slate-500 mt-2">=> Executing AI-03A (Subject & Signals Detection)...</div>';
          let p1 = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_03A
            .replace('{{SOURCE_ORIGIN}}', 'upload')
            .replace('{{EXAM_CONTEXT}}', appState.category || 'General')
            .replace('{{SOURCE_TEXT}}', appState.pdfText)
            .replace('{{PAGE_MAP_JSON}}', '[]')
            .replace('{{CHUNK_CONTEXT_JSON}}', 'null');
          
          let res1 = await API.generateContent(p1 + '\\n\\nOutput JSON only.');
          let parsed1 = JSON.parse(res1.replace(/```json\\n?|```/g, ''));
          appState.signals = parsed1;
          streamBox.innerHTML += `<div class="font-mono text-xs text-emerald-600 mt-1">✔ Subject detected: ${parsed1.primary_subject || 'Unknown'}</div>`;
          appState.subject = parsed1.primary_subject || 'Unknown';

          // PROMPT 2: Deep Core Extraction
          streamBox.innerHTML += '<div class="font-mono text-xs text-slate-500 mt-2">=> Executing AI-03B (Deep Core Extraction)...</div>';
          let p2 = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_03B
            .replace('{{SUBJECT_SIGNALS_JSON}}', JSON.stringify(appState.signals))
            .replace('{{SOURCE_TEXT}}', appState.pdfText)
            .replace('{{PAGE_MAP_JSON}}', '[]')
            .replace('{{CHUNK_CONTEXT_JSON}}', 'null');

          let res2 = await API.generateContent(p2 + '\\n\\nOutput JSON only.');
          let parsed2 = JSON.parse(res2.replace(/```json\\n?|```/g, ''));
          appState.deepAnalysis = parsed2;
          streamBox.innerHTML += `<div class="font-mono text-xs text-emerald-600 mt-1">✔ Deep extraction complete. Found ${parsed2.topics?.length||0} topics, ${parsed2.definitions?.length||0} defs.</div>`;

          // Proceed to Screen 3
          setTimeout(() => App.navigate(3), 1000);

        } catch (e) {
          Logger.add('ERROR', 'S2_EXTRACTION', e.message);
          streamBox.innerHTML += `<div class="font-mono text-xs text-rose-600 mt-2">Error during extraction: ${e.message}</div>`;
        }
      }
    };

    const Screen3_Understanding = {
      async init() {
        const streamBox = document.getElementById('screen3-content');
        streamBox.innerHTML = `<div class="mb-4">
          <h3 class="font-bold text-slate-800">Detected Subject: <span class="text-indigo-600">${appState.subject}</span></h3>
          <p class="text-sm text-slate-600">Evaluating applicable bundles...</p>
        </div>`;

        try {
          // Determine routed bundles based on subject
          let routedBundles = [];
          if (appState.subject.toLowerCase().includes('econ')) routedBundles.push({id: 'BND-ECON', features: ['demand_supply_graphs', 'metrics_tables']});
          else if (appState.subject.toLowerCase().includes('polity') || appState.subject.toLowerCase().includes('law')) routedBundles.push({id: 'BND-LAW', features: ['case_law', 'articles']});
          routedBundles.push({id: 'BND-FORM', features: ['formulas']});
          routedBundles.push({id: 'BND-DATA', features: ['charts', 'tables']});

          let p3 = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_03C
            .replace('{{SUBJECT_SIGNALS_JSON}}', JSON.stringify(appState.signals))
            .replace('{{DEEP_ANALYSIS_JSON}}', JSON.stringify(appState.deepAnalysis))
            .replace('{{ROUTED_BUNDLES_JSON}}', JSON.stringify(routedBundles))
            .replace('{{RELEVANT_SOURCE_EXCERPTS_JSON}}', '[]');

          let res3 = await API.generateContent(p3 + '\\n\\nOutput JSON only.');
          let parsed3 = JSON.parse(res3.replace(/```json\\n?|```/g, ''));
          appState.bundleSelections = parsed3.bundles || [];

          // Render Three-Tier UI
          this.renderThreeTierUI(parsed3.bundles || []);

        } catch (e) {
           Logger.add('ERROR', 'S3_UNDERSTANDING', e.message);
           streamBox.innerHTML += `<div class="text-sm text-rose-600 mt-2">Failed to evaluate bundles: ${e.message}</div>`;
           // Fallback UI
           this.renderThreeTierUI([]);
        }
      },
      renderThreeTierUI(bundles) {
        let html = '<div class="space-y-4">';
        bundles.forEach(b => {
          let badge = b.state === 'auto_on' ? '<span class="bg-emerald-100 text-emerald-700 px-2 py-1 rounded text-xs font-bold">Auto-On</span>' : 
                      (b.state === 'suggested' ? '<span class="bg-amber-100 text-amber-700 px-2 py-1 rounded text-xs font-bold">Suggested</span>' : 
                      '<span class="bg-slate-100 text-slate-500 px-2 py-1 rounded text-xs font-bold">Not Detected</span>');
          
          let check = (b.state === 'auto_on' || b.state === 'suggested') ? 'checked' : '';
          
          html += `<div class="p-4 border border-slate-200 rounded-xl bg-white shadow-sm flex items-center justify-between">
            <div>
              <h4 class="font-bold text-slate-800 flex items-center gap-2">${b.bundle_id} ${badge}</h4>
              <p class="text-xs text-slate-500 mt-1">${b.evidence.join(' ') || 'No specific evidence'}</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" value="" class="sr-only peer" ${check} onchange="Screen3_Understanding.toggleBundle('${b.bundle_id}', this.checked)">
              <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
            </label>
          </div>`;
        });
        html += '</div>';
        document.getElementById('screen3-content').innerHTML += html;
      },
      toggleBundle(id, state) {
        let b = appState.bundleSelections.find(x => x.bundle_id === id);
        if (b) {
            b.user_enabled = state;
            Toaster.show(`Bundle ${id} ${state ? 'enabled' : 'disabled'}`, 'sky');
        }
      }
    };
"""

pattern_step2 = r'const Step2 = \{'
match2 = re.search(pattern_step2, content)
if match2:
    insert_pos2 = match2.start()
    content = content[:insert_pos2] + screen_logic + '\n    ' + content[insert_pos2:]

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Screen2 and Screen3 logic injected!")
