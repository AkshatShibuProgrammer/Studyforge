import re
import json

doc3 = open(r'F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect\StudyForge_Document_3_Canonical_Stored_Prompt_Library.md', encoding='utf-8').read()

def get_prompt(prompt_id):
    m = re.search(rf'## {prompt_id}.*?```text\n([\s\S]*?)\n```', doc3)
    return m.group(1).strip() if m else ""

prompts_to_inject = {
    'AI_07A': get_prompt('AI-07A'),
    'AI_07G': get_prompt('AI-07G'),
    'AI_07B': get_prompt('AI-07B'),
    'AI_07D': get_prompt('AI-07D')
}

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject missing prompts into DEFAULT_PROMPTS
for key, value in prompts_to_inject.items():
    if value and f"{key}: `" not in content:
        # Find the end of DEFAULT_PROMPTS
        m = re.search(r'const DEFAULT_PROMPTS = \{([\s\S]*?)\n\};', content)
        if m:
            safe_value = value.replace('`', '\\`')
            new_prompts = m.group(1) + f",\n  {key}: `{safe_value}`"
            content = content.replace(m.group(0), f"const DEFAULT_PROMPTS = {{{new_prompts}\n}};")

# Now update Step3 functions to use these canonical prompts
# 1. generateCA uses AI_07D
patch_ca = """async generateCA(partId) {
        const part = appState.blueprint.parts.find(p => p.id === partId);
        const btn = document.getElementById(`btn-gen-ca-${partId}`);
        const initBtn = document.getElementById(`btn-gen-ca-init-${partId}`);
        
        Helper.setBtnLoading(btn, `Searching...`);
        Helper.setBtnLoading(initBtn, `Searching...`);
        if (!this.isGeneratingAll) this.switchTab(partId, 'ca');
        
        const initEl = document.getElementById(`s3-init-ca-${partId}`); if (initEl) initEl.classList.add('hidden');
        const ctrlEl = document.getElementById(`s3-ca-controls-${partId}`); if (ctrlEl) ctrlEl.classList.remove('hidden');
        const contentEl = document.getElementById(`s3-render-ca-${partId}`);
        
        part.status = 'ca_generating'; this.updatePartHeaderUI(partId);
        
        let prompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07D
            .replace("{{TOPIC}}", appState.subject)
            .replace("{{EXAM_CONTEXT}}", appState.category || 'General')
            .replace("{{PART_PLAN_JSON}}", JSON.stringify(part.plan || {}));
            
        if (contentEl) contentEl.innerHTML = `<div class="p-6 bg-slate-50 border rounded-lg text-slate-500 font-mono text-xs animate-pulse">Scanning live search indices for ${appState.category} specific current affairs...</div>`;

        let rawRes = "";
        try {
          await API.streamContent(prompt, (chunk, acc) => {
            rawRes = acc; if(contentEl) contentEl.innerHTML = marked.parse(acc);
          }, { temp: 0.4, useTools: true });
          
          part.currentAffairsText = rawRes; part.status = 'ca_done'; Session.save();
          this.mergeCA(partId, true);
        } catch(e) { part.status = 'text_done'; Toaster.show(`Failed CA`, 'rose'); }
        finally { Helper.setBtnLoading(btn, `↻ Regenerate CA`, false); if(initBtn) Helper.setBtnLoading(initBtn, `🔍 Search CA`, false); }
        this.updatePartUI(partId);
      }"""
content = re.sub(r'async generateCA\(partId\) \{[\s\S]*?this\.updatePartUI\(partId\);\n      \}', lambda m: patch_ca, content)

# 2. genImageInline uses AI_07B
patch_img = """async genImageInline(partId, imgId, useExistingPrompt = false) {
        const part = appState.blueprint.parts.find(p=>p.id===partId);
        const img = part.images.find(i=>i.assetId===imgId);
        const spec = appState.blueprint.imageRegistry.find(r=>r.id===imgId) || {};
        if(!useExistingPrompt) {
          img.status = 'generating_prompt'; this.hydrateInlineImages(partId);
          try {
            let builderPrompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07B
              .replace(/\{\{EXAM_CONTEXT\}\}/g, appState.category || '')
              .replace(/\{\{PART_TOPIC\}\}/g, part.title || '')
              .replace(/\{\{IMAGE_REQUEST_JSON\}\}/g, JSON.stringify(spec))
              .replace(/\{\{SURROUNDING_TEXT_JSON\}\}/g, part.generatedTextRaw || '');
            const detailedPrompt = await API.generateContent(builderPrompt);
            // Assuming it returns JSON with "expanded_prompt"
            const match = detailedPrompt.match(/\{[\s\S]*\}/);
            const parsed = match ? JSON.parse(match[0]) : {expanded_prompt: detailedPrompt};
            img.prompt = parsed.expanded_prompt || detailedPrompt.replace(/^\[.*?\]\s*/gm, '').trim(); 
          } catch(e) { img.status = 'error'; Toaster.show(`Prompt build failed for ${imgId}`, 'rose'); this.hydrateInlineImages(partId); return; }
        } else { img.prompt = document.getElementById(`img-prompt-in-${imgId}`).value; }
        
        img.status = 'generating_image'; this.hydrateInlineImages(partId);
        try {
          let aspect = spec.template && spec.template.includes("FORMULA_CARD") ? "1:1" : "16:9";
          img.base64 = await API.generateImage(img.prompt, aspect);
          img.status = 'embedded'; img.approved = true; 
          
          if(part.generatedJSON && part.generatedJSON.image_needed) {
             let req = part.generatedJSON.image_needed.find(i => i.request_id === imgId);
             if(req) req.status = 'embedded';
          }
          part.generatedText = this.renderInlineContentHTML(part);
        } catch(e) { img.status = 'error'; Toaster.show('Image gen failed', 'rose'); }
        Session.save(); this.updatePartUI(partId);
      }"""
