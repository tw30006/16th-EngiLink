const esbuild = require('esbuild');

esbuild.build({
    entryPoints: ["static/scripts/app.js"],
    bundle: true,
    outfile: "outfile/out.js",
}).catch(() => process.exit(1));
