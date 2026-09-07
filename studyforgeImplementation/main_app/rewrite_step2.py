import json
import re

ai_05 = """TASK: Create one complete execution blueprint for this specific StudyForge part. The headings, text plan, image plan, current-affairs plan, and validation plan must be designed together so they remain coherent.

Document topic and context:
{{TOPIC}}
{{EXAM_CONTEXT}}

Part plan:
{{PART_PLAN_JSON}}

Source slice for this part:
{{SOURCE_SLICE}}

Part-specific structured analysis:
{{PART_ANALYSIS_JSON}}

Complete document definitions. Use these when the part needs a definition from another part:
{{ALL_DEFINITIONS_JSON}}

Complete document formulas. Use these when the part references a formula from another part:
{{ALL_FORMULAS_JSON}}

Applied bundles and selected features for this part:
{{BUNDLE_SELECTIONS_JSON}}

Optional subject strategy:
{{SUBJECT_STRATEGY}}

Requirements:
1. Produce all five blueprint sections in one coherent response: headings, text_plan, image_plan, ca_plan, and validation_plan.
2. Text plan must state what will be taught, which source/analysis references support it, and which StudyForge containers are appropriate.
3. Image plan must focus on understanding difficult concepts. Recommend image count and styles based on learning need. Prefer one clear composite for related information, but request multiple images when one would be cluttered.
4. Each planned image must include learning goal, placement after a stable text/container anchor, recommended style, and style reasoning.
5. CA plan must generate editable query strings only. Do not execute searches now.
6. Validation plan must check the actual content dimensions in this part: formulas, comparisons, timelines, legal details, maps, personalities, processes, code, data, or other relevant elements. Do not use a rigid subject-only checklist.
7. Respect applied bundles but do not invent content absent from source/context.
8. Do not write final notes, generate images, or fetch current affairs in this call.

Return exactly this JSON object:
{
  "part_id": "",
  "headings": [
    {"heading_id": "H-1", "title": "", "level": 1, "purpose": ""}
  ],
  "text_plan": [
    {"container_id": "C-1", "heading_id": "H-1", "container_type": "", "teaching_goal": "", "source_refs": [], "analysis_refs": [], "bundle_features": []}
  ],
  "image_plan": [
    {"image_id": "IMG-1", "title": "", "placement_after": "C-1", "learning_goal": "", "content_to_show": [], "style_recommended": "", "style_reasoning": "", "mixed_style_allowed": true}
  ],
  "ca_plan": {
    "queries": [
      {"query_id": "CAQ-1", "query": "", "purpose": "", "related_heading_id": "H-1"}
    ]
  },
  "validation_plan": [
    {"check_id": "VAL-1", "what_to_check": "", "reason": "", "related_refs": []}
  ],
  "applied_bundles": []
}"""

# Inject AI_05
with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

insert_str = f"      AI_05: `{ai_05.replace('`', '\\`')}`,\n"
pattern = r'const DEFAULT_PROMPTS = \{'
match = re.search(pattern, content)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + '\n' + insert_str + content[insert_pos:]

