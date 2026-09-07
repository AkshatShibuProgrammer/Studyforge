import re

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad_pattern = r'const ContainerEngine = \{[\s\S]*?approveAllParts\(\) \{[\s\S]*?\}\n    \};'
content = re.sub(bad_pattern, '/*_STEP3_PLACEHOLDER_*/', content)

with open('step3_full_dump.txt', 'r', encoding='utf-8') as f:
    orig_step3 = f.read()

container_engine = """const ContainerEngine = {
  render(block) {
    const titleHtml = block.title ? `<h4 class="font-bold mb-2 flex items-center gap-2">${block.title}</h4>` : '';
    const traceBadge = this.getTraceBadge(block.traceability);
    const content = marked.parse(block.safe_content || '');
    
    switch(block.container_type) {
      case 'concept_box':
        return `<div class="my-4 p-5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-slate-700 text-sm">${content}</div></div>`;
      case 'formula_box':
        return `<div class="my-4 p-5 bg-slate-800 border border-slate-700 rounded-xl shadow-md text-white"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="font-mono text-emerald-300 text-sm overflow-x-auto">${content}</div></div>`;
      case 'story_box':
        return `<div class="my-4 p-5 bg-amber-50 border border-amber-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-amber-900 text-sm italic">${content}</div></div>`;
      case 'legal_box':
        return `<div class="my-4 p-5 bg-slate-50 border-l-4 border-slate-500 rounded-r-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="font-serif text-slate-800 text-sm">${content}</div></div>`;
      case 'ca_box':
        return `<div class="my-4 p-5 bg-sky-50 border border-sky-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-sky-900 text-sm">${content}</div></div>`;
      case 'data_insight':
        return `<div class="my-4 p-5 bg-emerald-50 border border-emerald-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-emerald-900 text-sm font-semibold">${content}</div></div>`;
      case 'process_box':
        return `<div class="my-4 p-5 bg-purple-50 border border-purple-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-purple-900 text-sm">${content}</div></div>`;
      case 'personality_box':
        return `<div class="my-4 p-5 bg-orange-50 border border-orange-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-orange-900 text-sm">${content}</div></div>`;
      case 'confusion_alert':
        return `<div class="my-4 p-5 bg-rose-50 border-l-4 border-rose-500 rounded-r-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-rose-900 text-sm">${content}</div></div>`;
      case 'geography_box':
        return `<div class="my-4 p-5 bg-stone-100 border border-stone-300 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-stone-800 text-sm">${content}</div></div>`;
      case 'medical_box':
        return `<div class="my-4 p-5 bg-red-50 border border-red-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-red-900 text-sm">${content}</div></div>`;
      case 'experiment_box':
        return `<div class="my-4 p-5 bg-teal-50 border border-teal-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-teal-900 text-sm">${content}</div></div>`;
      case 'admin_box':
        return `<div class="my-4 p-5 bg-indigo-50 border border-indigo-200 rounded-xl shadow-sm"><div class="flex justify-between items-start">${titleHtml}${traceBadge}</div><div class="text-indigo-900 text-sm">${content}</div></div>`;
      case 'comparison_table':
        return `<div class="my-4 w-full overflow-x-auto border border-slate-200 rounded-xl"><div class="flex justify-end p-2 bg-slate-50">${traceBadge}</div><div class="p-4">${content}</div></div>`;
      default:
        return `<div class="my-4 text-slate-800"><div class="flex justify-end">${traceBadge}</div>${content}</div>`;
    }
  },
  getTraceBadge(trace) {
    if(!trace) return '';
    const map = {
      'SOURCE_BACKED': '<span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 text-[10px] font-bold rounded">Source Backed</span>',
      'RESEARCH_REQUIRED': '<span class="px-2 py-0.5 bg-amber-100 text-amber-700 text-[10px] font-bold rounded">Inferred/Research</span>',
      'OPTIONAL_ENRICHMENT': '<span class="px-2 py-0.5 bg-purple-100 text-purple-700 text-[10px] font-bold rounded">Enrichment</span>',
      'WEB_SOURCED': '<span class="px-2 py-0.5 bg-sky-100 text-sky-700 text-[10px] font-bold rounded">Live Web</span>'
    };
    return map[trace] || `<span class="px-2 py-0.5 bg-slate-100 text-slate-700 text-[10px] font-bold rounded">${trace}</span>`;
  }
};
"""

