import re
import json

doc3 = open(r'F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect\StudyForge_Document_3_Canonical_Stored_Prompt_Library.md', encoding='utf-8').read()

def get_prompt(prompt_prefix):
    # Splits by ## AI-07
    parts = doc3.split('## AI-07')
    for p in parts:
        if p.startswith(prompt_prefix):
            m = re.search(r'```text\n([\s\S]*?)\n```', p)
            if m: return m.group(1).strip()
    return ""

prompts_to_inject = {
    'AI_07H': get_prompt('H'),
    'AI_07I': get_prompt('I')
}

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject missing prompts into DEFAULT_PROMPTS
for key, value in prompts_to_inject.items():
    if value and f"{key}: `" not in content:
        m = re.search(r'const DEFAULT_PROMPTS = \{([\s\S]*?)\n\};', content)
        if m:
            safe_value = value.replace('`', '\\`')
            new_prompts = m.group(1) + f",\n  {key}: `{safe_value}`"
            content = content.replace(m.group(0), f"const DEFAULT_PROMPTS = {{{new_prompts}\n}};")

# We also need to add Step3.approvePart to trigger AI_07H
patch_approve = """async approvePart(partId) {
        const p = appState.blueprint.parts.find(x => x.id === partId || x.part_id === partId);
        if(!p) return;
        const btn = document.querySelector(`#s3-wrapper-${partId} button[onclick="Step3.approvePart('${partId}')"]`);
        if(btn) { btn.innerHTML = `Validating...`; btn.disabled = true; }
        
        try {
            let prompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07H
                .replace("{{BLUEPRINT_PART_JSON}}", JSON.stringify(p.plan || {}))
                .replace("{{CURRENT_GENERATED_PART_JSON}}", p.generatedTextRaw || "{}");
            
            const res = await API.generateContent(prompt + '\\n\\nOutput valid JSON only.');
            const parsed = JSON.parse(res.replace(/```json\\n?|```/g, '').trim());
            
            p.validation = parsed;
            if (parsed.status === 'PASS' || parsed.status === 'PASS_WITH_WARNINGS') {
                p.approved = true; 
                p.status = 'approved';
                Session.save(); this.renderFeed();
                Toaster.show(`Part ${partId} Approved. Score: ${parsed.score}/10`, 'emerald');
            } else {
                Toaster.show(`Part ${partId} failed validation. Check console.`, 'rose');
                console.warn("Validation failed for part", partId, parsed);
                if(btn) { btn.innerHTML = `✓ Approve`; btn.disabled = false; }
            }
        } catch(e) {
            Toaster.show(`Validation error on ${partId}`, 'amber');
            console.error(e);
            if(btn) { btn.innerHTML = `✓ Approve`; btn.disabled = false; }
        }
      }"""
content = re.sub(r'approvePart\(partId\) \{[\s\S]*?Toaster\.show\(`Part \$\{partId\} Approved`, \'emerald\'\);\n      \}', lambda m: patch_approve, content)

# And we need to add the Final Export Screen (Screen 8) that runs AI-07I and then exports
# Wait, App.compileExport() does the export.
patch_export = """async compileExport() {
        const out = document.getElementById('export-content-area'); 
        const wrapper = document.getElementById('screen-8');
        out.innerHTML = `<div class="p-8 text-center text-slate-500 font-mono animate-pulse">Running Final Consolidated Validation (AI-07I)...</div>`;
        
        try {
            let prompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07I
                .replace("{{ALL_PARTS_JSON}}", JSON.stringify(appState.blueprint.parts.map(p => ({id: p.id, title: p.title, status: p.status, validation: p.validation}))));
            
            const res = await API.generateContent(prompt + '\\n\\nOutput valid JSON only.');
            const parsed = JSON.parse(res.replace(/```json\\n?|```/g, '').trim());
            
            appState.finalValidation = parsed;
            console.log("Final Validation:", parsed);
        } catch(e) {
            console.error("Final validation failed", e);
        }

        let html = '';
        if (appState.finalValidation && appState.finalValidation.status !== 'PASS') {
            html += `<div class="p-4 bg-amber-50 border border-amber-200 text-amber-800 rounded-lg mb-8">
                <strong>Final Validation Warnings:</strong><br>
                ${(appState.finalValidation.gap_alerts || []).join('<br>')}
            </div>`;
        }
        
        appState.blueprint.parts.forEach(p => {
          if(!p.generatedText) return;
          let inner = p.generatedText;
          // Strip out the interactive buttons for export
          inner = inner.replace(/<button[\s\S]*?<\/button>/g, '');
          html += `<div class="export-part"><h2>${p.title}</h2>${inner}</div><hr class="my-8">`;
        });
        out.innerHTML = html;
        
        if (typeof renderMathInElement !== 'undefined') {
          renderMathInElement(out, {
            delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false}
            ]
          });
        }
      }"""
content = re.sub(r'compileExport\(\) \{[\s\S]*?\}\n      \}', lambda m: patch_export, content)

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected AI-07H and AI-07I, updated approvePart and compileExport!")