# Replace Step2 completely
step2_replacement = """const Step2 = {
      init() {
        // UI updates when entering Screen 5
        document.getElementById('s2-detected-subject').textContent = appState.subject;
        document.getElementById('s2-card-subject').textContent = appState.subject;
      },
      async generateBlueprint() {
        document.getElementById('s2-progress-panel').classList.remove('hidden');
        document.getElementById('s2-blueprint-output').classList.add('hidden');
        const btn = document.getElementById('s2-gen-blueprint-btn');
        Helper.setBtnLoading(btn, `<svg class="w-5 h-5 animate-spin-slow inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> Generating Plan...`);

        const streamBox = document.getElementById('s2-raw-stream');
        streamBox.parentNode.classList.remove('hidden');
        streamBox.textContent = "[SYSTEM: Engineering parallel staggered blueprints for " + appState.blueprint.parts.length + " parts...]\\n";

        try {
          appState.blueprint.partPlans = [];
          
          for (let i = 0; i < appState.blueprint.parts.length; i++) {
             const part = appState.blueprint.parts[i];
             streamBox.textContent += `\\n[SYSTEM] Triggering AI-05 for ${part.part_id}...`;
             
             let p5 = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_05
               .replace('{{TOPIC}}', appState.subject)
               .replace('{{EXAM_CONTEXT}}', appState.category || 'General')
               .replace('{{PART_PLAN_JSON}}', JSON.stringify(part))
               .replace('{{SOURCE_SLICE}}', "See analysis context")
               .replace('{{PART_ANALYSIS_JSON}}', JSON.stringify(part.analysis_refs))
               .replace('{{ALL_DEFINITIONS_JSON}}', JSON.stringify(appState.deepAnalysis?.definitions || []))
               .replace('{{ALL_FORMULAS_JSON}}', JSON.stringify(appState.deepAnalysis?.formulas || []))
               .replace('{{BUNDLE_SELECTIONS_JSON}}', JSON.stringify(part.applied_bundles || []))
               .replace('{{SUBJECT_STRATEGY}}', '');

             let res = await API.generateContent(p5 + '\\n\\nOutput JSON only.');
             let parsed = JSON.parse(res.replace(/```json\\n?|```/g, ''));
             part.plan = parsed;
             appState.blueprint.partPlans.push(parsed);
             
             streamBox.textContent += `\\n[SYSTEM] Plan for ${part.part_id} completed successfully.`;
             streamBox.scrollTop = streamBox.scrollHeight;
             
             // Stagger delay
             await new Promise(r => setTimeout(r, 1000));
          }

          document.getElementById('s2-progress-panel').classList.add('hidden');
          document.getElementById('s2-blueprint-output').classList.remove('hidden');
          this.renderBlueprintCards();
          Session.save();

        } catch(e) { 
          Logger.add('ERROR', 'S5_BLUEPRINT', e.message);
          Toaster.show('Blueprint generation failed', 'rose'); 
          streamBox.textContent += `\\n[ERROR] ${e.message}`;
        }
        finally { Helper.setBtnLoading(btn, `✓ Generate Blueprint`, false); }
      },
      parseBlueprint(text) {
        // Legacy support/stub if needed
      },
      renderBlueprintCards() {
        const cardsDiv = document.getElementById('s2-bp-cards');
        if(!cardsDiv) return;
        
        let html = '';
        appState.blueprint.parts.forEach(part => {
           const p = part.plan;
           if (!p) return;
           html += `<div class="bg-white p-6 rounded-xl shadow border border-slate-200 mb-6">
             <h3 class="text-xl font-bold text-indigo-700">${part.part_id}: ${part.title}</h3>
             
             <div class="mt-4">
               <h4 class="font-bold text-sm text-slate-800">Headings</h4>
               <ul class="list-disc pl-5 text-sm text-slate-600 mt-2">
                 ${(p.headings || []).map(h => `<li><strong>${h.title}</strong> - ${h.purpose}</li>`).join('')}
               </ul>
             </div>
             
             <div class="mt-4">
               <h4 class="font-bold text-sm text-slate-800">Visual Plan</h4>
               <div class="space-y-2 mt-2">
                 ${(p.image_plan || []).map(img => `<div class="bg-slate-50 p-3 rounded text-sm border border-slate-200">
                   <strong>[${img.image_id}] ${img.title}</strong><br>
                   <span class="text-xs text-slate-500">Goal: ${img.learning_goal} | Style: ${img.style_recommended}</span>
                 </div>`).join('')}
                 ${(!p.image_plan || p.image_plan.length === 0) ? '<span class="text-sm text-slate-500">No images planned.</span>' : ''}
               </div>
             </div>
           </div>`;
        });
        cardsDiv.innerHTML = html;
      },
      approveBlueprint() {
        appState.blueprint.isApproved = true;
        document.getElementById('s2-app-gate-status').textContent = "Approved & Locked";
        document.getElementById('s2-approve-btn').className = "w-full py-3 bg-slate-700 text-white font-bold rounded-xl cursor-not-allowed";
        document.getElementById('s2-approve-btn').disabled = true;
        Session.save(); App.navigate(6);
      }
    };"""

pattern_replace = r'const Step2 = \{[\s\S]*?approveBlueprint\(\) \{[\s\S]*?\}\n    \};'
content = re.sub(pattern_replace, step2_replacement, content)

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step2 successfully replaced with Phase 4 logic!")