generate_part_text_patch = """async generatePartText(partId) {
        const part = appState.blueprint.parts.find(p => p.id === partId);
        const btn = document.getElementById(`btn-gen-notes-${partId}`);
        const initBtn = document.getElementById(`btn-gen-notes-init-${partId}`);
        
        Helper.setBtnLoading(btn, `Generating...`);
        Helper.setBtnLoading(initBtn, `Generating...`);
        if (!this.isGeneratingAll) this.switchTab(partId, 'notes');
        
        const initEl = document.getElementById(`s3-init-notes-${partId}`); if (initEl) initEl.classList.add('hidden');
        const ctrlEl = document.getElementById(`s3-notes-controls-${partId}`); if (ctrlEl) ctrlEl.classList.remove('hidden');
        const contentEl = document.getElementById(`s3-render-notes-${partId}`); if (!contentEl) return;
        
        part.status = 'text_generating'; this.updatePartHeaderUI(partId);
        
        contentEl.innerHTML = `<div class="p-6 bg-slate-50 border rounded-lg text-slate-500 font-mono text-xs animate-pulse">Contacting Gemini Core. Generating JSON structure... Please wait.</div>`;

        let finalPrompt = (appState.prompts.SYS_01 || "") + '\\n\\n' + (appState.prompts.AI_07A || "")
            .replace('{{TOPIC}}', appState.subject || '')
            .replace('{{EXAM_CONTEXT}}', appState.category || '')
            .replace('{{PART_PLAN_JSON}}', JSON.stringify(part.plan || {}))
            .replace('{{SOURCE_SLICE}}', part.rawData || "See attached analysis.")
            .replace('{{PART_ANALYSIS_JSON}}', JSON.stringify(part.analysis_refs || {}))
            .replace('{{ALL_DEFINITIONS_JSON}}', JSON.stringify(appState.deepAnalysis?.definitions || []))
            .replace('{{ALL_FORMULAS_JSON}}', JSON.stringify(appState.deepAnalysis?.formulas || []))
            .replace('{{BLUEPRINT_JSON}}', JSON.stringify(appState.blueprint || {}))
            .replace('{{BUNDLE_SELECTIONS_JSON}}', JSON.stringify(part.applied_bundles || []))
            .replace('{{CA_RESULTS_JSON}}', '[]');

        part.generatedTextRaw = ""; part.generatedText = "";
        try {
          const res = await API.generateContent(finalPrompt + '\\n\\nOutput valid JSON only.', {temp: 0.5});
          const jsonStr = res.replace(/```json\\n?|```/g, '').trim();
          const parsed = JSON.parse(jsonStr);
          part.generatedJSON = parsed;
          part.generatedTextRaw = JSON.stringify(parsed, null, 2);
          part.generatedText = this.renderInlineContentHTML(part);
          if (contentEl) contentEl.innerHTML = part.generatedText;
          const wc = document.getElementById(`s3-word-count-${partId}`); if(wc) wc.textContent = part.generatedTextRaw.split(/\\s+/).length;
          
          if (parsed.image_needed && parsed.image_needed.length > 0) {
              parsed.image_needed.forEach(req => {
                  let imgId = req.request_id || `IMAGE_${part.partNumber}.${Math.floor(Math.random()*1000)}`;
                  let existingRegistry = appState.blueprint.imageRegistry.find(r => r.id === imgId);
                  if(!existingRegistry) {
                      appState.blueprint.imageRegistry.push({
                          id: imgId,
                          topic: req.description,
                          layout: req.style_hint,
                          template: 'custom'
                      });
                  }
              });
          }
          this.hydrateInlineImages(partId);
          
          part.status = 'text_done'; Session.save();
        } catch(e) { part.status = 'not_started'; Toaster.show(`Failed: ${part.id}`, 'rose'); }
        finally { 
          Helper.setBtnLoading(btn, `↻ Regenerate`, false); 
          if(initBtn) Helper.setBtnLoading(initBtn, `⚡ Generate Notes`, false); 
          
          if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(contentEl, {
              delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false}
              ]
            });
          }
        }
        this.updatePartUI(partId); 
      }"""

render_inline_patch = """renderInlineContentHTML(part) {
        if(part.generatedJSON && part.generatedJSON.html_blocks) {
            let html = part.generatedJSON.html_blocks.map(b => {
                let out = ContainerEngine.render(b);
                if (part.generatedJSON.image_needed) {
                    part.generatedJSON.image_needed.filter(i => i.after_anchor === b.anchor).forEach(i => {
                        out += this.mountHtml(part.id, i.request_id);
                    });
                }
                return out;
            }).join('');
            
            if (part.generatedJSON.image_needed) {
                 part.generatedJSON.image_needed.filter(i => !i.after_anchor || !part.generatedJSON.html_blocks.find(b => b.anchor === i.after_anchor)).forEach(i => {
                     html += this.mountHtml(part.id, i.request_id);
                 });
            }
            
            if (part.currentAffairsMerged && part.currentAffairsText) {
                html += `\\n\\n<h3 class="font-bold text-lg mt-8 mb-4 border-b pb-2">📰 Current Affairs Supplement</h3>\\n` + marked.parse(part.currentAffairsText);
            }
            return html;
        } else {
            let html = marked.parse(part.generatedTextRaw || '');
            html = html.replace(/<p>IMAGE_NEEDED:\\s*(IMAGE_\\d+\\.\\d+)<\\/p>/g, (m, id) => this.mountHtml(part.id, id));
            html = html.replace(/IMAGE_NEEDED:\\s*(IMAGE_\\d+\\.\\d+)/g, (m, id) => this.mountHtml(part.id, id));
            html = html.replace(/<p>%%%EMBEDDED_IMAGE_(IMAGE_\\d+\\.\\d+)%%%<\\/p>/g, (m, id) => this.mountHtml(part.id, id));
            html = html.replace(/%%%EMBEDDED_IMAGE_(IMAGE_\\d+\\.\\d+)%%%/g, (m, id) => this.mountHtml(part.id, id));
            return html;
        }
      }"""

orig_step3 = re.sub(r'async generatePartText\(partId\) \{[\s\S]*?this\.updatePartUI\(partId\); \n      \}', lambda m: generate_part_text_patch, orig_step3)
orig_step3 = re.sub(r'renderInlineContentHTML\(part\) \{[\s\S]*?return html;\n      \}', lambda m: render_inline_patch, orig_step3)

final_injection = container_engine + "\n\n" + orig_step3
content = content.replace('/*_STEP3_PLACEHOLDER_*/', final_injection)

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully restored Step3 and integrated ContainerEngine!")