content = re.sub(r'async genImageInline\(partId, imgId, useExistingPrompt = false\) \{[\s\S]*?this\.updatePartUI\(partId\);\n      \}', lambda m: patch_img, content)

# 3. editImgPromptFirst uses AI_07B
patch_edit_img = """async editImgPromptFirst(partId, imgId) {
        const part = appState.blueprint.parts.find(p=>p.id===partId);
        const img = part.images.find(i=>i.assetId===imgId);
        const spec = appState.blueprint.imageRegistry.find(r=>r.id===imgId) || {};
        img.status = 'generating_prompt'; this.hydrateInlineImages(partId);
        try {
          let builderPrompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07B
              .replace(/\{\{EXAM_CONTEXT\}\}/g, appState.category || '')
              .replace(/\{\{PART_TOPIC\}\}/g, part.title || '')
              .replace(/\{\{IMAGE_REQUEST_JSON\}\}/g, JSON.stringify(spec))
              .replace(/\{\{SURROUNDING_TEXT_JSON\}\}/g, part.generatedTextRaw || '');
          const detailedPrompt = await API.generateContent(builderPrompt);
          const match = detailedPrompt.match(/\{[\s\S]*\}/);
          const parsed = match ? JSON.parse(match[0]) : {expanded_prompt: detailedPrompt};
          img.prompt = parsed.expanded_prompt || detailedPrompt.replace(/^\[.*?\]\s*/gm, '').trim(); 
          img.status = 'prompt_ready'; this.hydrateInlineImages(partId);
          document.getElementById(`img-editbox-${imgId}`).classList.remove('hidden');
          document.getElementById(`img-ctrls-${imgId}`).classList.add('hidden');
          document.getElementById(`img-prompt-in-${imgId}`).value = img.prompt;
        } catch(e) { img.status = 'error'; this.hydrateInlineImages(partId); }
      }"""
content = re.sub(r'async editImgPromptFirst\(partId, imgId\) \{[\s\S]*?this\.hydrateInlineImages\(partId\); \}\n      \}', lambda m: patch_edit_img, content)

# 4. submitRefine uses AI_07G
patch_refine = """async submitRefine(id) {
        const p = appState.blueprint.parts.find(x=>x.id===id);
        const inst = document.getElementById(`s3-refinefoot-in-${id}`).value; if(!inst) return;
        document.getElementById(`s3-stat-${id}`).textContent = 'REFINING';
        try {
          const prompt = appState.prompts.SYS_01 + "\\n\\n" + appState.prompts.AI_07G
              .replace('{{USER_INSTRUCTION}}', inst)
              .replace('{{CURRENT_PART_JSON}}', p.generatedTextRaw || '{}')
              .replace('{{SOURCE_SLICE}}', p.rawData || '')
              .replace('{{TARGET_ANCHOR}}', 'whole_part');
          
          const res = await API.generateContent(prompt + '\\n\\nOutput valid JSON only.');
          const parsed = JSON.parse(res.replace(/```json\\n?|```/g, '').trim());
          
          if(parsed.html_blocks) {
              p.generatedJSON = parsed;
              p.generatedTextRaw = JSON.stringify(parsed, null, 2);
              p.generatedText = this.renderInlineContentHTML(p);
          }
          
          if(p.approved) p.approvedButEdited = true;
          if(!p.versions) p.versions = [];
          p.versions.push({ versionNumber: p.versions.length+1, timestamp: new Date().toISOString(), type: 'ai_refine', content: p.generatedTextRaw, instruction: inst });
          document.getElementById(`s3-refinefoot-${id}`).classList.add('hidden');
          Session.save(); this.updatePartUI(id); Toaster.show('Refinement applied', 'purple');
        } catch(e) { Toaster.show('Refine failed', 'rose'); this.updatePartUI(id); }
      }"""
content = re.sub(r'async submitRefine\(id\) \{[\s\S]*?this\.updatePartUI\(id\); \}\n      \}', lambda m: patch_refine, content)

# 5. Fix HTML ids in renderFeed for ContainerEngine
content = content.replace("s3-sec-${p.part_id}", "s3-sec-${p.id}")
content = content.replace("s3-wrapper-${p.part_id}", "s3-wrapper-${p.id}")
content = content.replace("s3-stat-${p.part_id}", "s3-stat-${p.id}")
content = content.replace("Step3.generatePartText('${p.part_id}')", "Step3.generatePartText('${p.id}')")
content = content.replace("Step3.approvePart('${p.part_id}')", "Step3.approvePart('${p.id}')")
content = content.replace("s3-render-notes-${p.part_id}", "s3-render-notes-${p.id}")
content = content.replace("p.part_id", "p.id")

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected AI-07 prompts and updated generateCA, genImageInline, editImgPromptFirst, submitRefine!")
