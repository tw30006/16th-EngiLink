const esbuild = require('esbuild');

esbuild.build({
    entryPoints: ["scripts/entry.js"],
    bundle: true,
    outfile: "bundle.js",
}).catch(() => process.exit(1));
