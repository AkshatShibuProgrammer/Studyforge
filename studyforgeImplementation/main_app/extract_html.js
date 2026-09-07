const fs = require('fs');

const extract = (transcriptPath) => {
    const lines = fs.readFileSync(transcriptPath, 'utf8').split('\n');
    let html = '';
    
    for (let l of lines) {
        if (!l.trim()) continue;
        try {
            const d = JSON.parse(l);
            if (d.content && d.content.includes('<!DOCTYPE html>') && d.content.includes('<html')) {
                html = d.content;
                break;
            }
            if (d.tool_calls) {
                for (let call of d.tool_calls) {
                    if (call.function && call.function.arguments) {
                        const args = typeof call.function.arguments === 'string' ? JSON.parse(call.function.arguments) : call.function.arguments;
                        // look inside tool calls?
                    }
                }
            }
            if (d.output) { // For view_file output? transcript format uses 'tool_responses' maybe?
                 
            }
        } catch(e) {}
    }
    
    if (html) {
        fs.writeFileSync('recovered.html', html);
        console.log('Recovered file of length: ' + html.length);
    } else {
        console.log('Not found in content block, checking other places...');
    }
};

extract('C:\\Users\\Aksha\\.gemini\\antigravity\\brain\\3b978445-aadb-43f8-97a4-dc81c00eb978\\.system_generated\\logs\\transcript_full.jsonl');
extract('C:\\Users\\Aksha\\.gemini\\antigravity\\brain\\34ca128d-e077-4e14-b881-df4642c4ba75\\.system_generated\\logs\\transcript_full.jsonl');

