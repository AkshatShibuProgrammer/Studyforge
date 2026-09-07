import json
import re

ai_04 = """TASK: Split the material into coherent teachable parts and assign only relevant selected bundles to each part.

Document topic and context:
{{TOPIC}}
{{EXAM_CONTEXT}}

Total source length and page information:
{{SOURCE_LENGTH_AND_PAGE_INFO_JSON}}

Recommended part-count guardrail:
{{PART_COUNT_GUARDRAIL_JSON}}

Merged structured analysis. Use this as the primary input:
{{DEEP_ANALYSIS_JSON}}

Selected global bundle features:
{{BUNDLE_SELECTIONS_JSON}}

Supporting source context. This is either the full source when safe or topic-level summaries when the source is large:
{{SPLITTING_SOURCE_CONTEXT}}

Requirements:
1. Use the recommended page/length range as a guardrail, not an absolute rule.
2. Prioritize conceptual coherence: related topics stay together; a formula stays with its explanation; a PYQ stays with the topic it tests; examples stay near the concept they explain.
3. Avoid tiny parts containing only one or two short paragraphs unless that content is independently necessary.
4. If coherent learning requires a count outside the guardrail, return the proposal but set an explicit warning.
5. Assign selected global bundles only to parts where source evidence and part content make them relevant. Do not assign a formula bundle to a part with no formula-related content merely because the bundle is globally enabled.
6. Return stable part IDs, page/source scope, topic IDs, analysis references, applied bundle IDs, and a concise rationale.
7. Do not generate notes or images in this call.

Return exactly this JSON object:
{
  "recommended_range": {"min_parts": 0, "max_parts": 0},
  "proposed_count": 0,
  "out_of_range_warning": {"required": false, "message": ""},
  "parts": [
    {
      "part_id": "P-01",
      "title": "",
      "page_range": [],
      "topic_ids": [],
      "analysis_refs": {"definitions": [], "formulas": [], "pyqs": [], "examples": [], "timelines": [], "tables": [], "comparisons": []},
      "applied_bundles": [],
      "rationale": "",
      "density_note": ""
    }
  ]
}"""

# Step 1: Inject AI_04 into DEFAULT_PROMPTS
with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

insert_str = f"      AI_04: `{ai_04.replace('`', '\\`')}`,\n"
pattern = r'const DEFAULT_PROMPTS = \{'
match = re.search(pattern, content)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + '\n' + insert_str + content[insert_pos:]

# Step 2: Inject Screen4 logic before const Step2
screen_logic = """
    const Screen4_Splitting = {
      async init() {
        const streamBox = document.getElementById('screen4-content');
        streamBox.innerHTML = '<div class="font-mono text-xs text-sky-600 bg-sky-50 p-4 rounded-lg shadow-inner">[SYSTEM] Initiating Intelligent Splitting...</div>';
        
        try {
          const pgCount = Math.max(1, Math.ceil((appState.pdfText || "").length / 3000));
          const guardrail = { min_parts: 1, max_parts: Math.ceil(pgCount / 2) };
          const enabledBundles = (appState.bundleSelections || []).filter(b => b.user_enabled || b.state === 'auto_on');

          let p4 = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_04
            .replace('{{TOPIC}}', appState.subject)
            .replace('{{EXAM_CONTEXT}}', appState.category || 'General')
            .replace('{{SOURCE_LENGTH_AND_PAGE_INFO_JSON}}', JSON.stringify({ chars: (appState.pdfText || "").length, estimated_pages: pgCount }))
            .replace('{{PART_COUNT_GUARDRAIL_JSON}}', JSON.stringify(guardrail))
            .replace('{{DEEP_ANALYSIS_JSON}}', JSON.stringify(appState.deepAnalysis))
            .replace('{{BUNDLE_SELECTIONS_JSON}}', JSON.stringify(enabledBundles))
            .replace('{{SPLITTING_SOURCE_CONTEXT}}', '[]');

          let res4 = await API.generateContent(p4 + '\\n\\nOutput JSON only.');
          let parsed4 = JSON.parse(res4.replace(/```json\\n?|```/g, ''));
          appState.blueprint.parts = parsed4.parts || [];
          
          streamBox.innerHTML += `<div class="font-mono text-xs text-emerald-600 mt-2">✔ Split into ${parsed4.proposed_count || appState.blueprint.parts.length} parts based on coherence.</div>`;
          
          // Move to Blueprint Planning
          setTimeout(() => App.navigate(5), 1000);

        } catch (e) {
          Logger.add('ERROR', 'S4_SPLITTING', e.message);
          streamBox.innerHTML += `<div class="font-mono text-xs text-rose-600 mt-2">Error during splitting: ${e.message}</div>`;
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

print("Screen4 logic injected!")
