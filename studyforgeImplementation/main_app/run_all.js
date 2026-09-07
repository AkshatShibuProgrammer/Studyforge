const { execSync } = require('child_process');
const scripts = [
    'update_phase0.js',
    'update_phase1.js',
    'update_phase1_ai02.js',
    'update_phase2.js',
    'update_phase3.js',
    'update_phase4.js',
    'update_phase5.js',
    'update_phase6.js',
    'update_phase7.js'
];

for (let script of scripts) {
    console.log(`Running ${script}...`);
    try {
        const out = execSync(`node "C:\\Users\\Aksha\\.gemini\\antigravity\\brain\\34ca128d-e077-4e14-b881-df4642c4ba75\\scratch\\${script}"`);
        console.log(out.toString());
    } catch (e) {
        console.error(`Error in ${script}`);
        console.error(e.stderr ? e.stderr.toString() : e.message);
    }
}
