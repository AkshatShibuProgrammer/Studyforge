import re

step3_replacement = """const ContainerEngine = {
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
        return `<div class="my-4 text-slate-800">${content}</div>`;
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

const Step3 = {
      renderFeed() {
        const container = document.getElementById('s3-feed');
        if(!container) return;
        if(appState.blueprint.parts.length === 0) return;
        document.getElementById('s3-empty-state').classList.add('hidden');
        
        container.innerHTML = appState.blueprint.parts.map(p => {
          return `
          <section id="s3-sec-${p.part_id}" class="part-section scroll-mt-48 mb-12 animate-fade-in">
            <div class="p-6 bg-white rounded-2xl border border-slate-200 shadow-sm" id="s3-wrapper-${p.part_id}">
              <div class="mb-4 flex justify-between items-start">
                <div>
                  <span class="text-xs bg-slate-800 text-white px-2 py-1 rounded font-mono">${p.part_id}</span>
                  <span class="font-bold text-slate-800 text-sm ml-2">${p.title}</span>
                </div>
                <span id="s3-stat-${p.part_id}" class="text-xs font-bold px-3 py-1 rounded bg-slate-100 text-slate-600">${p.approved ? 'APPROVED' : (p.status || 'PENDING').toUpperCase()}</span>
              </div>
              <div class="border border-slate-200 rounded-xl bg-white overflow-hidden mb-4">
                <div class="p-4 bg-slate-50 border-b border-slate-200 flex justify-between">
                   <span class="font-bold text-slate-700 text-sm">Generated Notes</span>
                   <div>
                     <button onclick="Step3.generatePartText('${p.part_id}')" class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg shadow-sm">Generate / Regenerate</button>
                     ${!p.approved ? `<button onclick="Step3.approvePart('${p.part_id}')" class="ml-2 px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-lg text-xs shadow-sm transition">✓ Approve</button>` : ''}
                   </div>
                </div>
                <div class="p-4 min-h-[150px]" id="s3-render-notes-${p.part_id}">
                  ${p.generatedBlocks ? p.generatedBlocks.map(b => ContainerEngine.render(b)).join('') : '<div class="text-slate-400 text-sm italic">Not generated yet.</div>'}
                </div>
              </div>
            </div>
          </section>`;
        }).join('');
      },
      
      async generatePartText(partId) {
        const part = appState.blueprint.parts.find(p => p.part_id === partId);
        const contentEl = document.getElementById(`s3-render-notes-${partId}`);
        if(!contentEl) return;
        
        contentEl.innerHTML = `<div class="p-6 bg-slate-50 border rounded-lg text-slate-500 font-mono text-xs animate-pulse">Contacting Gemini Core. Assembling containers using AI-07A... Please wait.</div>`;
        part.status = 'generating'; this.updateHeader(partId);

        let p_str = appState.prompts.SYS_01 + '\\n\\n' + appState.prompts.AI_07A
            .replace('{{TOPIC}}', appState.subject)
            .replace('{{EXAM_CONTEXT}}', appState.category || 'General')
            .replace('{{PART_PLAN_JSON}}', JSON.stringify(part.plan || {}))
            .replace('{{SOURCE_SLICE}}', "See attached analysis.")
            .replace('{{PART_ANALYSIS_JSON}}', JSON.stringify(part.analysis_refs || {}))
            .replace('{{ALL_DEFINITIONS_JSON}}', JSON.stringify(appState.deepAnalysis?.definitions || []))
            .replace('{{ALL_FORMULAS_JSON}}', JSON.stringify(appState.deepAnalysis?.formulas || []))
            .replace('{{BLUEPRINT_JSON}}', JSON.stringify(appState.blueprint))
            .replace('{{BUNDLE_SELECTIONS_JSON}}', JSON.stringify(part.applied_bundles || []))
            .replace('{{CA_RESULTS_JSON}}', '[]');

        try {
          const res = await API.generateContent(p_str + '\\n\\nOutput JSON only.');
          const parsed = JSON.parse(res.replace(/```json\\n?|```/g, ''));
          part.generatedBlocks = parsed.html_blocks || [];
          contentEl.innerHTML = part.generatedBlocks.map(b => ContainerEngine.render(b)).join('');
          part.status = 'done'; Session.save();
        } catch(e) {
          part.status = 'error'; 
          contentEl.innerHTML = `<div class="text-rose-600 text-sm">Failed to generate: ${e.message}</div>`;
        }
        this.updateHeader(partId);
      },
      
      updateHeader(partId) {
        const p = appState.blueprint.parts.find(x => x.part_id === partId);
        const stat = document.getElementById(`s3-stat-${partId}`);
        if(stat) stat.textContent = p.approved ? 'APPROVED' : (p.status || 'PENDING').toUpperCase();
      },

      approvePart(partId) {
        const p = appState.blueprint.parts.find(x => x.part_id === partId);
        p.approved = true; Session.save(); this.renderFeed();
        Toaster.show(`Part ${partId} Approved`, 'emerald');
      },

      generateEverything() {
        // Just sequentially generate everything
        appState.blueprint.parts.forEach(async (p, idx) => {
           if(!p.generatedBlocks) {
               await new Promise(r => setTimeout(r, idx * 2000));
               this.generatePartText(p.part_id);
           }
        });
      },

      approveAllParts() {
         appState.blueprint.parts.forEach(p => p.approved = true);
         Session.save(); this.renderFeed();
      }
    };"""

with open('studyforge_main.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'const Step3 = \{[\s\S]*?if\(n===7 && window\.Step3\) Step3\.renderFeed\(\);'
match = re.search(pattern, content)
if match:
    # Need to be careful not to delete the navTo logic since it's after Step3.
    # The regex match ends at `if(n===7 && window.Step3) Step3.renderFeed();` 
    # That means we matched too much!
    pass

# Better replacement strategy: replace just Step3 object
pattern2 = r'const Step3 = \{[\s\S]*?\n    \};\n'
content = re.sub(pattern2, step3_replacement + '\n', content)

with open('studyforge_main.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step3 replaced with new ContainerEngine and AI-07A integration!")
